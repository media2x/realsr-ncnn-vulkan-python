#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
from realsr_ncnn_vulkan_python import Realsr
import time

start_time = time.time()
input_image = Image.open("input.png")
upscaler = Realsr(0)
output_image = upscaler.process(input_image)
output_image.save("output.png")
print(f"Elapsed time: {time.time() - start_time} secs")
