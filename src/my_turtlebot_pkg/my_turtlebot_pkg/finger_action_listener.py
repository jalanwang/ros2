import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# -*- coding: utf-8 -*-
def classify_hand(hand_landmarks):
    results = "I dont know"
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]

    landmarks = hand_landmarks.landmark
    def is_finger_straight(finger_tip_idx, finger_dip_idx):
        return landmarks[finger_tip_idx].y < landmarks[finger_dip_idx].y

    # 손가락 펼침 여부
    index_straight = is_finger_straight(8, 6)
    middle_straight = is_finger_straight(12, 10)
    ring_straight = is_finger_straight(16, 14)
    pinky_straight = is_finger_straight(20, 18)
    thumb_open = landmarks[4].x < landmarks[3].x  # 엄지 위치 판단(개개인 손 방향에 따라 조정 필요)

    if index_straight and not middle_straight and not ring_straight and not pinky_straight:
       results = "one"
    elif index_straight and middle_straight and not ring_straight and not pinky_straight:
        results =  "sissor"
    elif index_straight and middle_straight and ring_straight and not pinky_straight:
        results =  "three"
    elif not index_straight and not middle_straight and not ring_straight and not pinky_straight:
        results =  "Rock"
    elif index_straight and middle_straight and ring_straight and pinky_straight:
        results =  "paper"

    return results
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("카메라를 찾을 수 없습니다.")
      # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
      continue

    # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # 이미지에 손 주석을 그립니다.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    gesture = "hands detect"

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        gesture = classify_hand(hand_landmarks)

    cv2.putText(image, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
