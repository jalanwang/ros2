# ~/robot/robot_ws/src/my_move_turtle_pkg/launch/turtlesim_and_teleop.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                namespace= "turtlesim", package='turtlesim',
                executable='turtlesim_node', output='screen'),
            Node(
                namespace= "pub_cmd_vel", package='my_move_turtle_pkg',
                executable='move_turtle', output='screen'),
        ]
    )
