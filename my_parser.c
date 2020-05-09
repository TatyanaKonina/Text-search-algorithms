#include<Python.h>
#include "structs.h"
#include <string.h>
#include "my_parser.h"

PyObject* python_func_init() {
    PyObject* pName, * pModule, * pDict, * pFunc, * pVal;
    Py_Initialize();
    PyObject* sysmodule = PyImport_ImportModule("sys");
    PyObject* syspath = PyObject_GetAttrString(sysmodule, "path");
    PyList_Append(syspath, PyUnicode_FromString("."));
    Py_DECREF(syspath);
    Py_DECREF(sysmodule);

    // Initialize the Python Interpreter
    // Build the name object
    pName = PyUnicode_FromString("try");
    if (!pName) {
        exit( ERROR_OPEN_PYFILE);
    }

    // Load the module object
    pModule = PyImport_Import(pName);
    if (!pModule) {
        exit( ERROR_MODULE_OBJECT);
    }

    // pDict is a borrowed reference 
    pDict = PyModule_GetDict(pModule);
    if (!pDict) {
        exit( ERROR_DICT_OBJECT);
    }

    // pFunc is also a borrowed reference 
    pFunc = PyDict_GetItemString(pDict, "book_parser");
    if (!pFunc) {
        exit( ERROR_FUNC);
    }
    Py_DECREF(pDict);
    Py_DECREF(pModule);
    Py_DECREF(pName);
    return pFunc;
}

char* parser(PyObject* pFunc) {
    char* text = NULL;
    PyObject* pVal;
    if (PyCallable_Check(pFunc))
    {
        pVal = PyObject_CallFunction(pFunc, NULL);
        if (pVal != NULL) {
            PyObject* pResultRepr = PyObject_Repr(pVal);
            // ≈сли полученную строку не скопировать, то после очистки ресурсов Python еЄ не будет.
            // ƒл€ начала pResultRepr нужно привести к массиву байтов.
            text = _strdup(PyBytes_AS_STRING(PyUnicode_AsEncodedString(pResultRepr, "utf-8", "ERROR")));
            Py_XDECREF(pResultRepr);
            Py_XDECREF(pVal);
        }
        else {
            exit( ERROR_CALL_FUNC);
        }
    }
    return text;
}

void python_clean(PyObject* pFunc) {
    Py_DECREF(pFunc);
    Py_Finalize();// Finish the Python Interpreter
}

SearchRequest* text_parser(char * pattern) {
    SearchRequest* Request;
    Request = (SearchRequest*)malloc(sizeof(SearchRequest));
    Request->pattern = (Pattern*)malloc(sizeof(Pattern));
    Request->pattern->needleSize = 0;
    Request->text = (Text*)malloc(sizeof(Text));
    Request->text->haystackSize = 0;

    Request->pattern->needle = _strdup(pattern);
    Request->pattern->needleSize = strlen(pattern);

    PyObject* pFunc;
    pFunc = python_func_init();
   
    Request->text->haystack = _strdup(parser(pFunc));
    Request->text->haystackSize = strlen(Request->text->haystack);

    python_clean(pFunc);

    return Request;
}