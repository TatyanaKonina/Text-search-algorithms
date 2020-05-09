#pragma once
#ifndef PARSER_H
#define PERSER_H
#include <Python.h>
#include "structs.h"

PyObject* python_func_init();

char* parser(PyObject* pFunc);

void python_clean(PyObject* pFunc);


#endif // !PARCER_H

