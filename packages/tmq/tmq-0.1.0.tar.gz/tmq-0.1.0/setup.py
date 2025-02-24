# vim: set ts=4 sw=4 :
# _*_ coding: utf-8 _*_
# Copyright (c) 2025 TMQ Authors
# SPDX-License-Identifier: MPL-2.0

__author__ = 'Martin Wawro'

import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CppExtension, CUDAExtension

class FilteredBuildExtension(BuildExtension):
    def build_extensions(self):
        # First build everything normally
        super().build_extensions()

        # After successful build, remove header files from the build directory
        # This ensures they won't be included in the wheel
        build_lib = os.path.join(self.build_lib, 'tmq')
        if os.path.exists(build_lib):
            for file in os.listdir(build_lib):
                if file.endswith(('.h', '.hpp', '.cu', '.cpp')):
                    os.remove(os.path.join(build_lib, file))


source_dir = os.path.abspath(os.path.join("src", "tmq"))

setup(
    name = "tmq",
    version = "0.1.0",
    author = "Martin Wawro",
    author_email = "martin.wawro@gmail.com",
    packages = ["tmq"],
    package_dir = {"" : "src"},
    description = "Quantization aware machine learning",
    ext_modules = [
        CUDAExtension("tmq.tmq_cuda", [
            "src/tmq/tmq_cuda.cu"
        ]),
        CppExtension("tmq.tmq_native", [
            "src/tmq/tmq_native.cpp"
        ]),
    ],
    cmdclass = { "build_ext" : FilteredBuildExtension },
    python_requires = ">=3.8",
    exclude_package_data = {
        ""    : [ "*.cu", "*.cpp", "*.h" ],
        "tmq" : [ "*.cu", "*.cpp", "*.h" ],
    }
)
