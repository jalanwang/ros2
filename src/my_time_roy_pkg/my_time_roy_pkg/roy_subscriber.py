import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Header
from rclpy.qos import QoSProfile

class MessageSubscriber(Node): # 클래스 이름 오타 수정
    def __init__(self):
        super().__init__('message_time_subscriber')
        self.qos_profile = QoSProfile(depth=10)

        # String 타입 구독
        self.string_sub = self.create_subscription(
            String,
            'message', # 퍼블리셔 측 토픽 이름과 맞출 것
            self.message_callback,
            self.qos_profile)

        # Header 타입 구독
        self.time_sub = self.create_subscription(
            Header,
            'time',
            self.time_callback,
            self.qos_profile)

    def message_callback(self, msg):
        self.get_logger().info(f'Received String: "{msg.data}"')

    def time_callback(self, msg):
        # stamp 객체에서 초와 나노초를 추출하여 가독성 있게 출력
        sec = msg.stamp.sec
        nanosec = msg.stamp.nanosec
        self.get_logger().info(f'Received Time: {sec}.{nanosec:09d}s')

def main(args=None):
    rclpy.init(args=args)
    node = MessageSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
