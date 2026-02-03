import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro # Xacro 파일을 처리하기 위해 반드시 필요

def generate_launch_description():
    # 1. 시뮬레이션 시간 사용 여부 설정 (Gazebo 등과 연동 시 중요)
    use_sim_time = LaunchConfiguration("use_sim_time")

    # 2. 패키지 경로 및 파일 경로 설정
    # urdf_tutorial 패키지의 설치된 공유 디렉토리 경로를 가져옴
    pkg_path = os.path.join(get_package_share_directory("urdf_tutorial"))
    xacro_file = os.path.join(pkg_path, "urdf", "robot_1.xacro")

    # 3. Xacro 변환 (핵심!)
    # .xacro 파일을 읽어서 순수한 XML(URDF) 형태의 데이터로 변환함
    robot_description = xacro.process_file(xacro_file)

    # 4. 노드에 전달할 파라미터 묶음
    # 변환된 URDF 데이터(.toxml())를 'robot_description'이라는 이름의 파라미터로 저장
    params = {"robot_description": robot_description.toxml(), "use_sim_time": use_sim_time}

    return LaunchDescription(
        [
            # 5. 런치 실행 시 인자를 받을 수 있게 선언 (기본값 false)
            DeclareLaunchArgument(
                "use_sim_time", default_value="false", description="use sim time"
            ),

            # 6. robot_state_publisher 노드 실행
            # 로봇의 URDF 정보를 읽어 TF(좌표계 변환) 데이터를 계산하고 발행하는 역할
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[params], # 위에서 만든 파라미터를 노드에 주입
            ),
        ]
    )
