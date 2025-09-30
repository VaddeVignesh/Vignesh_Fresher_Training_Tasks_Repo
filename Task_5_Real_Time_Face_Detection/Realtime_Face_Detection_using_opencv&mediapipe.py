import cv2
import mediapipe as mp
import time

class ProFaceDetector:
    """
    Simple face detector using MediaPipe FaceDetection only.
    """
    def __init__(self, min_detection_confidence=0.5):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=min_detection_confidence,
            model_selection=1  # 0 = short range, 1 = full range
        )

    def find_faces(self, image):
        ih, iw, _ = image.shape
        detections_data = []

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(img_rgb)

        if results.detections:
            for detection in results.detections:
                bbox_c = detection.location_data.relative_bounding_box
                x_min = int(bbox_c.xmin * iw)
                y_min = int(bbox_c.ymin * ih)
                w = int(bbox_c.width * iw)
                h = int(bbox_c.height * ih)
                detections_data.append({
                    'bbox': (x_min, y_min, w, h),
                    'score': detection.score[0]
                })

        return detections_data


def draw_stylish_bbox(img, bbox, score, color=(0, 255, 0), l=30, t=5, rt=1):
    x, y, w, h = bbox[0]-10, bbox[1]-20, bbox[2]+20, bbox[3]+30
    x1, y1 = x + w, y + h

    cv2.rectangle(img, (x, y), (x1, y1), color, rt)
    cv2.line(img, (x, y), (x + l, y), color, t)
    cv2.line(img, (x, y), (x, y + l), color, t)
    cv2.line(img, (x1, y), (x1 - l, y), color, t)
    cv2.line(img, (x1, y), (x1, y + l), color, t)
    cv2.line(img, (x, y1), (x + l, y1), color, t)
    cv2.line(img, (x, y1), (x, y1 - l), color, t)
    cv2.line(img, (x1, y1), (x1 - l, y1), color, t)
    cv2.line(img, (x1, y1), (x1, y1 - l), color, t)

    if score > 0.01:
        label = f'{int(score * 100)}%'
        (w_text, h_text), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)
        cv2.rectangle(img, (x, y - h_text - 15), (x + w_text + 10, y - 10), color, -1)
        cv2.putText(img, label, (x + 5, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(" Error: Could not open webcam.")
        return

    cap.set(3, 1280)
    cap.set(4, 720)

    p_time = 0
    detector = ProFaceDetector(min_detection_confidence=0.35)

    while True:
        success, img = cap.read()
        if not success:
            print(" Failed to grab frame.")
            break

        img = cv2.flip(img, 1)
        detections = detector.find_faces(img)

        colors = [(255, 0, 255), (0, 255, 255), (0, 255, 0), (255, 255, 0), (0, 128, 255)]
        for i, face in enumerate(detections):
            draw_stylish_bbox(img, face['bbox'], face['score'], color=colors[i % len(colors)])

        # FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        overlay = img.copy()
        cv2.rectangle(overlay, (5, 5), (420, 110), (0, 0, 0), -1)
        img = cv2.addWeighted(overlay, 0.6, img, 0.4, 0)
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), 2)
        cv2.putText(img, f'Faces Detected: {len(detections)}', (20, 95), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("My Face Detector", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()
