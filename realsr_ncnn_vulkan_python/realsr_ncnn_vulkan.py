#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RealSR ncnn Vulkan Python wrapper
Author: ArchieMeng
Date Created: February 4, 2021
Last Modified: February 13, 2022

Dev: K4YT3X
Last Modified: February 13, 2022
"""

# built-in imports
import importlib
import math
import pathlib
import sys

# third-party imports
from PIL import Image

# local imports
if __package__ is None:
    import realsr_ncnn_vulkan_wrapper as wrapped
else:
    wrapped = importlib.import_module(f"{__package__}.realsr_ncnn_vulkan_wrapper")


class Realsr:
    def __init__(
        self,
        gpuid=0,
        model="models-DF2K",
        tta_mode=False,
        scale: float = 4,
        tilesize=0,
        num_threads=1,
        **_kwargs,
    ):
        """
        RealSR class which can do image super resolution.

        :param gpuid: the id of the gpu device to use.
        :param model: the name or the path to the model
        :param tta_mode: whether to enable tta mode or not
        :param scale: scale ratio. value: float. default: 2
        :param tilesize: tile size. 0 for automatically setting the size. default: 0
        :param num_threads: number of threads. default: 1
        """
        self._raw_realsr = wrapped.RealSRWrapped(gpuid, tta_mode, num_threads)
        self.model = model
        self.gpuid = gpuid
        self.scale = scale  # the real scale ratio
        self.set_params(scale, tilesize)
        self.load()

    def set_params(self, scale=4.0, tilesize=0):
        """
        set parameters for realsr object

        :param scale: 1/2. default: 2
        :param tilesize: default: 0
        :return: None
        """
        self._raw_realsr.scale = (
            4  # control the real scale ratio at each raw process function call
        )
        self._raw_realsr.tilesize = self.get_tilesize() if tilesize <= 0 else tilesize
        self._raw_realsr.prepadding = self.get_prepadding()

    def load(
        self, param_path: pathlib.Path = None, model_path: pathlib.Path = None
    ) -> None:
        """
        Load models from given paths. Use self.model if one or all of the parameters are not given.

        :param param_path: the path to model params. usually ended with ".param"
        :param model_path: the path to model bin. usually ended with ".bin"
        :return: None
        """
        if param_path is None or model_path is None:
            model_dir = pathlib.Path(self.model)

            # try to load it from module path if not exists as directory
            if not model_dir.is_dir():
                model_dir = pathlib.Path(__file__).parent / "models" / self.model

            param_path = model_dir / f"x{self._raw_realsr.scale}.param"
            model_path = model_dir / f"x{self._raw_realsr.scale}.bin"

        if param_path.exists() and model_path.exists():
            param_path_str, model_path_str = wrapped.StringType(), wrapped.StringType()
            if sys.platform in ("win32", "cygwin"):
                param_path_str.wstr = wrapped.new_wstr_p()
                wrapped.wstr_p_assign(param_path_str.wstr, str(param_path))
                model_path_str.wstr = wrapped.new_wstr_p()
                wrapped.wstr_p_assign(model_path_str.wstr, str(model_path))
            else:
                param_path_str.str = wrapped.new_str_p()
                wrapped.str_p_assign(param_path_str.str, str(param_path))
                model_path_str.str = wrapped.new_str_p()
                wrapped.str_p_assign(model_path_str.str, str(model_path))

            self._raw_realsr.load(param_path_str, model_path_str)
        else:
            raise FileNotFoundError(f"{param_path} or {model_path} not found")

    def process(self, im: Image) -> Image:
        """
        Upscale the given PIL.Image, and will call RealSR.process() more than once for scale ratios greater than 4

        :param im: PIL.Image
        :return: PIL.Image
        """
        if self.scale > 1:
            cur_scale = 1
            w, h = im.size
            while cur_scale < self.scale:
                im = self._process(im)
                cur_scale *= 4
            w, h = math.floor(w * self.scale), math.floor(h * self.scale)
            im = im.resize((w, h))

        return im

    def _process(self, im: Image) -> Image:
        """
        Call RealSR.process() once for the given PIL.Image

        :param im: PIL.Image
        :return: PIL.Image
        """
        in_bytes = bytearray(im.tobytes())
        channels = int(len(in_bytes) / (im.width * im.height))
        out_bytes = bytearray((self._raw_realsr.scale ** 2) * len(in_bytes))

        raw_in_image = wrapped.Image(in_bytes, im.width, im.height, channels)
        raw_out_image = wrapped.Image(
            out_bytes,
            self._raw_realsr.scale * im.width,
            self._raw_realsr.scale * im.height,
            channels,
        )

        self._raw_realsr.process(raw_in_image, raw_out_image)

        return Image.frombytes(
            im.mode,
            (self._raw_realsr.scale * im.width, self._raw_realsr.scale * im.height),
            bytes(out_bytes),
        )

    def get_prepadding(self) -> int:
        if self.model.find("models-DF2K") or self.model.find("models-DF2K_JPEG"):
            return 10
        else:
            raise NotImplementedError(f'model "{self.model}" is not supported')

    def get_tilesize(self):
        if self.model.find("models-DF2K") or self.model.find("models-DF2K_JPEG"):
            if self.gpuid >= 0:
                heap_budget = wrapped.get_heap_budget(self.gpuid)
                if heap_budget > 1900:
                    return 200
                elif heap_budget > 550:
                    return 100
                elif heap_budget > 190:
                    return 64
                else:
                    return 32
            else:
                return 200
        else:
            raise NotImplementedError(f'model "{self.model}" is not supported')


class RealSR(Realsr):
    ...
