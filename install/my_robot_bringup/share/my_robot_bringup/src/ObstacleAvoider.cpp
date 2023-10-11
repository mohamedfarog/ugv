#include "ObstacleAvoider.hpp"

#define MAX_RANGE 0.15

ObstacleAvoider::ObstacleAvoider() : Node("obstacle_avoider") {
  publisher_ = create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 1);

  range1_sub_ = create_subscription<sensor_msgs::msg::Range>(
      "/range1", 1,
      std::bind(&ObstacleAvoider::leftSensorCallback, this,
                std::placeholders::_1));

  range2_sub_ = create_subscription<sensor_msgs::msg::Range>(
      "/range2", 1,
      std::bind(&ObstacleAvoider::rightSensorCallback, this,
                std::placeholders::_1));
}

void ObstacleAvoider::leftSensorCallback(
    const sensor_msgs::msg::Range::SharedPtr msg) {
 range1_value = msg->range;
}

void ObstacleAvoider::rightSensorCallback(
    const sensor_msgs::msg::Range::SharedPtr msg) {
  range2_value = msg->range;

  auto command_message = std::make_unique<geometry_msgs::msg::Twist>();

  command_message->linear.x = 0.1;

  if (range1_value < 0.9 * MAX_RANGE ||
      range2_value < 0.9 * MAX_RANGE) {
    command_message->angular.z = -2.0;
  }

  publisher_->publish(std::move(command_message));
}

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  auto avoider = std::make_shared<ObstacleAvoider>();
  rclcpp::spin(avoider);
  rclcpp::shutdown();
  return 0;
}