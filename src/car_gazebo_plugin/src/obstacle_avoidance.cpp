#include "rclcpp/rclcpp.hpp"              // ROS Core Libraries

#include "geometry_msgs/msg/twist.hpp"    // Twist
#include "sensor_msgs/msg/laser_scan.hpp" // Laser Scan

using std::placeholders::_1;

class ObstacleAvoidance : public rclcpp::Node
{
    public:
    ObstacleAvoidance() : Node("obstacle_avoidance") {
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

      auto node = rclcpp::Node::make_shared("obstacle_avoidance");
      auto default_qos = rclcpp::QoS(rclcpp::SystemDefaultsQoS());
      node->create_subscription<sensor_msgs::msg::LaserScan>(
      "/scan",default_qos,
        std::bind(&ObstacleAvoidance::topic_callback, this, _1));
   }

    private:
    void topic_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
        int distToObstacle = 1;
        auto move = geometry_msgs::msg::Twist();

        if(msg->ranges[300] > distToObstacle) {
            move.linear.x = 0.5;
            move.angular.z = 0.0;
            publisher_->publish(move);
        }

        if(msg->ranges[300] <= distToObstacle) {
            move.linear.x = 0.5;
            move.angular.z = 3.5;
            publisher_->publish(move); 
        }  
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  
  rclcpp::spin(std::make_shared<ObstacleAvoidance>());
  rclcpp::shutdown();
  return 0;
}