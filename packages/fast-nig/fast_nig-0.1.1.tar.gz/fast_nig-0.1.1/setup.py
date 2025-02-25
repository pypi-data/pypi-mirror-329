import os
import sys

import pybind11
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Paths for Boost and OpenMP on macOS (via Homebrew)
boost_include_dir = "/opt/homebrew/opt/boost/include"
omp_include_dir = "/opt/homebrew/opt/libomp/include"

ext_modules = [
    Extension(
        "fast_nig",
        ["src/nig.cpp"],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True),
            boost_include_dir,
            omp_include_dir,
        ],
        language="c++",
        extra_compile_args=["-std=c++17", "-Xpreprocessor", "-fopenmp"],
        extra_link_args=["-lomp", "-L/opt/homebrew/opt/libomp/lib"],
    ),
]

setup(
    name="fast_nig",
    version="0.1.1",
    author="YBaumann",
    author_email="baumann@swissquant.com",
    description="NIG distribution with PPF approximations using cubic spline and pybind11",
    ext_modules=ext_modules,
    setup_requires=["pybind11>=2.6.0", "numpy"],
    install_requires=["pybind11>=2.6.0", "numpy"],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
