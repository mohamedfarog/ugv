cmake_minimum_required(VERSION 3.8)
project(car_gazebo_plugin)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


find_package(gazebo REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(gazebo_ros_pkgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(ackermann_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

add_library(car_gazebo_plugin SHARED src/car_gazebo_plugin.cpp)

# add_executable(cpp_node src/car_gazebo_plugin.cpp)
# ament_target_dependencies(cpp_node rclcpp) 


# add_executable(car_gazebo_plugin src/obstacle_avoidance.cpp)
# ament_target_dependencies(car_gazebo_plugin rclcpp std_msgs)





target_include_directories(car_gazebo_plugin PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

ament_target_dependencies(car_gazebo_plugin
  "gazebo_ros"
  "rclcpp"
  "sensor_msgs"
  "ackermann_msgs"
  "std_msgs"
  "nav_msgs"
  "geometry_msgs"
  "tf2"
  "tf2_ros"
  )

install(TARGETS
  car_gazebo_plugin
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
