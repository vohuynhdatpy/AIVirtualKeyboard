import time
import cv2
import numpy as np
from pynput.keyboard import Controller, Key
from tensorflow import keras
from modules.cnn_model import build_cnn_cbam_extended


class GestureRecognizer:
    def __init__(self):
        self.keyboard = Controller()
        self.final_text = ""
        self.last_click_time = 0  # thời gian nhấn ký tự cuối cùng

        # Xây dựng và compile CNN model cho gesture recognition (5 classes: Click=0, Pinch=1, Grab=2, Swipe=3, Stop=4)
        self.model = build_cnn_cbam_extended(input_shape=(64, 64, 3), num_classes=5)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print("✅ CNN model built and compiled for GestureRecognizer.")

    def preprocess_hand_image(self, img, bbox=None):
        """
        Crop và preprocess vùng tay từ img để input CNN (resize 64x64, normalize [0,1]).
        - bbox: [x1, y1, x2, y2] từ HandTracker.
        """
        if bbox is None:
            h, w = img.shape[:2]
            bbox = [0, 0, w, h]

        x1, y1, x2, y2 = map(int, bbox)
        # Clamp bbox để tránh out-of-bound
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)

        hand_crop = img[y1:y2, x1:x2]
        if hand_crop.size == 0:
            return None

        # Resize và normalize
        hand_crop = cv2.resize(hand_crop, (64, 64))
        hand_crop = hand_crop.astype(np.float32) / 255.0
        hand_crop = np.expand_dims(hand_crop, axis=0)  # Add batch dim
        return hand_crop

    def predict_gesture(self, img, bbox=None, threshold=0.6):
        """
        Predict gesture bằng CNN từ crop tay.
        - Trả về: (class_id, confidence) hoặc (None, 0) nếu conf thấp.
        """
        processed = self.preprocess_hand_image(img, bbox)
        if processed is None:
            return None, 0

        predictions = self.model.predict(processed, verbose=0)
        class_id = np.argmax(predictions[0])
        confidence = predictions[0][class_id]

        if confidence >= threshold:
            gestures = {0: "Click", 1: "Pinch", 2: "Grab", 3: "Swipe", 4: "Stop"}
            print(f"🔍 Predicted: {gestures.get(class_id, 'Unknown')} (conf: {confidence:.2f})")
            return class_id, confidence
        return None, 0

    def check_click(self, distance, key, img, bbox=None, lmList=None):
        """
        Hybrid check: Sử dụng CNN predict gesture (ưu tiên Click class=0), fallback distance nếu cần.
        - distance: Khoảng cách ngón trỏ-ngón giữa (fallback).
        - key: Phím để press.
        - img: Frame OpenCV.
        - bbox: Bounding box tay (từ HandTracker).
        - lmList: Landmarks (tùy chọn, nếu dùng MLP hybrid sau).
        """
        current_time = time.time()
        if current_time - self.last_click_time < 0.4:
            return False

        # Ưu tiên CNN predict
        class_id, conf = self.predict_gesture(img, bbox)
        trigger = False
        if class_id == 0 and conf > 0.7:  # Click gesture
            trigger = True
            print(f"✅ CNN Click triggered!")
        elif distance < 30:  # Fallback rule-based
            trigger = True
            print(f"📏 Distance fallback triggered (dist: {distance:.1f})")

        if trigger:
            try:
                self.keyboard.press(key)
                self.keyboard.release(key)
                self.last_click_time = current_time
                self.final_text += str(key)  # Lưu text
                print(f"Đã nhấn: {key}")
                return True
            except ValueError:
                print(f"⚠ Không hỗ trợ phím: {key}")

        return False


# ========== DEMO SỬ DỤNG (TÍCH HỢP VÀO MAIN LOOP) ==========
if __name__ == "__main__":
    recognizer = GestureRecognizer()

    # Ví dụ tích hợp trong main.py loop (giả sử có hands từ HandTracker)
    # hands, img = tracker.detect(img)
    # if hands:
    #     hand = hands[0]
    #     bbox = hand['bbox']
    #     lmList = hand['lmList']
    #     p1 = lmList[8][:2]  # Index tip
    #     p2 = lmList[12][:2]  # Middle tip
    #     distance = tracker.get_distance(p1, p2)
    #     key = 'A'  # Từ hover button
    #     recognizer.check_click(distance, key, img, bbox=bbox, lmList=lmList)

    print("🚀 GestureRecognizer với CNN tích hợp sẵn sàng cho AI Virtual Keyboard!")
