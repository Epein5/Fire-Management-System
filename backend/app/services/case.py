# import cv2
import time
import numpy as np
# from ultralytics import YOLO
import os
import sys


class FireDetection:
    def __init__(self, model):
        self.model = model  # Store the model object
        self.previous_detections = []
        self.alert_triggered = False
        self.last_alert_time = 0
        self.time_threshold_constant = 15
        self.threshold_box_area = 15000
        self.time_threshold_increase = 13
        self.last_increasing_alert_time = 0
        self.last_large_alert_time = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.start_time = time.time()

    def send_alert(self, message, image, results):
        print(message)
        # Create a new text file indicating fire detection
        with open("fire_detected.txt", "w") as file:
            file.write(message)

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
                            if self.a == 0:
                                self.send_alert("Fire is Detected: Constant detection!", image, results)
                                self.a += 1
                            self.last_alert_time = current_time
                        if box_area > self.threshold_box_area:
                            results = np.array(frame, dtype="uint8")
                            image = results.copy()
                            if self.b == 0:
                                self.send_alert("Fire is Detected: Large bounding box!", image, results)
                                self.b += 1
                            self.last_alert_time = current_time
                            self.last_large_alert_time = current_time
                        if all(prev_box[2] * prev_box[3] < x2 * y2 for prev_box in self.previous_detections):
                            if current_time - self.last_increasing_alert_time > self.time_threshold_increase:
                                results = np.array(frame, dtype="uint8")
                                image = results.copy()
                                if self.c == 0:
                                    self.send_alert("Fire is Detected: Bounding box increasing continuously!", image, results)
                                    self.c += 1
                                self.last_increasing_alert_time = current_time
                                self.last_alert_time = current_time
                        self.previous_detections.append([x1, y1, x2, y2])
                        if len(self.previous_detections) > 50:
                            self.previous_detections.pop(0)
                if not any(names[class_id] in ["fire", "smoke"] for class_id in classes):
                    self.alert_triggered = False
