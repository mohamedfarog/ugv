#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import signal

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration


from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from nav2_common.launch import RewrittenYaml

use_sim_time = LaunchConfiguration('use_sim_time')

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_sim_car = get_package_share_directory('my_robot_bringup')

    bringup_dir = get_package_share_directory('my_robot_bringup')
    launch_dir = os.path.join(bringup_dir, 'launch')
    world_config = DeclareLaunchArgument(
          'world',
          default_value=[os.path.join(pkg_sim_car, 'worlds', 'nav3.world'), ''],
          description='Dae world file')
    
    # Specify the actions

    rviz_config_path = os.path.join(pkg_sim_car, 'config', 'red-crash.rviz')
    start_rviz2_cmd = ExecuteProcess(
        cmd=['rviz2', '--display-config', rviz_config_path],
        cwd=[launch_dir],
        output='screen')

    # rviz_config_path = os.path.join(pkg_sim_car, 'rviz', 'urdf_config.rviz')
    # start_rviz2_cmd = ExecuteProcess(
    #     cmd=['rviz2', '--display-config', rviz_config_path],
    #     cwd=[launch_dir],
    #     output='screen')

    static_map_path = os.path.join(pkg_sim_car, 'maps', 'map1.yaml')

    bringup_dir = get_package_share_directory('nav2_bringup')
    bringup_launch_dir = os.path.join(bringup_dir, 'launch')


    nav2_params_path = os.path.join(
        get_package_share_directory('my_robot_bringup'),
        'config',
        'nav2_params1.yaml')


    behavior_tree_path = os.path.join(
        get_package_share_directory('my_robot_bringup'),
        'behavior_trees',
        'navigate_w_replanning_time2.xml')

    configured_nav2_params = RewrittenYaml(
        source_file=nav2_params_path,
        param_rewrites={'default_nav_to_pose_bt_xml': behavior_tree_path},
        convert_types=True)
    
    declare_map_yaml_cmd = DeclareLaunchArgument(
    name='map',
    default_value=static_map_path,
    description='Full path to map file to load')

    nav_bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(bringup_launch_dir, 'bringup_launch.py')),
        launch_arguments={
            'slam': "1",
            'map': 'map.yaml',
            'params_file': configured_nav2_params,
        }.items()
    )

    # # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )

    car = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            # os.path.join(pkg_sim_car, 'launch', 'spawn_red_crash.launch.py'),
            os.path.join(pkg_sim_car, 'launch', 'spawn_car.launch.py'),
        )
    )
    declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='true',
    description='Use simulation (Gazebo) clock if true')


    joy = Node(
            package='joy', executable='joy_node', output='screen')
    teleop_twist = Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            output='screen',
            parameters=[os.path.join(pkg_sim_car, "config", "teleop_twist_joy.yaml")])
    
    map_server_config_path = os.path.join(
    get_package_share_directory('my_robot_bringup'),
    'maps',
    'map1.yaml'
)
    map_server_cmd = Node(
    package='nav2_map_server',
    executable='map_server',
    output='screen',
    parameters=[{'yaml_filename': map_server_config_path}])

    lifecycle_nodes = ['map_server']
    use_sim_time = True
    autostart = True


    start_lifecycle_manager_cmd = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        emulate_tty=True, # https://github.com/ros2/launch/issues/188
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': autostart},
                    {'node_names': lifecycle_nodes}])


    ld = LaunchDescription()

    ld.add_action(map_server_cmd)
    ld.add_action(start_lifecycle_manager_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(world_config)
    ld.add_action(gazebo)

    # ld.add_action(start_gazebo_server_cmd)
    # ld.add_action(start_gazebo_client_cmd)
    ld.add_action(TimerAction(
            period=5.0,
            actions=[start_rviz2_cmd]))
    ld.add_action(car)
    ld.add_action(joy)
    ld.add_action(teleop_twist)
    # ld.add_action(nav_bringup_cmd)
    ld.add_action(declare_use_sim_time_cmd)




    ld.add_action(TimerAction(
            period=0.0,
            actions=[nav_bringup_cmd]))
    return ld