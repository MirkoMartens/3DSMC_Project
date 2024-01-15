

project(Test)

#set you dir to OpenCV
set(OpenCV_dir "include/opencv-4.9.0" )

set(OpenCV_dir $(OpenCV_dir))
find_package(OpenCV REQUIRED)

add_executable(Test main.cpp)

#set your OpenCV lib file in case it doesn't work
#set(OpenCV_LIBS opencv_core opencv_imgproc opencv_highgui opencv_imgcodecs)

target_link_libraries(Test ${OpenCV_LIBS})