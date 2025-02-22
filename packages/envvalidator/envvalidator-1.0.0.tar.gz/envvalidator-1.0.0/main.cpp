// SPDX-License-Identifier: Apache-2.0
// Author: Qiyaya

#define PY_SSIZE_T_CLEAN
extern "C" { 
    #include <Python.h> 
}

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <regex>
#include <unordered_map>

std::string trim_whitespace(const std::string &str) {
    size_t start = str.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    size_t end = str.find_last_not_of(" \t\n\r");
    return str.substr(start, end - start + 1);
}

bool is_integer(const std::string &str) {
    static const std::regex int_regex(R"(^-?\d+$)");
    return std::regex_match(str, int_regex);
}

bool is_boolean(const std::string &str) {
    return str == "true" || str == "false" || str == "TRUE" || str == "FALSE";
}

bool matches_regex(const std::string &value, const std::string &pattern) {
    std::regex regex_pattern(pattern);
    return std::regex_match(value, regex_pattern);
}

static PyObject *validate_env(PyObject *self, PyObject *args) {
    const char *file_path;
    PyObject *schema;

    if (!PyArg_ParseTuple(args, "sO!", &file_path, &PyDict_Type, &schema)) {
        return NULL;
    }

    std::unordered_map<std::string, std::string> env_vars;
    std::ifstream file(file_path);

    if (file) {
        std::string line;
        while (std::getline(file, line)) {
            if (line.empty() || line[0] == '#') continue; // Ignore comments and empty lines
            
            size_t pos = line.find('=');
            if (pos == std::string::npos) continue; // Invalid line
            
            std::string key = trim_whitespace(line.substr(0, pos));
            std::string value = trim_whitespace(line.substr(pos + 1));

            env_vars[key] = value;
        }
        file.close();
    }
    PyObject *result_dict = PyDict_New();

    PyObject *keys = PyDict_Keys(schema);
    Py_ssize_t size = PyList_Size(keys);

    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject *key_obj = PyList_GetItem(keys, i);
        const char *key = PyUnicode_AsUTF8(key_obj);
        PyObject *expected_type = PyDict_GetItem(schema, key_obj);

        std::string value;
        if (env_vars.find(key) != env_vars.end()) {
            value = env_vars[key];
        } else {
            const char *env_value = getenv(key);
            if (env_value) {
                value = std::string(env_value);
            } else {
                PyErr_Format(PyExc_ValueError, "Missing required environment variable: %s", key);
                return NULL;
            }
        }

        // Validate types
        if (PyUnicode_Check(expected_type)) {
            std::string expected_type_str = PyUnicode_AsUTF8(expected_type);
            if (expected_type_str == "int" && !is_integer(value)) {
                PyErr_Format(PyExc_ValueError, "Invalid integer for key '%s'", key);
                return NULL;
            } else if (expected_type_str == "bool" && !is_boolean(value)) {
                PyErr_Format(PyExc_ValueError, "Invalid boolean for key '%s'", key);
                return NULL;
            }
        } else if (PyDict_Check(expected_type)) {
            PyObject *regex_pattern = PyDict_GetItemString(expected_type, "regex");
            if (regex_pattern && PyUnicode_Check(regex_pattern)) {
                std::string pattern = PyUnicode_AsUTF8(regex_pattern);
                if (!std::regex_match(value, std::regex(pattern))) {
                    PyErr_Format(PyExc_ValueError, "Value '%s' does not match regex pattern for key '%s'", value.c_str(), key);
                    return NULL;
                }
            }
        }

        PyDict_SetItemString(result_dict, key, PyUnicode_FromString(value.c_str()));
    }

    return result_dict;
}

// Define module methods
static PyMethodDef EnvValidatorMethods[] = {
    {"validate_env", validate_env, METH_VARARGS, "Validate a .env file against a schema, with system variable fallback and regex support."},
    {NULL, NULL, 0, NULL}
};

// Define module
static struct PyModuleDef envvalidatormodule = {
    PyModuleDef_HEAD_INIT,
    "envvalidator",
    "Environment variable validator",
    -1,
    EnvValidatorMethods
};

// Initialize module
PyMODINIT_FUNC PyInit_envvalidator(void) {
    return PyModule_Create(&envvalidatormodule);
}
