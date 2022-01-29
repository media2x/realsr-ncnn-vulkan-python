#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmake_build_extension
import pathlib
import setuptools

setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="realsr-ncnn-vulkan-python",
            install_prefix="realsr_ncnn_vulkan_python",
            write_top_level_init="from .realsr_ncnn_vulkan import Realsr",
            source_dir=str(pathlib.Path(__file__).parent / "realsr_ncnn_vulkan_python"),
            cmake_configure_options=[
                "-DBUILD_SHARED_LIBS:BOOL=OFF",
                "-DCALL_FROM_SETUP_PY:BOOL=ON",
            ],
        )
    ],
    cmdclass={"build_ext": cmake_build_extension.BuildExtension},
)
