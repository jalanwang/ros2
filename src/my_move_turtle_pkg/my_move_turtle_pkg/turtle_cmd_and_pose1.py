# ROS2 Python 라이브러리 임포트
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose  # Turtlesim의 Pose 메시지 타입
from my_first_package_msgs.msg import CmdAndPoseVel  # 커스텀 메시지 타입

class CmdAndPose(Node):
    """
    Turtlesim의 위치 정보를 구독하는 노드 클래스
    """

    def __init__(self):
        # 노드 초기화: 노드 이름은 'turtle_cmd_pose'
        super().__init__('turtle_cmd_pose')

        # Pose 메시지를 받는 Subscriber 생성
        # 토픽: /turtle1/pose, 콜백 함수: callback_pose, 큐 크기: 10
        self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.callback_pose, 10)
        self.cmd_pose = CmdAndPoseVel()

    def callback_pose(self, msg):
        self.cmd_pose.pose_x = msg.x
        self.cmd_pose.pose_y = msg.y
        self.cmd_pose.linear_vel = msg.linear_velocity
        self.cmd_pose.angular_vel = msg.angular_velocity
        #print(msg)  # 받은 Pose 메시지 출력
        print(self.cmd_pose) # 받은 CmdAndPoseVel 메시지 출력

def main(args=None):
    # ROS2 Python 클라이언트 라이브러리 초기화
    rclpy.init(args=args)

    # CmdAndPose 노드 인스턴스 생성
    node = CmdAndPose()

    try:
        # 노드 실행 (콜백 함수들이 호출될 수 있도록 대기)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시 로그 출력
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        # 노드 종료 처리
        node.destroy_node()
        # ROS2 종료
        rclpy.shutdown()


# 스크립트가 직접 실행될 때만 main() 함수 호출
if __name__ == '__main__':
    main()
