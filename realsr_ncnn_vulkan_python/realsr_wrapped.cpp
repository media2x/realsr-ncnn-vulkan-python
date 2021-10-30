//
// Created by archiemeng on 29/3/21.
//
#include "realsr_wrapped.h"

RealSRWrapped::RealSRWrapped(int gpuid, bool tta_mode) : RealSR(gpuid, tta_mode) {}

int RealSRWrapped::load(const StringType &parampath, const StringType &modelpath) {
#if _WIN32
    return RealSR::load(*parampath.wstr, *modelpath.wstr);
#else
    return RealSR::load(*parampath.str, *modelpath.str);
#endif
}

int RealSRWrapped::process(const Image &inimage, Image outimage) {
    int c = inimage.elempack;
    ncnn::Mat inimagemat = ncnn::Mat(inimage.w, inimage.h, (void*) inimage.data, (size_t) c, c);
    ncnn::Mat outimagemat = ncnn::Mat(outimage.w, outimage.h, (void*) outimage.data, (size_t) c, c);
    return RealSR::process(inimagemat, outimagemat);
};

uint32_t get_heap_budget(int gpuid) {
    return ncnn::get_gpu_device(gpuid)->get_heap_budget();
}

int get_gpu_count() {
    return ncnn::get_gpu_count();
}
