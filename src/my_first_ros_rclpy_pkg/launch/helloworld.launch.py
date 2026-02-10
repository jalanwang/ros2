# ~/robot_ws/src/my_first_ros_rclpy_pkg/launch/helloworld.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. HelloWorld Publisher 실행
        Node(
            package='my_first_ros_rclpy_pkg', # 네 패키지 이름
            executable='helloworld_publisher', # setup.py에 등록한 실행 이름
            name='publisher_node'
        ),
        # 2. HelloWorld Subscriber 실행
        Node(
            package='my_first_ros_rclpy_pkg',
            executable='helloworld_subscriber',
            name='subscriber_node',
            output='screen' # 터미널에 로그를 출력하기 위해 설정
        ),
    ])
