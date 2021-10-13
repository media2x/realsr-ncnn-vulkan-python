%module realsr_ncnn_vulkan_wrapper

%include "cpointer.i"
%include "carrays.i"
%include "std_string.i"
%include "std_wstring.i"
%include "stdint.i"
%include "pybuffer.i"

%pybuffer_mutable_string(unsigned char *d);
%pointer_functions(std::string, str_p);
%pointer_functions(std::wstring, wstr_p);

%{
#include "realsr.h"
#include "realsr_wrapped.h"
%}

class RealSR
{
    public:
        RealSR(int gpuid, bool tta_mode = false);
        ~RealSR();

        // realsr parameters
        int scale;
        int tilesize;
        int prepadding;
};
%include "realsr_wrapped.h"