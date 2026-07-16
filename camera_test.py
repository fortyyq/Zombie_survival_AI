import cv2
from hand_detector import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector()

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, lmList = detector.findHands(frame)

    if len(lmList) != 0:
        x = detector.getHandX(lmList)

        if x is not None:
            cv2.putText(
                frame,
                f"X : {x}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()