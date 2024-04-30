from fastapi import FastAPI, HTTPException,Request,Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .services.firebaseservice import FirebaseService
from fastapi.templating import Jinja2Templates
from .model import *
import httpx
from fastapi.responses import StreamingResponse
import cv2
from ultralytics import YOLO
import numpy as np
# import os
import sys
import os

# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root directory to the system path
sys.path.append(project_root)

# Now you can import the FireDetection class
from app.services.case import FireDetection


# Load the YOLOv8 model
# model = YOLO("yolov8n.pt")
model = YOLO("static/model/firev8.pt")
fire_detection = FireDetection(model)


app = FastAPI()
templates = Jinja2Templates(directory=r"C:\Users\KNYpe\Desktop\Fire-Management-System\frontend")
app.mount("/assets", StaticFiles(directory=r"C:\Users\KNYpe\Desktop\Fire-Management-System\frontend\assets"), name="assets")
app.mount("/static", StaticFiles(directory=r"C:\Users\KNYpe\Desktop\Fire-Management-System\static"), name="static")

firebase_service = FirebaseService()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    no_of_fire_cases = firebase_service.find_total_fire_cases()
    available_no_of_manpower = firebase_service.get_assigned_and_available_resources_count()['available_manpower_count']
    available_no_of_vehicles = firebase_service.get_assigned_and_available_resources_count()['available_vehicle_count']
    assigned_no_of_manpower = firebase_service.get_assigned_and_available_resources_count()['assigned_manpower_count']
    assigned_no_of_vehicles = firebase_service.get_assigned_and_available_resources_count()['assigned_vehicle_count']
    hawa = firebase_service.get_all_assigned_resources()
    # print(hawa)
    try:
        fire_location = firebase_service.process_fires_with_location_names()
    except:
        print("Error in processing fire data with location names")
    return templates.TemplateResponse("index.html", 
                                      {"request": request,
                                       "no_of_fire_cases": no_of_fire_cases,
                                       "available_no_of_manpower": available_no_of_manpower,
                                       "available_no_of_vehicles": available_no_of_vehicles,
                                       "assigned_no_of_manpower": assigned_no_of_manpower,
                                       "assigned_no_of_vehicles": assigned_no_of_vehicles,
                                       "fire_location": fire_location})


@app.get("/map/{fire_id}", response_class=HTMLResponse)
async def show_map(request: Request, fire_id: str):
    info = firebase_service.find_fire_by_id(fire_id)
    remaining_resources = firebase_service.get_remaining_resources()
    manpower_data, vehicle_data = remaining_resources  # Unpack the tuple

    return templates.TemplateResponse("map.html", {"request": request, "info": info, "manpower_data": manpower_data, "vehicle_data": vehicle_data,"fire_id":fire_id})

@app.delete("/delete/{fire_id}", response_class=JSONResponse)
async def delete_fire(fire_id: str):
    firebase_service.delete_fire(fire_id)
    # Return a JavaScript code to reload the page
    return {'message': f"Fire entry with ID '{fire_id}' deleted successfully"}

@app.get("/route", response_class=JSONResponse)
async def get_route(start_latitude: float, start_longitude: float, end_latitude: float, end_longitude: float):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=YOUR_API_KEY&start={start_longitude},{start_latitude}&end={end_longitude},{end_latitude}"
        )
        return response.json()

@app.post("/assign-resources")
async def assign_resources(resource_assignment: AssignResourcesRequest):
    vehi_dict = {}
    man_dict = {}
    fire_id = resource_assignment.fire_id
    manpower_data = resource_assignment.manpower_data
    vehicle_data = resource_assignment.vehicle_data

    for manpower_id in manpower_data:
        manpower_info = firebase_service.get_resources_info(manpower_id, "manpower")
        if manpower_info:
            man_dict[manpower_id] = manpower_info

    for vehicle_id in vehicle_data:
        vehicle_info = firebase_service.get_resources_info(vehicle_id, "vehicles")
        if vehicle_info:
            vehi_dict[vehicle_id] = vehicle_info

    firebase_service.assign_resources(fire_id, man_dict, vehi_dict)
    firebase_service.update_fire_condition(fire_id)
    return {"message": "Resources assigned successfully"}

