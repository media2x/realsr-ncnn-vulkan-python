# RealSR ncnn Vulkan Python

## Introduction
[realsr-ncnn-vulkan](https://github.com/nihui/realsr-ncnn-vulkan) is nihui's ncnn implementation of Real-World Super-Resolution via Kernel Estimation and Noise Injection super resolution.

realsr-ncnn-vulkan-python wraps [realsr-ncnn-vulkan project](https://github.com/nihui/realsr-ncnn-vulkan) by SWIG to make it easier to integrate realsr-ncnn-vulkan with existing python projects.

## Downloads

Linux/Windos/Mac X86_64 build releases are available now.

However, for Linux distro with GLIBC < 2.29 (like Ubuntu 18.04), the ubuntu-1804 pre-built should be used.

## Build

First, you have to install python, python development package (Python native development libs in Visual Studio), vulkan SDK and SWIG on your platform. And then:

### Linux
```shell
git clone https://github.com/ArchieMeng/realsr-ncnn-vulkan-python.git
cd realsr-ncnn-vulkan-python
git submodule update --init --recursive
cmake -B build src
cd build
make
```

### Windows
I used Visual Studio 2019 and msvc v142 to build this project for Windows.

Install visual studio and open the project directory, and build. Job done.

The only problem on Windows is that, you cannot use [CMake for Windows](https://cmake.org/download/) to generate the Visual Studio solution file and build it. This will make the lib crash on loading.

The only way is [use Visual Studio to open the project as directory](https://www.microfocus.com/documentation/visual-cobol/vc50/VS2019/GUID-BE1C48AA-DB22-4F38-9644-E9B48658EF36.html), and build it from Visual Studio.

## About RealSR

Real-World Super-Resolution via Kernel Estimation and Noise Injection (CVPRW 2020)

https://github.com/jixiaozhong/RealSR

Xiaozhong Ji, Yun Cao, Ying Tai, Chengjie Wang, Jilin Li, and Feiyue Huang

*Tencent YouTu Lab*

Our solution is the **winner of CVPR NTIRE 2020 Challenge on Real-World Super-Resolution** in both tracks.

https://arxiv.org/abs/2005.01996

## Usages

### Example Program

```Python
from PIL import Image
from realsr_ncnn_vulkan import RealSR
# if installed from pypi or binary wheels,
# from realsr_ncnn_vulkan_python import RealSR

im = Image.open("0.png")
upscaler = RealSR(0, scale=4)
out_im = upscaler.process(im)
out_im.save("temp.png")
```

If you encounter crash or error, try to upgrade your GPU driver

- Intel: https://downloadcenter.intel.com/product/80939/Graphics-Drivers
- AMD: https://www.amd.com/en/support
- NVIDIA: https://www.nvidia.com/Download/index.aspx

## Original RealSR NCNN Vulkan Project

- https://github.com/nihui/realsr-ncnn-vulkan

## Original RealSR Project

- https://github.com/jixiaozhong/RealSR

## Other Open-Source Code Used

- https://github.com/Tencent/ncnn for fast neural network inference on ALL PLATFORMS
- https://github.com/webmproject/libwebp for encoding and decoding Webp images on ALL PLATFORMS
- https://github.com/nothings/stb for decoding and encoding image on Linux / MacOS
- https://github.com/tronkko/dirent for listing files in directory on Windows
