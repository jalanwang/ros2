import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

# MediaPipe 설정
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def classify_hand(hand_landmarks):
    landmarks = hand_landmarks.landmark

    def is_finger_straight(finger_tip_idx, finger_dip_idx):
        return landmarks[finger_tip_idx].y < landmarks[finger_dip_idx].y

    index_straight = is_finger_straight(8, 6)
    middle_straight = is_finger_straight(12, 10)
    ring_straight = is_finger_straight(16, 14)
    pinky_straight = is_finger_straight(20, 18)

    # 손동작에 따른 결과 반환
    if index_straight and not middle_straight and not ring_straight and not pinky_straight:
        return "one"     # 전진
    elif index_straight and middle_straight and not ring_straight and not pinky_straight:
        return "sissor"  # 왼쪽 회전
    elif index_straight and middle_straight and ring_straight and not pinky_straight:
        return "three"   # 오른쪽 회전
    elif not index_straight and not middle_straight and not ring_straight and not pinky_straight:
        return "Rock"    # 정지
    elif index_straight and middle_straight and ring_straight and pinky_straight:
        return "paper"   # 후진
    return "None"

class HandControlNode(Node):
    def __init__(self):
        super().__init__('hand_control_node')
        self.qos_profile = QoSProfile(depth=10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', self.qos_profile)
        self.twist = Twist()

    def publish_move(self, gesture):
        # 제스처별 속도 할당
        if gesture == "one":      # 전진
            self.twist.linear.x = 0.2
            self.twist.angular.z = 0.0
        elif gesture == "paper":  # 후진
            self.twist.linear.x = -0.2
            self.twist.angular.z = 0.0
        elif gesture == "sissor": # 왼쪽 회전
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5
        elif gesture == "three":  # 오른쪽 회전
            self.twist.linear.x = 0.0
            self.twist.angular.z = -0.5
        elif gesture == "Rock":   # 정지
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0

        self.publisher.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    node = HandControlNode()

    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            gesture = "None"
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    gesture = classify_hand(hand_landmarks)

            # ROS2 메시지 발행
            node.publish_move(gesture)

            # 화면 표시
            cv2.putText(image, f"Gesture: {gesture}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.imshow('MediaPipe Hand Control', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    node.destroy_node()
    rclpy.shutdown()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
