# /home/robot/robot_ws/src/my_turtlebot_pkg/my_turtlebot_pkg/turtle_make_shape_server.py

import rclpy
import math
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action import GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from my_package_msgs.action import TurtleMakeShape
from my_package_msgs.srv import GoFront, Rotate, Stop

class TurtleMakeShapeServer(Node):

    def __init__(self):
        super().__init__('turtle_make_shape_server')
        self.get_logger().info('TurtleMakeShape Action Server started.')

        self.action_server_callback_group = ReentrantCallbackGroup()
        self.client_callback_group = ReentrantCallbackGroup()

        self._action_server = ActionServer(
            self,
            TurtleMakeShape,
            'turtle_make_shape',
            self.execute_callback,
            callback_group=self.action_server_callback_group,
            goal_callback=self.goal_callback,
            handle_accepted_callback=self.handle_accepted_callback
        )

        # Create service clients to MoveTurtleLogic
        self.go_front_client = self.create_client(GoFront, 'go_front_service', callback_group=self.client_callback_group)
        self.rotate_client = self.create_client(Rotate, 'rotate_service', callback_group=self.client_callback_group)
        self.stop_client = self.create_client(Stop, 'stop_service', callback_group=self.client_callback_group)

        # Wait for services to be available
        self.get_logger().info('Waiting for GoFront service...')
        self.go_front_client.wait_for_service()
        self.get_logger().info('GoFront service available.')
        self.get_logger().info('Waiting for Rotate service...')
        self.rotate_client.wait_for_service()
        self.get_logger().info('Rotate service available.')
        self.get_logger().info('Waiting for Stop service...')
        self.stop_client.wait_for_service()
        self.get_logger().info('Stop service available.')

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Received goal request: {goal_request}')
        # Accept all goals for now
        return GoalResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle):
        # This is called when the goal is accepted.
        # Start a new thread or task to execute the goal to avoid blocking the main thread.
        self.get_logger().info('Goal accepted. Executing...')
        goal_handle.execute()

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = TurtleMakeShape.Feedback()
        result_msg = TurtleMakeShape.Result()

        shape_type = goal_handle.request.shape_type
        side_length = goal_handle.request.side_length
        iterations = goal_handle.request.iterations

        if shape_type == 1:  # Square
            self.get_logger().info(f'Drawing {iterations} squares of side length {side_length}m.')
            for i in range(iterations):
                if goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    result_msg.message = 'Square drawing canceled.'
                    self.get_logger().info('Square drawing canceled.')
                    await self._call_stop_service()
                    return result_msg

                feedback_msg.status = f'Drawing square {i+1}/{iterations}, side length {side_length}m'
                goal_handle.publish_feedback(feedback_msg)
                self.get_logger().info(feedback_msg.status)

                await self._draw_square_segment(side_length)
                time.sleep(0.5) # Small pause between shapes

            result_msg.message = f'{iterations} squares drawn successfully!'
            self.get_logger().info(result_msg.message)
            goal_handle.succeed()

        elif shape_type == 2:  # Triangle
            self.get_logger().info(f'Drawing {iterations} triangles of side length {side_length}m.')
            for i in range(iterations):
                if goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    result_msg.message = 'Triangle drawing canceled.'
                    self.get_logger().info('Triangle drawing canceled.')
                    await self._call_stop_service()
                    return result_msg

                feedback_msg.status = f'Drawing triangle {i+1}/{iterations}, side length {side_length}m'
                goal_handle.publish_feedback(feedback_msg)
                self.get_logger().info(feedback_msg.status)

                await self._draw_triangle_segment(side_length)
                time.sleep(0.5) # Small pause between shapes

            result_msg.message = f'{iterations} triangles drawn successfully!'
            self.get_logger().info(result_msg.message)
            goal_handle.succeed()

        else:
            goal_handle.abort()
            result_msg.message = 'Invalid shape type requested.'
            self.get_logger().error(result_msg.message)

        await self._call_stop_service() # Ensure robot stops at the end
        return result_msg

    async def _draw_square_segment(self, side_length):
        for i in range(4):
            self.get_logger().info(f'Square: Moving forward {side_length}m (segment {i+1}/4)')
            await self._call_go_front_service(side_length)
            self.get_logger().info(f'Square: Rotating 90 degrees (segment {i+1}/4)')
            await self._call_rotate_service(90.0)
            time.sleep(0.1) # Small pause between movements

    async def _draw_triangle_segment(self, side_length):
        for i in range(3):
            self.get_logger().info(f'Triangle: Moving forward {side_length}m (segment {i+1}/3)')
            await self._call_go_front_service(side_length)
            self.get_logger().info(f'Triangle: Rotating 120 degrees (segment {i+1}/3)')
            await self._call_rotate_service(120.0)
            time.sleep(0.1) # Small pause between movements

    async def _call_go_front_service(self, length):
        request = GoFront.Request()
        request.length = length
        future = self.go_front_client.call_async(request) # Call service asynchronously
        rclpy.spin_until_future_complete(self, future) # This is still needed for blocking wait in async context
        if future.result() is not None:
            self.get_logger().info(f'GoFront service response: {future.result().success}')
            return future.result().success
        else:
            self.get_logger().error('GoFront service call failed.')
            return False

    async def _call_rotate_service(self, angle_degrees):
        request = Rotate.Request()
        request.angle_degrees = angle_degrees
        future = self.rotate_client.call_async(request) # Call service asynchronously
        rclpy.spin_until_future_complete(self, future) # This is still needed for blocking wait in async context
        if future.result() is not None:
            self.get_logger().info(f'Rotate service response: {future.result().success}')
            return future.result().success
        else:
            self.get_logger().error('Rotate service call failed.')
            return False

    async def _call_stop_service(self):
        request = Stop.Request()
        future = self.stop_client.call_async(request) # Call service asynchronously
        rclpy.spin_until_future_complete(self, future) # This is still needed for blocking wait in async context
        if future.result() is not None:
            self.get_logger().info(f'Stop service response: {future.result().success}')
            return future.result().success
        else:
            self.get_logger().error('Stop service call failed.')
            return False

def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor() # Use MultiThreadedExecutor for ActionServer with service clients
    action_server = TurtleMakeShapeServer()
    executor.add_node(action_server)

    try:
        executor.spin()
    except KeyboardInterrupt:
        action_server.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
