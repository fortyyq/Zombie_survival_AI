import cv2
import mediapipe as mp

class HandDetector:

    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        lmList = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

                h, w, c = img.shape

                for id, lm in enumerate(handLms.landmark):
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    lmList.append((id, cx, cy))

        return img, lmList

    def getHandX(self, lmList):

        if len(lmList) == 0:
            return None

        return lmList[9][1]

    def fingersUp(self, lmList):

        if len(lmList) == 0:
            return [0, 0, 0, 0, 0]

        tips = [4, 8, 12, 16, 20]
        fingers = []

        if lmList[tips[0]][1] > lmList[tips[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1, 5):
            if lmList[tips[i]][2] < lmList[tips[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers