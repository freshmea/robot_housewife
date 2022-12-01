cmake_minimum_required(VERSION 3.5)
project(hansu_cam)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Emulate colcon by providing paths to other projects in the workspace
if ($ENV{CLION_IDE})
  message(STATUS "Running inside CLion")
  find_package(fastrtps_cmake_module REQUIRED)
  set(FastRTPS_INCLUDE_DIR "/opt/ros/foxy/include")
  set(FastRTPS_LIBRARY_RELEASE "/opt/ros/foxy/lib/libfastrtps.so")
  set(ros2_shared_DIR "${PROJECT_SOURCE_DIR}/../../../install/ros2_shared/share/ros2_shared/cmake")
endif ()

# Try for OpenCV 4.X, but settle for whatever is installed
find_package(OpenCV 4 QUIET)
if (NOT OpenCV_FOUND)
  find_package(OpenCV REQUIRED)
endif ()
message(STATUS "Found OpenCV version ${OpenCV_VERSION}")

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(camera_calibration_parsers REQUIRED)
find_package(class_loader REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(ros2_shared REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)



# Package includes not needed for CMake >= 2.8.11
include_directories(
  include
  ${ros2_shared_INCLUDE_DIRS}
)

set(node_plugins "")

add_executable(hansu_cam src/stereo_camera.cpp)
ament_target_dependencies(hansu_cam rclcpp std_msgs)

#=============
# OpenCV camera node
#=============

add_library(
  opencv_cam_node SHARED
  src/opencv_cam_node.cpp
)
target_compile_definitions(
  opencv_cam_node
  PRIVATE "COMPOSITION_BUILDING_DLL"
)
ament_target_dependencies(
  opencv_cam_node
  camera_calibration_parsers
  class_loader
  OpenCV
  rclcpp
  rclcpp_components
  sensor_msgs
)
rclcpp_components_register_nodes(opencv_cam_node "opencv_cam::OpencvCamNode")
set(node_plugins "${node_plugins}opencv_cam::OpencvCamNode;$<TARGET_FILE:opencv_cam_node>\n")

#=============
# Test subscriber node
#=============

add_library(
  subscriber_node SHARED
  src/subscriber_node.cpp
)
target_compile_definitions(
  subscriber_node
  PRIVATE "COMPOSITION_BUILDING_DLL"
)
ament_target_dependencies(
  subscriber_node
  class_loader
  rclcpp
  rclcpp_components
  sensor_msgs
)
rclcpp_components_register_nodes(subscriber_node "opencv_cam::ImageSubscriberNode")
set(node_plugins "${node_plugins}opencv_cam::ImageSubscriberNode;$<TARGET_FILE:subscriber_node>\n")

#=============
# OpenCV camera main, IPC=true
#=============

add_executable(
  opencv_cam_main
  src/opencv_cam_main.cpp
)
target_link_libraries(
  opencv_cam_main
  opencv_cam_node
)
ament_target_dependencies(
  opencv_cam_main
  rclcpp
)

#=============
# Manual composition of camera and subscriber nodes, IPC=true
#=============

add_executable(
  ipc_test_main
  src/ipc_test_main.cpp
)
target_link_libraries(
  ipc_test_main
  opencv_cam_node
  subscriber_node
)
ament_target_dependencies(
  ipc_test_main
  rclcpp
)
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

#=============
# Export
# Best practice, see https://discourse.ros.org/t/ament-best-practice-for-sharing-libraries/3602
#=============

ament_export_dependencies(class_loader)

ament_export_include_directories(include)

ament_package()




install(
TARGETS hansu_cam
    DESTINATION lib/${PROJECT_NAME})
