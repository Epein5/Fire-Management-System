import time
import numpy as np
# from .firebaseservice import FirebaseService

class FireDetection:
    def __init__(self, model):
        self.model = model  # Store the model object
        self.previous_detections = []
        self.alert_triggered = False
        self.last_alert_time = 0
        self.time_threshold_constant = 15
        self.threshold_box_area = 5500
        self.time_threshold_increase = 13
        self.last_increasing_alert_time = 0
        self.last_large_alert_time = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.start_time = time.time()
        self.bool = False
        # self.firebase_service = FirebaseService()

    # def send_alert(self, message, image, results):
    #     print(message)
    #     if message == 2:
    #         self.firebase_service.create_new_fire()

    def process_frame(self, frame, results):
        for detection in results:
            boxes = results[0].boxes.xyxy.tolist()
            classes = results[0].boxes.cls.tolist()
            names = results[0].names
            confidences = results[0].boxes.conf.tolist()

            if boxes is not None and confidences is not None:
                for box, prob, class_id in zip(boxes, confidences, classes):
                    if names[class_id] in ["fire", "smoke"]:
                        x1, y1, x2, y2 = box
                        box_width = x2 - x1
                        box_height = y2 - y1
                        box_area = box_width * box_height
                        current_time = time.time() - self.start_time + 1

                        if current_time - self.last_alert_time > self.time_threshold_constant:
                            results = np.array(frame, dtype="uint8")
                            image = results.copy()
                            # a = str(box_area)
                            if self.a == 0:
                                # self.send_alert(str(box_area), image, results) COnsntant box
                                # self.send_alert(0,image,results)
                                self.a += 1
                            self.last_alert_time = current_time

                        if box_area > self.threshold_box_area:
                            results = np.array(frame, dtype="uint8")
                            image = results.copy()
                            if self.b == 0:
                                # self.send_alert(f"Fire is Detected: Large bounding box! {box_area}", image, results)
                                # self.send_alert(1,image,results)
                                self.b += 1
                            self.last_alert_time = current_time
                            self.last_large_alert_time = current_time

                        self.previous_detections.append([x1, y1, x2, y2])

                        if len(self.previous_detections) > 1:
                            prev_box_area = self.previous_detections[-2][2] * self.previous_detections[-2][3]
                            current_box_area = x2 * y2
                            area_increase = current_box_area - prev_box_area

                            # Set a threshold for significant area increase
                            significant_increase_threshold = 100  # Adjust this value according to your requirements

                            if area_increase > significant_increase_threshold:
                                if current_time - self.last_increasing_alert_time > self.time_threshold_increase:
                                    results = np.array(frame, dtype="uint8")
                                    image = results.copy()
                                    if self.c == 0:
                                        # self.send_alert("Fire is Detected: Bounding box increasing rapidly!", image, results)
                                        # self.send_alert(2,image,results)
                                        self.bool = True
                                        self.c += 1
                                    self.last_increasing_alert_time = current_time
                                    self.last_alert_time = current_time

                        if len(self.previous_detections) > 50:
                            self.previous_detections.pop(0)

                if not any(names[class_id] in ["fire", "smoke"] for class_id in classes):
                    self.alert_triggered = False
        return self.bool