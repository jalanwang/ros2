import rclpy as rp
from rclpy.action import ActionServer
from my_first_package_msgs.action import DistTurtle
from rclpy.node import Node
import time

class DistTurtleServer(Node):

  def __init__(self):
      super().__init__('dist_turtle_action_server')
      self.action_server = ActionServer(self, DistTurtle, 'dist_turtle', self.excute_callback)

  def excute_callback(self, goal_handle):
        self.get_logger().info('=== Action callback started ===')
        result = DistTurtle.Result()
        feedback_msg = DistTurtle.Feedback()

        # 작업 수행 중 피드백 발행
        for n in range(0,10):
            feedback_msg.remained_dist = float(n)
            self.get_logger().info(f'Publishing feedback: {n}')
            goal_handle.publish_feedback(feedback_msg)  # 피드백 발행
            time.sleep(0.5)

        # 작업 완료 후 성공 표시
        self.get_logger().info('=== Action completed, sending success ===')
        goal_handle.succeed()
        return result


def main(args=None):
    rp.init(args=args)
    dist_turtle_action_server = DistTurtleServer()
    rp.spin(dist_turtle_action_server)

if __name__ == '__main__':
    main()
