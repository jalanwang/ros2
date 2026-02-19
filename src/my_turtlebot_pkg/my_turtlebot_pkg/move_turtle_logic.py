# ~/robot/robot_ws/src/my_turtlebot_pkg/my_turtlebot_pkg/move_turtle_logic.py
# 라이다 센서 데이터를 구독
# 터틀을 움직이게 한다.
# 현재 정면 좌우 45도씩 바라보고 있다.
# 0.3m 이내에 장애물이 있으면 멈춘다.
# 수정중

import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan

from rclpy.callback_groups import ReentrantCallbackGroup
from my_package_msgs.srv import GoFront, Rotate, Stop

from .turtle_pose_and_position import TurtlebotPose
import time

class MoveTurtleLogic(Node):
  def __init__(self):
    super().__init__('move_turtle_logic')

    # 위치 추적 클래스 객체 생성
    self.pose_tracker = TurtlebotPose(self)

    self.qos_profile = QoSProfile(depth = 10)
    self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', self.qos_profile)
    # cmd_vel_publisher는 Twist 메시지를 /cmd_vel 토픽에 발행하는 퍼블리셔 인터페이스

    self.has_scan_received = False # 라이다 데이터를 받았는지 여부를 추적하는 플래그
    self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, qos_profile=qos_profile_sensor_data)
    # scan_sub는 LaserScan 메시지를 /scan 토픽에서 구독하는 서브스크라이버 인터페이스.
    # qos_profile_sensor_data는 센서 데이터에 적합한 QoS 설정을 사용.

    self.velocity = 0.0
    self.angular = 0.0
    self.scan_ranges = [] # 라이다 데이터의 범위를 저장하는 리스트
    self.front_min = 0.0 # 라이다 데이터에서 전방의 최소 거리값을 저장하는 변수

    self.MAX_LINEAR_VEL = 0.22 # m/s (Turtlebot3 Burger max linear velocity)
    self.MAX_ANGULAR_VEL = 2.84 # rad/s (Turtlebot3 Burger max angular velocity)

    # Service Servers for basic movements
    self.service_callback_group = ReentrantCallbackGroup()
    self.go_front_srv = self.create_service(GoFront, 'go_front_service', self.go_front_service_callback, callback_group=self.service_callback_group)
    self.rotate_srv = self.create_service(Rotate, 'rotate_service', self.rotate_service_callback, callback_group=self.service_callback_group)
    self.stop_srv = self.create_service(Stop, 'stop_service', self.stop_service_callback, callback_group=self.service_callback_group)

    self.get_logger().info("MoveTurtleLogic node initialized with movement services.")

    self.linear_x = 0.2 # m/s (Turtlebot3 Burger max linear velocity)
    self.log_queue = [] # 로직 엔진에서 발생하는 로그 메시지를 저장하는 큐.

  def scan_callback(self, msg):
    #라이다 CW 가정
    self.scan_ranges = msg.ranges
    self.has_scan_received = True
    scan_range = len(self.scan_ranges)
    if scan_range == 0:
      return

    right_range = int(scan_range / 8) # 45도
    left_range = int(scan_range * 7 / 8) # one round -45도

    front_ranges = self.scan_ranges[0:right_range] + self.scan_ranges[left_range:]
    if front_ranges:
      self.front_min = min(front_ranges) # 전방의 최소 거리값을 계산하여 front_min 변수에 저장

  def is_obstacle_ahead(self):
    if not self.has_scan_received:
      return False

    return self.front_min < 0.3
    # 장애물이 0.3m 이내에 있으면 True 반환, 그렇지 않으면 False 반환

  def add_log(self, msg):
    self.log_queue.append(msg) # 로직 엔진에서 로그 메시지를 생성할 때마다 add_log 함수를 호출하여 로그 큐에 메시지를 추가한다.

  def get_yaw(self):
    """Returns the current yaw angle of the robot in radians."""
    return self.pose_tracker.last_pose_theta

  def _apply_velocity_limits(self):
    """Applies velocity limits to self.velocity and self.angular."""
    self.velocity = max(-self.MAX_LINEAR_VEL, min(self.velocity, self.MAX_LINEAR_VEL))
    self.angular = max(-self.MAX_ANGULAR_VEL, min(self.angular, self.MAX_ANGULAR_VEL))

  def _internal_stop(self):
    """Internal helper to stop the robot. Used by blocking movements and obstacle detection."""
    self.velocity = 0.0
    self.angular = 0.0
    self._apply_velocity_limits() # Ensure limits are applied even for stop
    # Publish a stop command immediately
    msg = Twist()
    msg.linear.x = 0.0
    msg.angular.z = 0.0
    self.cmd_vel_publisher.publish(msg)
    # self.add_log("Robot internally stopped.") # Avoid excessive logging for internal stops

  def stop(self):
    """Public stop command, logs and publishes. This is called by GUI."""
    self._internal_stop()
    self.add_log("Stopped by user command.")
    self.get_logger().info("Robot stopped by user command.")

  # Service Callbacks
  def go_front_service_callback(self, request, response):
    self.get_logger().info(f"Received GoFront service request: length={request.length}")
    self.go_front(request.length) # Call the internal blocking function
    response.success = True
    return response

  def rotate_service_callback(self, request, response):
    self.get_logger().info(f"Received Rotate service request: angle_degrees={request.angle_degrees}")
    self.rotate(request.angle_degrees) # Call the internal blocking function
    response.success = True
    return response

  def stop_service_callback(self, request, response):
    self.get_logger().info("Received Stop service request.")
    self._internal_stop() # Call internal stop
    response.success = True
    return response

  def set_linear_velocity(self, linear_speed):
    """Sets the linear velocity."""
    self.velocity = linear_speed
    self._apply_velocity_limits()
    self.add_log(f"Current V: {self.velocity:.2f}, W: {self.angular:.2f}")

  def set_angular_velocity(self, angular_speed):
    """Sets the angular velocity."""
    self.angular = angular_speed
    self._apply_velocity_limits()
    self.add_log(f"Current V: {self.velocity:.2f}, W: {self.angular:.2f}")

  def rotate(self, target_angle_degrees):
    """Rotates the turtlebot by a specified angle in degrees (blocking)."""
    # Convert degrees to radians
    target_angle_radians = math.radians(target_angle_degrees)

    initial_yaw = self.get_yaw()
    target_yaw = initial_yaw + target_angle_radians

    # Normalize target_yaw to [-pi, pi]
    target_yaw = math.atan2(math.sin(target_yaw), math.cos(target_yaw))

    # Use a fixed angular speed for turning
    # Ensure turn_speed is within MAX_ANGULAR_VEL
    turn_speed = 0.5 # rad/s, adjust as needed
    if abs(turn_speed) > self.MAX_ANGULAR_VEL:
        turn_speed = self.MAX_ANGULAR_VEL if turn_speed > 0 else -self.MAX_ANGULAR_VEL

    # Determine rotation direction
    if target_angle_degrees < 0:
        turn_speed = -abs(turn_speed)
    else:
        turn_speed = abs(turn_speed)

    # Loop until the robot is within a small tolerance of the target yaw
    yaw_tolerance = math.radians(2.0) # 2 degrees tolerance

    while True:
        # rclpy.spin_once(self, timeout_sec=0.01) # Executor handles spinning, removed to prevent nested spin
        current_yaw = self.get_yaw()

        yaw_diff = target_yaw - current_yaw
        yaw_diff = math.atan2(math.sin(yaw_diff), math.cos(yaw_diff)) # Shortest angular distance

        if abs(yaw_diff) < yaw_tolerance:
            break # Reached target angle

        self.set_angular_velocity(turn_speed if yaw_diff > 0 else -turn_speed) # Set angular velocity
        time.sleep(0.01) # Small delay

    self._internal_stop() # Stop the robot after turning
    self.add_log(f"Rotated by {target_angle_degrees:.2f} degrees.")

  def go_front(self, length):
    """Moves the turtlebot straight for a specified length."""
    start_x = self.pose_tracker.last_pose_x
    start_y = self.pose_tracker.last_pose_y
    distance_moved = 0.0

    self.set_linear_velocity(self.linear_x) # Start moving forward with default linear_x

    while distance_moved < length:
      # The update_and_publish loop will handle publishing cmd_vel based on self.velocity
      # We just need to spin to get updated pose data
      # rclpy.spin_once(self, timeout_sec=0.01) # Executor handles spinning, removed to prevent nested spin

      current_x = self.pose_tracker.last_pose_x
      current_y = self.pose_tracker.last_pose_y
      distance_moved = math.sqrt((current_x - start_x)**2 + (current_y - start_y)**2)

      time.sleep(0.01) # Small delay to prevent busy-waiting

    self._internal_stop() # Stop the robot after moving the desired length
    self.add_log(f"Moved {length:.2f} meters.")


  def update_key(self, key):
    # GUI에서 버튼 클릭 시 호출되는 함수로, 키 입력을 처리하여 터틀봇의 움직임을 제어하는 함수
    if key in ['w','W']:
      # Increment current velocity and then set it
      new_velocity = self.velocity + 0.05 # Smaller increment for finer control
      self.set_linear_velocity(new_velocity)
    elif key in ['a','A']:
      # Increment current angular velocity and then set it
      new_angular = self.angular + 0.1
      self.set_angular_velocity(new_angular)
    elif key in ['s','S']:
      self.stop()
    elif key in ['d','D']:
      # Decrement current angular velocity and then set it
      new_angular = self.angular - 0.1
      self.set_angular_velocity(new_angular)
    elif key in ['x','X']:
      # Decrement current velocity and then set it
      new_velocity = self.velocity - 0.05 # Smaller decrement
      self.set_linear_velocity(new_velocity)

  def action_triangle(self):
    # GUI에서 삼각형 버튼 클릭 시 호출되는 함수로, 특정 행동을 수행하도록 하는 함수
    self.get_logger().info('Triangle button clicked!')
    self.add_log("Triangle button clicked! (GUI will send Action Goal)")

  def action_square(self):
    # GUI에서 사각형 버튼 클릭 시 호출되는 함수로, 특정 행동을 수행하도록 하는 함수
    self.get_logger().info('Square button clicked!')
    self.add_log("Square button clicked! (GUI will send Action Goal)")

  def update_and_publish(self):
    msg = Twist() # Twist 메시지 객체를 생성하여 터틀봇의 선속도와 각속도를 설정하는 함수

    # Check for obstacles only if the robot is trying to move forward
    if self.is_obstacle_ahead() and self.velocity > 0:
      log_text=f"Obstacle Detected! Distance: {self.front_min: .2f}m"
      self.get_logger().info(f'Obstacle 발견!: {self.front_min}', throttle_duration_sec=1)
      self.add_log(log_text)
      self._internal_stop() # Use internal stop
      msg.linear.x = 0.0
      msg.angular.z = 0.0
    else:
      msg.linear.x = self.velocity
      msg.angular.z = self.angular
      # Only log "No Obstacle" if not already stopped by obstacle
      if not self.is_obstacle_ahead():
        self.get_logger().info(f'No Obstacle: {self.front_min}', throttle_duration_sec=1)

    self.cmd_vel_publisher.publish(msg) # cmd_vel 토픽에 Twist 메시지를 발행하여 터틀봇의 속도와 회전 속도를 제어

# The main function for MoveTurtleLogic is commented out because it's intended to be
# instantiated and spun by move_turtle_by_controller_rclpy.py.
# If this node were to run standalone, this main function would be used.
# def main(args=None):
#   rclpy.init(args=args)
#   node = MoveTurtleLogic()
#   try:
#     rclpy.spin(node)
#   except KeyboardInterrupt:
#     node.get_logger().info('Keyboard interrupt!!!!')
#   finally:
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
# 	  main()
