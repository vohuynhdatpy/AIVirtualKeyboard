import cv2
from cvzone.HandTrackingModule import HandDetector

class HandTracker:
    def __init__(self, detection_conf=0.8):
        self.detector = HandDetector(detectionCon=detection_conf)

    def detect(self, img):
        hands, img = self.detector.findHands(img)
        return hands, img

    def get_distance(self, p1, p2, img):
        """Tính khoảng cách giữa 2 điểm landmark"""
        l, info, img = self.detector.findDistance(p1, p2, img)
        return l
