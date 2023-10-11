#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/range.hpp"

class ObstacleAvoider : public rclcpp::Node {
public:
  explicit ObstacleAvoider();

private:
  void leftSensorCallback(const sensor_msgs::msg::Range::SharedPtr msg);
  void rightSensorCallback(const sensor_msgs::msg::Range::SharedPtr msg);

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr range1_sub_;
  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr range2_sub_;

  double range1_value{0.0};
  double range2_value{0.0};
};