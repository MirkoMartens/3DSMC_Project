#define CV_CPU_SIMD_FILENAME "/home/jeanjean/Documents/3dProject/3DSMC_Project/test/include/opencv-4.9.0/modules/core/test/test_intrin512.simd.hpp"
#define CV_CPU_DISPATCH_MODE AVX512_SKX
#include "opencv2/core/private/cv_cpu_include_simd_declarations.hpp"

#define CV_CPU_DISPATCH_MODES_ALL AVX512_SKX, BASELINE

#undef CV_CPU_SIMD_FILENAME
