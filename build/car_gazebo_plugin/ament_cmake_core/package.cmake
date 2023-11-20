set(_AMENT_PACKAGE_NAME "car_gazebo_plugin")
set(car_gazebo_plugin_VERSION "0.0.0")
set(car_gazebo_plugin_MAINTAINER "farog <eldgeel2000@gmail.com>")
set(car_gazebo_plugin_BUILD_DEPENDS "geometry_msgs" "ackermann_msgs" "nav_msgs" "gazebo_ros" "rclcpp" "sensor_msgs" "std_msgs")
set(car_gazebo_plugin_BUILDTOOL_DEPENDS "ament_cmake")
set(car_gazebo_plugin_BUILD_EXPORT_DEPENDS "ackermann_msgs" "nav_msgs" "gazebo_ros" "rclcpp" "sensor_msgs" "std_msgs")
set(car_gazebo_plugin_BUILDTOOL_EXPORT_DEPENDS )
set(car_gazebo_plugin_EXEC_DEPENDS "ackermann_msgs" "nav_msgs" "gazebo_ros" "rclcpp" "sensor_msgs" "std_msgs")
set(car_gazebo_plugin_TEST_DEPENDS "ament_lint_auto" "ament_lint_common")
set(car_gazebo_plugin_GROUP_DEPENDS )
set(car_gazebo_plugin_MEMBER_OF_GROUPS )
set(car_gazebo_plugin_DEPRECATED "")
set(car_gazebo_plugin_EXPORT_TAGS)
list(APPEND car_gazebo_plugin_EXPORT_TAGS "<build_type>ament_cmake</build_type>")
list(APPEND car_gazebo_plugin_EXPORT_TAGS "<gazebo_ros plugin_path=\"${prefix}\"/>")
