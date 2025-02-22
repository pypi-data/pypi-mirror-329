#include <stdbool.h>

#include <Python.h>
#include <numpy/arrayobject.h>

// Function to parse NumPy array input
static int** parse_numpy_matrix(PyArrayObject *matrix, int *n) {
    *n = PyArray_DIM(matrix, 0);  // Get matrix size
    int **adj = malloc(*n * sizeof(int*));
    
    for (int i = 0; i < *n; i++) {
        adj[i] = (int*) PyArray_GETPTR2(matrix, i, 0);
    }
    
    return adj;
}

// Returns a greedy independent set
static PyObject* max_independent_set(PyObject *self, PyObject *args) {
    PyArrayObject *matrix;
    if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &matrix)) return NULL;

    int n;
    int **adj = parse_numpy_matrix(matrix, &n);
    bool *in_set = calloc(n, sizeof(bool));

    // Greedy selection: pick nodes with the least neighbors first
    for (int i = 0; i < n; i++) {
        bool independent = true;
        for (int j = 0; j < n; j++) {
            if (adj[i][j] && in_set[j]) {
                independent = false;
                break;
            }
        }
        if (independent) in_set[i] = true;
    }

    // Convert result to a Python list
    PyObject *result = PyList_New(0);
    for (int i = 0; i < n; i++) {
        if (in_set[i]) PyList_Append(result, PyLong_FromLong(i));
    }

    free(in_set);
    free(adj);
    return result;
}

static PyMethodDef MISMethods[] = {
    {"max_independent_set", max_independent_set, METH_VARARGS, "Find a Maximum Independent Set"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mis_module = {
    PyModuleDef_HEAD_INIT, "mispy", NULL, -1, MISMethods
};

PyMODINIT_FUNC PyInit_mis(void) {
    import_array();  // Initialize NumPy C API
    return PyModule_Create(&mis_module);
}
