// SPDX-License-Identifier: Apache-2.0
// Author: Qiyaya

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <time.h>
#include <stdbool.h>

#ifdef _WIN32
    #include <windows.h>
    #define sleep_ms(ms) Sleep(ms)  // Windows Sleep() takes milliseconds
#else
    #include <unistd.h>
#endif

static PyObject *update_callback = NULL;
static PyObject *render_callback = NULL;
static PyObject *update_func = NULL;
static PyObject *render_func = NULL;
static bool running = false;
static double target_fps = 60.0;

#ifdef _WIN32
static void enable_high_precision_timer() {
    timeBeginPeriod(1);  // Improves sleep accuracy to 1ms
}
#endif

// Cross-platform high-resolution timer
static double get_time() {
#ifdef _WIN32
    LARGE_INTEGER frequency, counter;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart / (double)frequency.QuadPart;
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1.0e9;
#endif
}

static void precise_sleep(double seconds) {
#ifdef _WIN32
    Sleep((DWORD)(seconds * 1000));  // Convert seconds to milliseconds
#else
    struct timespec ts;
    ts.tv_sec = (time_t)seconds;
    ts.tv_nsec = (long)((seconds - ts.tv_sec) * 1e9);
    nanosleep(&ts, NULL);
#endif
}

static PyObject* start_game_loop(PyObject *self, PyObject *args) {
    double delta_time;
    double frame_time = 1.0 / target_fps;

#ifdef _WIN32
    enable_high_precision_timer();
#endif

    running = true;
    double previous_time = get_time();

    // Cache function pointers to reduce Python overhead
    update_func = update_callback;
    render_func = render_callback;
    Py_XINCREF(update_func);
    Py_XINCREF(render_func);

    int frame_counter = 0;

    while (running) {
        double current_time = get_time();
        delta_time = current_time - previous_time;
        previous_time = current_time;

        if (update_func && PyCallable_Check(update_func)) {
            PyObject *arg = PyFloat_FromDouble(delta_time);
            PyObject *result = PyObject_CallObject(update_func, PyTuple_Pack(1, arg));
            Py_DECREF(arg);
            if (!result) {
                PyErr_Print();
                running = false;
                break;
            }
            Py_DECREF(result);
        }

        if (!running) break;

        if (render_func && PyCallable_Check(render_func)) {
            PyObject *result = PyObject_CallObject(render_func, NULL);
            if (!result) {
                PyErr_Print();
                running = false;
                break;
            }
            Py_DECREF(result);
        }

        if (!running) break;

        // Reduce the frequency of checking Python signals (every 30 frames)
        if (++frame_counter % 30 == 0 && PyErr_CheckSignals() != 0) {
            running = false;
            PyErr_SetInterrupt();
            break;
        }

        // Sleep to maintain target frame rate
        double sleep_time = frame_time - (get_time() - previous_time);
        if (sleep_time > 0 && running) {
            precise_sleep(sleep_time);
        }
    }

    Py_XDECREF(update_func);
    Py_XDECREF(render_func);
    update_func = NULL;
    render_func = NULL;

    Py_RETURN_NONE;
}

static PyObject* stop_game_loop(PyObject *self, PyObject *args) {
    running = false;
    Py_RETURN_NONE;
}

static PyObject* set_update(PyObject *self, PyObject *args) {
    PyObject *temp;
    if (!PyArg_ParseTuple(args, "O", &temp)) {
        return NULL;
    }
    if (!PyCallable_Check(temp)) {
        PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
        return NULL;
    }
    Py_XINCREF(temp);
    Py_XDECREF(update_callback);
    update_callback = temp;
    Py_RETURN_NONE;
}

static PyObject* set_render(PyObject *self, PyObject *args) {
    PyObject *temp;
    if (!PyArg_ParseTuple(args, "O", &temp)) {
        return NULL;
    }
    if (!PyCallable_Check(temp)) {
        PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
        return NULL;
    }
    Py_XINCREF(temp);
    Py_XDECREF(render_callback);
    render_callback = temp;
    Py_RETURN_NONE;
}

static PyObject* set_fps(PyObject *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, "d", &target_fps)) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyMethodDef GameLoopMethods[] = {
    {"start", start_game_loop, METH_NOARGS, "Start the game loop"},
    {"stop", stop_game_loop, METH_NOARGS, "Stop the game loop"},
    {"set_update", set_update, METH_VARARGS, "Set the update function"},
    {"set_render", set_render, METH_VARARGS, "Set the render function"},
    {"set_fps", set_fps, METH_VARARGS, "Set the FPS"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef gameloopmodule = {
    PyModuleDef_HEAD_INIT,
    "miniloop",
    "Render cycle loop handler",
    -1,
    GameLoopMethods
};

PyMODINIT_FUNC PyInit_miniloop(void) {
    return PyModule_Create(&gameloopmodule);
}