@app.get("/livefeed", response_class=HTMLResponse)
async def livefeed(request: Request):
    no_of_fire_cases = firebase_service.find_total_fire_cases()
    available_no_of_manpower = firebase_service.get_assigned_and_available_resources_count()['available_manpower_count']
    available_no_of_vehicles = firebase_service.get_assigned_and_available_resources_count()['available_vehicle_count']
    assigned_no_of_manpower = firebase_service.get_assigned_and_available_resources_count()['assigned_manpower_count']
    assigned_no_of_vehicles = firebase_service.get_assigned_and_available_resources_count()['assigned_vehicle_count']
    try:
        fire_location = firebase_service.process_fires_with_location_names()
    except:
        print("Error in processing fire data with location names")
    return templates.TemplateResponse("live.html", 
                                      {"request": request,
                                       "no_of_fire_cases": no_of_fire_cases,
                                       "available_no_of_manpower": available_no_of_manpower,
                                       "available_no_of_vehicles": available_no_of_vehicles,
                                       "assigned_no_of_manpower": assigned_no_of_manpower,
                                       "assigned_no_of_vehicles": assigned_no_of_vehicles,
                                       "fire_location": fire_location})

@app.get("/video_feed/{video_id}", response_class=HTMLResponse)
async def video_feed(request: Request, video_id: str):
    print(video_id)
    return {"video_id": video_id}


video_paths = {
    "1": "static/videos/fire.mp4",
    # "2": "static/videos/midcandle.mp4",
    # "2": "static/videos/fire1.mp4",
    # "3": "static/videos/video1.mp4",
    # "4": "static/videos/cow.mp4",
    # Add more video paths as needed
}

video_captures = {video_id: cv2.VideoCapture(path) for video_id, path in video_paths.items()}
print(video_captures)

# def generate_frames(video_id):
#     print(f"Generating frames for video: {video_id}")
#     camera = video_captures[video_id]
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             # Run object detection using YOLOv8
#             downsampled_frame = cv2.resize(frame, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
#             results = model(downsampled_frame)
#             a = fire_detection.process_frame(downsampled_frame, results)
#             if a == True:
#                 firebase_service.create_new_fire()
#             # Draw bounding boxes and labels on the frame
#             annotated_frame = results[0].plot()
#             # frame = cv2.cvtColor(np.array(annotated_frame), cv2.COLOR_RGB2BGR)
#             frame = np.array(annotated_frame)
#             # print(frame.shape)
#             # Call the 'create_fire' function for each detected object


#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             # print("Frame generated")
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.get("/video/{video_id}")
# async def video_feed(video_id: str):
#     print(f"Video feed for video: {video_id}")
#     if video_id in video_captures:
#         return StreamingResponse(generate_frames(video_id), media_type="multipart/x-mixed-replace; boundary=frame")
#     else:
#         return {"error": f"Video '{video_id}' not found"}
def generate_frames(video_id):
    print(f"Generating frames for video: {video_id}")
    camera = video_captures[video_id]
    fire_detected = False
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Run object detection using YOLOv8
            downsampled_frame = cv2.resize(frame, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
            results = model(downsampled_frame)
            if not fire_detected:
                fire_detected = fire_detection.process_frame(downsampled_frame, results)
                if fire_detected:
                    firebase_service.create_new_fire()
            # Draw bounding boxes and labels on the frame
            annotated_frame = results[0].plot()
            frame = np.array(annotated_frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/video/{video_id}")
async def video_feed(video_id: str):
    print(f"Video feed for video: {video_id}")
    if video_id in video_captures:
        return StreamingResponse(generate_frames(video_id), media_type="multipart/x-mixed-replace; boundary=frame")
    else:
        return {"error": f"Video '{video_id}' not found"}