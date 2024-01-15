#define CV_CPU_SIMD_FILENAME "/home/jeanjean/Documents/3dProject/3DSMC_Project/test/include/opencv-4.9.0/modules/gapi/src/backends/fluid/gfluidimgproc_func.simd.hpp"
#define CV_CPU_DISPATCH_MODE SSE4_1
#include "opencv2/core/private/cv_cpu_include_simd_declarations.hpp"

#define CV_CPU_DISPATCH_MODE AVX2
#include "opencv2/core/private/cv_cpu_include_simd_declarations.hpp"

#define CV_CPU_DISPATCH_MODES_ALL AVX2, SSE4_1, BASELINE

#undef CV_CPU_SIMD_FILENAME
