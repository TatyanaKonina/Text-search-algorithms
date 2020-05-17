#include<Python.h>
#include "structs.h"
#include <string.h>
#include "my_parser.h"

PyObject* python_func_init() {
    PyObject* pName, * pModule, * pDict, * pFunc, * pVal;
    Py_Initialize();// Загрузка интерпретатора Python
    PyObject* sysmodule = PyImport_ImportModule("sys");// Выполнение команд в интерпретаторе
    PyObject* syspath = PyObject_GetAttrString(sysmodule, "path");// Загрузка модуля sys
    PyList_Append(syspath, PyUnicode_FromString("."));
    Py_DECREF(syspath);
    Py_DECREF(sysmodule);
    pName = PyUnicode_FromString("try"); // Загрузка try.py
    if (!pName) {
        exit( ERROR_OPEN_PYFILE);
    }
    pModule = PyImport_Import(pName);/ Загрузить объект модуля
    if (!pModule) {
        exit( ERROR_MODULE_OBJECT);
    }
    pDict = PyModule_GetDict(pModule);// Словарь объектов содержащихся в модуле
    if (!pDict) {
        exit( ERROR_DICT_OBJECT);
    }
    pFunc = PyDict_GetItemString(pDict, "book_parser");
    if (!pFunc) {
        exit( ERROR_FUNC);
    }
    Py_DECREF(pDict);// Вернуть ресурсы системе
    Py_DECREF(pModule);
    Py_DECREF(pName);
    return pFunc;
}

char* parser(PyObject* pFunc) {
    char* text = NULL;
    PyObject* pVal;
    if (PyCallable_Check(pFunc))// Проверка pObjct на годность.
    {
        pVal = PyObject_CallFunction(pFunc, NULL);// Получить объект с именем val
        if (pVal != NULL) {
            PyObject* pResultRepr = PyObject_Repr(pVal);
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
    Py_Finalize();
}
