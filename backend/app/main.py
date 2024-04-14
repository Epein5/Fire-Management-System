from services.firebaseservice import FirebaseService
import uuid

firebase_service = FirebaseService()

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