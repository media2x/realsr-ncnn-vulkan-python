import sys
from math import floor
from pathlib import Path

from PIL import Image

if __package__:
    import importlib

    raw = importlib.import_module(f"{__package__}.realsr_ncnn_vulkan_wrapper")
else:
    import realsr_ncnn_vulkan_wrapper as raw


class RealSR:
    def __init__(
            self,
            gpuid=0,
            model="models-DF2K",
            tta_mode=False,
            scale: float = 4,
            tilesize=0,
    ):
        """
        RealSR class which can do image super resolution.

        :param gpuid: the id of the gpu device to use.
        :param model: the name or the path to the model
        :param tta_mode: whether to enable tta mode or not
        :param scale: scale ratio. value: float. default: 2
        :param tilesize: tile size. 0 for automatically setting the size. default: 0
        """
        self._raw_realsr = raw.RealSRWrapped(gpuid, tta_mode)
        self.model = model
        self.gpuid = gpuid
        self.scale = scale  # the real scale ratio
        self.set_params(scale, tilesize)
        self.load()

    def set_params(self, scale=4., tilesize=0):
        """
        set parameters for realsr object

        :param scale: 1/2. default: 2
        :param tilesize: default: 0
        :return: None
        """
        self._raw_realsr.scale = 4  # control the real scale ratio at each raw process function call
        self._raw_realsr.tilesize = self.get_tilesize() if tilesize <= 0 else tilesize
        self._raw_realsr.prepadding = self.get_prepadding()

    def load(self, parampath: str = "", modelpath: str = "") -> None:
        """
        Load models from given paths. Use self.model if one or all of the parameters are not given.

        :param parampath: the path to model params. usually ended with ".param"
        :param modelpath: the path to model bin. usually ended with ".bin"
        :return: None
        """
        if not parampath or not modelpath:
            model_dir = Path(self.model)
            if not model_dir.is_absolute():
                if (
                        not model_dir.is_dir()
                ):  # try to load it from module path if not exists as directory
                    dir_path = Path(__file__).parent
                    model_dir = dir_path.joinpath("models", self.model)

            if self._raw_realsr.scale == 4:
                parampath = model_dir.joinpath("x4.param")
                modelpath = model_dir.joinpath("x4.bin")

        if Path(parampath).exists() and Path(modelpath).exists():
            parampath_str, modelpath_str = raw.StringType(), raw.StringType()
            if sys.platform in ("win32", "cygwin"):
                parampath_str.wstr = raw.new_wstr_p()
                raw.wstr_p_assign(parampath_str.wstr, str(parampath))
                modelpath_str.wstr = raw.new_wstr_p()
                raw.wstr_p_assign(modelpath_str.wstr, str(modelpath))
            else:
                parampath_str.str = raw.new_str_p()
                raw.str_p_assign(parampath_str.str, str(parampath))
                modelpath_str.str = raw.new_str_p()
                raw.str_p_assign(modelpath_str.str, str(modelpath))

            self._raw_realsr.load(parampath_str, modelpath_str)
        else:
            raise FileNotFoundError(f"{parampath} or {modelpath} not found")

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
            w, h = floor(w * self.scale), floor(h * self.scale)
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

        raw_in_image = raw.Image(in_bytes, im.width, im.height, channels)
        raw_out_image = raw.Image(
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
        heap_budget = raw.get_heap_budget(self.gpuid)
        if self.model.find("models-DF2K") or self.model.find("models-DF2K_JPEG"):
            if heap_budget > 1900:
                return 200
            elif heap_budget > 550:
                return 100
            elif heap_budget > 190:
                return 64
            else:
                return 32
        else:
            raise NotImplementedError(f'model "{self.model}" is not supported')


if __name__ == "__main__":
    from time import time

    t = time()
    im = Image.open("../images/0.png")
    upscaler = RealSR(0)
    out_im = upscaler.process(im)
    out_im.save("temp.png")
    print(f"Elapsed time: {time() - t}s")
