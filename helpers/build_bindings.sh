#!/bin/sh

OUT="protoserial$(python3-config --extension-suffix)"
DINC="-Isubmodules/libprotoserial -Isubmodules/pybind11/include -Isubmodules/libprotoserial/submodules/etl/include -I/usr/include/python3.10 $(python3 -m pybind11 --includes)"

g++ -Wall -shared -std=c++20 -fPIC $DINC src/pybind11.cpp -o $OUT
