import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from rclpy.qos import QoSProfile

class RealTimePub(Node): # 클래스 네이밍 컨벤션(PascalCase) 적용
    def __init__(self):
        super().__init__('time_publisher')
        # QoS 프로필 설정
        self.qos_profile = QoSProfile(depth=10)

        # Publisher 생성 (오타 수정: massage -> message)
        self.message_publisher = self.create_publisher(Header, 'time', self.qos_profile)

        # 1초 주기로 타이머 실행
        self.timer = self.create_timer(1.0, self.publish_time_msg)

    def publish_time_msg(self):
        msg = Header()
        # ROS 2 시스템 시간을 Header 메시지의 stamp에 할당
        now = self.get_clock().now()
        msg.stamp = now.to_msg()

        self.message_publisher.publish(msg)

        # 로그 출력 최적화
        sec, nanosec = now.seconds_nanoseconds()
        self.get_logger().info(f'Published Stamp: sec={sec}, nanosec={nanosec}')

def main(args=None):
    rclpy.init(args=args)
    node = RealTimePub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__': # 언더바 오타 수정
    main()
