#include <Python.h>
extern int chkauthattr(const char *authname, const char* username);

static PyObject *SecdbError;
static PyObject * secdb_chkauthattr(PyObject *self, PyObject *args);

static PyMethodDef SecdbMethods[] = {
    {"chkauthattr",  secdb_chkauthattr, METH_VARARGS,
     "Check Authorization Attribute."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static PyObject *
secdb_chkauthattr(PyObject *self, PyObject *args)
{
    const char *attr;
    const char *user;
    int sts;

    if (!PyArg_ParseTuple(args, "ss", &attr, &user))
        return NULL;
    sts = chkauthattr(attr, user);
    return Py_BuildValue("i", sts);
}

PyMODINIT_FUNC
initsecdb(void)
{
    PyObject *m;

    m = Py_InitModule("secdb", SecdbMethods);
    if (m == NULL)
        return;

    SecdbError = PyErr_NewException("secdb.error", NULL, NULL);
    Py_INCREF(SecdbError);
    PyModule_AddObject(m, "error", SecdbError);
}

