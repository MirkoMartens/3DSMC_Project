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
CMAKE_SOURCE_DIR = /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build

# Include any dependencies generated for this target.
include CMakeFiles/moreteapots.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/moreteapots.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/moreteapots.dir/flags.make

CMakeFiles/moreteapots.dir/moreteapots.cpp.o: CMakeFiles/moreteapots.dir/flags.make
CMakeFiles/moreteapots.dir/moreteapots.cpp.o: ../moreteapots.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/moreteapots.dir/moreteapots.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/moreteapots.dir/moreteapots.cpp.o -c /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/moreteapots.cpp

CMakeFiles/moreteapots.dir/moreteapots.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/moreteapots.dir/moreteapots.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/moreteapots.cpp > CMakeFiles/moreteapots.dir/moreteapots.cpp.i

CMakeFiles/moreteapots.dir/moreteapots.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/moreteapots.dir/moreteapots.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/moreteapots.cpp -o CMakeFiles/moreteapots.dir/moreteapots.cpp.s

# Object files for target moreteapots
moreteapots_OBJECTS = \
"CMakeFiles/moreteapots.dir/moreteapots.cpp.o"

# External object files for target moreteapots
moreteapots_EXTERNAL_OBJECTS =

moreteapots: CMakeFiles/moreteapots.dir/moreteapots.cpp.o
moreteapots: CMakeFiles/moreteapots.dir/build.make
moreteapots: /usr/lib/x86_64-linux-gnu/libGL.so
moreteapots: /usr/lib/x86_64-linux-gnu/libGLU.so
moreteapots: /usr/lib/x86_64-linux-gnu/libglut.so
moreteapots: /usr/lib/x86_64-linux-gnu/libXmu.so
moreteapots: /usr/lib/x86_64-linux-gnu/libXi.so
moreteapots: /usr/lib/x86_64-linux-gnu/libGL.so
moreteapots: CMakeFiles/moreteapots.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable moreteapots"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/moreteapots.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/moreteapots.dir/build: moreteapots

.PHONY : CMakeFiles/moreteapots.dir/build

CMakeFiles/moreteapots.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/moreteapots.dir/cmake_clean.cmake
.PHONY : CMakeFiles/moreteapots.dir/clean

CMakeFiles/moreteapots.dir/depend:
	cd /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1 /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1 /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build /home/fzemiri/Annee_2/Rendu2/rendu2/TP1/tp1ogl-v2023.1.0-rc1/build/CMakeFiles/moreteapots.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/moreteapots.dir/depend
