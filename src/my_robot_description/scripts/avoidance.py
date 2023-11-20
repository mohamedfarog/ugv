#! /usr/bin/env python3

import rclpy 
from rclpy.node import Node 
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist

distToObstacle = 10

class ObstacleAvoidance(Node):
        def __init__(self):
            super().__init__('obstacle_avoidance')
            self.sub = self.create_subscription(LaserScan, '/scan', self.obstacle_callback, 10)
            self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        def obstacle_callback(self, msg):
            # self.get_logger().info('The distance to obstacle is %s ' % msg.ranges[135])

            move = Twist()

            if msg.ranges[135] > 13.0:
                move.linear.x = 0.5
                move.angular.z = 0.0
                print('Moving forward', msg.ranges[300])
            
            if msg.ranges[135] < 13.0:
                move.linear.x = 0.0
                move.angular.z = 0.0  
            self.pub.publish(move)

def main(args=None):

        rclpy.init(args=args)

        obstacle_avoidance = ObstacleAvoidance()

        rclpy.spin(obstacle_avoidance)

        obstacle_avoidance.destroy_node()

        rclpy.shutdown()

if __name__ == '__main__':
        main()