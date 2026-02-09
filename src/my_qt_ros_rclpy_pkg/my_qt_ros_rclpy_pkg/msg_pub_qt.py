import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread
from rclpy.executors import MultiThreadedExecutor
from my_qt_ros_rclpy_pkg.pub_msg_ui import Ui_MainWindow


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


class HelloworldPublisher(QMainWindow):
    """Qt GUI 메인 윈도우 - Publisher"""

    def __init__(self):
        super(HelloworldPublisher, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 버튼 연결
        self.ui.btn_start.clicked.connect(self.btn_pub_start_clicked)
        self.ui.btn_cancel.clicked.connect(self.btn_pub_cancel_clicked)

        # ROS2 초기화
        rclpy.init()
        self.count = 0
        self.pub_node = Node("helloworld_publisher")
        qos_profile = QoSProfile(depth=10)
        self.helloworld_publisher = self.pub_node.create_publisher(String, 'helloworld', qos_profile)
        self.timer = self.pub_node.create_timer(1, self.publish_helloworld_msg)

        # Executor 및 스레드 설정
        self.executor = MultiThreadedExecutor()
        self.rclpy_thread = RclpyThread(self.executor)
        self.rclpy_thread.start()

    def publish_helloworld_msg(self):
        """Hello World 메시지 퍼블리시"""
        msg = String()
        msg.data = 'Hello World: {0}'.format(self.count)
        self.helloworld_publisher.publish(msg)
        self.pub_node.get_logger().info('Published message: {0}'.format(msg.data))
        self.count += 1
        self.ui.listWidget.addItem(msg.data)

    def btn_pub_start_clicked(self):
        """Start 버튼 클릭 - Publisher 시작"""
        self.executor.add_node(self.pub_node)
        self.ui.listWidget.addItem('Publisher started')

    def btn_pub_cancel_clicked(self):
        """Cancel 버튼 클릭 - Publisher 중지"""
        self.executor.remove_node(self.pub_node)
        self.ui.listWidget.addItem('Publisher stopped')

    def closeEvent(self, event):
        """윈도우 종료 이벤트 - 리소스 정리"""
        print("쓰레드 및 노드 종료")
        self.executor.shutdown()
        self.rclpy_thread.quit()
        self.rclpy_thread.wait()
        self.pub_node.destroy_node()
        rclpy.shutdown()
        super().closeEvent(event)


def main(args=None):
    """메인 함수"""
    app = QApplication(sys.argv)
    window = HelloworldPublisher()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
