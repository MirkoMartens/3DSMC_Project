# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/fzemiri/Annee_2/Rendu2/rendu2/TP3

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build

# Include any dependencies generated for this target.
include CMakeFiles/robot.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/robot.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/robot.dir/flags.make

CMakeFiles/robot.dir/robot.cpp.o: CMakeFiles/robot.dir/flags.make
CMakeFiles/robot.dir/robot.cpp.o: ../robot.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/robot.dir/robot.cpp.o"
	/mnt/n7fs/ens/tp_cregut/gnat/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/robot.dir/robot.cpp.o -c /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/robot.cpp

CMakeFiles/robot.dir/robot.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/robot.dir/robot.cpp.i"
	/mnt/n7fs/ens/tp_cregut/gnat/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/robot.cpp > CMakeFiles/robot.dir/robot.cpp.i

CMakeFiles/robot.dir/robot.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/robot.dir/robot.cpp.s"
	/mnt/n7fs/ens/tp_cregut/gnat/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/robot.cpp -o CMakeFiles/robot.dir/robot.cpp.s

# Object files for target robot
robot_OBJECTS = \
"CMakeFiles/robot.dir/robot.cpp.o"

# External object files for target robot
robot_EXTERNAL_OBJECTS =

robot: CMakeFiles/robot.dir/robot.cpp.o
robot: CMakeFiles/robot.dir/build.make
robot: /usr/lib/x86_64-linux-gnu/libGLU.so
robot: /usr/lib/x86_64-linux-gnu/libglut.so
robot: /usr/lib/x86_64-linux-gnu/libGLX.so
robot: /usr/lib/x86_64-linux-gnu/libOpenGL.so
robot: /usr/lib/x86_64-linux-gnu/libXmu.so
robot: /usr/lib/x86_64-linux-gnu/libXi.so
robot: CMakeFiles/robot.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable robot"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/robot.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/robot.dir/build: robot

.PHONY : CMakeFiles/robot.dir/build

CMakeFiles/robot.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/robot.dir/cmake_clean.cmake
.PHONY : CMakeFiles/robot.dir/clean

CMakeFiles/robot.dir/depend:
	cd /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/fzemiri/Annee_2/Rendu2/rendu2/TP3 /home/fzemiri/Annee_2/Rendu2/rendu2/TP3 /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build /home/fzemiri/Annee_2/Rendu2/rendu2/TP3/build/CMakeFiles/robot.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/robot.dir/depend

