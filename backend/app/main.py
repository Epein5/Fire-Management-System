# from services.firebaseservice import FirebaseService
# import uuid

# firebase_service = FirebaseService()

# result = firebase_service.get_all_data()
# print(result)




# new_fire_id = firebase_service.create_new_fire()
# print("New fire ID:", new_fire_id)




# fire_id_to_update = "-Nv3aK6ZLGT3b89x5nxf"
# firebase_service.update_fire_condition(fire_id_to_update)





# fire_id_to_update = "-Nv3aK6ZLGT3b89x5nxf"  # Replace with the ID of the fire entry you want to update
# manpower_data = {
#     'unique_id_1': {'photo': 'photo_url_1','name':'name_1','contact':'contact_1'},
#     'unique_id_2': {'photo': 'photo_url_2','name':'name_2','contact':'contact_2'}
# }  # Manpower data with unique IDs and photo URLs
# vehicle_data = {
#     'bus_no_1':{ 'photo': 'photo_url_1',},
#     'bus_no_2':{ 'photo': 'photo_url_2',}
# }  # Vehicle data with unique IDs and photo URLs
# firebase_service.assign_resources(fire_id_to_update, manpower_data, vehicle_data)





# manpower1_id = firebase_service.create_manpower('Ram Bahadur', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Hari Shah', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Shyam Neupane', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Aman Kumar Jha', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Anshu Patel', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Bhabuk Thapa', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Bikash Thapa', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Biraj Thapa', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Bishal Thapa', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Bishnu Timilshina', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Bishnu Thapa', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Bishnu Adhikari', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Bishnu Shrestha', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Bishnu Aachraya', 'photo_url_2')
# manpower1_id = firebase_service.create_manpower('Aakash Thapa', 'photo_url_1')
# manpower2_id = firebase_service.create_manpower('Aakash Gautam', 'photo_url_2')

# # Create vehicles with photo URLs
# vehicle1_id = firebase_service.create_vehicle('vehicle_photo_url_1')
# vehicle2_id = firebase_service.create_vehicle('vehicle_photo_url_2')
# vehicle1_id = firebase_service.create_vehicle('vehicle_photo_url_3')
# vehicle2_id = firebase_service.create_vehicle('vehicle_photo_url_4')

# print("Manpower IDs:", manpower1_id, manpower2_id)
# print("Vehicle IDs:", vehicle1_id, vehicle2_id)


# firebase_service.delete_fire("-Nv3BTw9wX3D9Ny5IY32") 
# print(firebase_service.find_total_fire_cases())

# manpower_data, vehicle_data = firebase_service.get_all_assigned_resources()
# print(manpower_data, vehicle_data)



# remaining_manpower, remaining_vehicles = firebase_service.get_remaining_resources()
# print("Remaining Manpower:")
# for manpower_id, manpower_info in remaining_manpower.items():
#     print(manpower_id, ":", manpower_info)

# print("\nRemaining Vehicles:")
# for vehicle_id, vehicle_info in remaining_vehicles.items():
#     print(vehicle_id, ":", vehicle_info)




# resources_count = firebase_service.get_assigned_and_available_resources_count()

# print("Assigned Manpower Count:", resources_count['assigned_manpower_count'])
# print("Assigned Vehicle Count:", resources_count['assigned_vehicle_count'])
# print("Available Manpower Count:", resources_count['available_manpower_count'])
# print("Available Vehicle Count:", resources_count['available_vehicle_count'])


from fastapi import FastAPI, HTTPException,Request,Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .services.firebaseservice import FirebaseService
from fastapi.templating import Jinja2Templates
from .model import *
import httpx


app = FastAPI()
templates = Jinja2Templates(directory=r"C:\Users\KNYpe\Desktop\Fire-Management-System\frontend")
app.mount("/assets", StaticFiles(directory=r"C:\Users\KNYpe\Desktop\Fire-Management-System\frontend\assets"), name="assets")

firebase_service = FirebaseService()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    no_of_fire_cases = firebase_service.find_total_fire_cases()
    available_no_of_manpower = firebase_service.get_assigned_and_available_resources_count()['available_manpower_count']
    available_no_of_vehicles = firebase_service.get_assigned_and_available_resources_count()['available_vehicle_count']
    assigned_no_of_manpower = firebase_service.get_assigned_and_available_resources_count()['assigned_manpower_count']
    assigned_no_of_vehicles = firebase_service.get_assigned_and_available_resources_count()['assigned_vehicle_count']
    hawa = firebase_service.get_all_assigned_resources()
    print(hawa)
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

    # print(remaining_resources)
    return templates.TemplateResponse("map.html", {"request": request, "info": info, "manpower_data": manpower_data, "vehicle_data": vehicle_data,"fire_id":fire_id})

@app.get("/delete/{fire_id}", response_class=JSONResponse)
async def delete_fire(request: Request, fire_id: str):
    firebase_service.delete_fire(fire_id)
    # Return a JavaScript code to reload the page
    return {'message': "Fire entry with ID '{fire_id}' deleted successfully"}

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
                                       "fire_location": fire_location,})

@app.get("/video_feed/{video_id}", response_class=HTMLResponse)
async def video_feed(request: Request, video_id: str):
    print(video_id)
    return {"video_id": video_id}