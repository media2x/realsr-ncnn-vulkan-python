#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import setuptools

import cmake_build_extension

cmake_flags = [
    "-DBUILD_SHARED_LIBS:BOOL=OFF",
    "-DCALL_FROM_SETUP_PY:BOOL=ON",
]
if "CMAKE_FLAGS" in os.environ:
    flags = os.environ["CMAKE_FLAGS"]
    cmake_flags.extend(flags.split())

setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="realsr-ncnn-vulkan-python",
            install_prefix="realsr_ncnn_vulkan_python",
            write_top_level_init="from .realsr_ncnn_vulkan import Realsr, RealSR, wrapped",
            source_dir=str(pathlib.Path(__file__).parent / "realsr_ncnn_vulkan_python"),
            cmake_configure_options=cmake_flags,
        )
    ],
    cmdclass={"build_ext": cmake_build_extension.BuildExtension},
)
