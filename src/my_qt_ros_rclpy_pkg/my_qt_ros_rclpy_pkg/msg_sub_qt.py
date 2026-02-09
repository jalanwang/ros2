import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile, QThread, Signal, Slot
from rclpy.executors import MultiThreadedExecutor
from my_qt_ros_rclpy_pkg.sub_msg_ui import Ui_MainWindow
# .sub_pub_msg_ui에서 Ui_Form 임포트에서 위와 같이 수정

class RclpyThread(QThread):
    """ROS2 executor를 별도 스레드에서 실행"""
    def __init__(self, executor):
        super().__init__()
        self.executor = executor

    def run(self):
        try:
            self.executor.spin()
        finally:
            rclpy.shutdown()

class HelloworldSubscriber(QMainWindow):
    """Qt GUI 메인 윈도우 - Subscriber"""

    def __init__(self):
        super(HelloworldSubscriber, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 버튼 연결
        self.ui.btn_start.clicked.connect(self.btn_sub_start_clicked)
        self.ui.btn_cancel.clicked.connect(self.btn_sub_cancel_clicked)

        # ROS2 초기화
        rclpy.init()
        self.sub_node = Node("Helloworld_subscriber")
        qos_profile = QoSProfile(depth=10)
        self.helloworld_subscriber = self.sub_node.create_subscription(
            String,
            'helloworld',
            self.subscribe_topic_message,
            qos_profile)

        # Executor 및 스레드 설정
        self.executor = MultiThreadedExecutor()
        self.rclpy_thread = RclpyThread(self.executor)
        self.rclpy_thread.start()

    def subscribe_topic_message(self, msg):
        """토픽 메시지 수신 콜백"""
        self.sub_node.get_logger().info('Received message: {0}'.format(msg.data))
        self.ui.listWidget.addItem(msg.data)

    def btn_sub_start_clicked(self):
        """Start 버튼 클릭 - Subscriber 시작"""
        self.executor.add_node(self.sub_node)

    def btn_sub_cancel_clicked(self):
        """Cancel 버튼 클릭 - Subscriber 종료"""
        self.executor.remove_node(self.sub_node)

    def closeEvent(self, event):
        """윈도우 종료 이벤트 - 리소스 정리"""
        print("쓰레드 및 노드 종료")
        self.executor.shutdown()
        self.rclpy_thread.quit()
        self.rclpy_thread.wait()
        self.sub_node.destroy_node()
        rclpy.shutdown()
        super().closeEvent(event)

def main():
    """메인 함수"""

    app = QApplication(sys.argv)
    window = HelloworldSubscriber()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
