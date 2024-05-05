import firebase_admin
from firebase_admin import credentials, db, storage
from  datetime import datetime
import uuid
import reverse_geocoder as rg

class FirebaseService:
    def __init__(self):
        self.cred = credentials.Certificate(r"C:\Users\KNYpe\Desktop\Fire-Management-System\backend\ServiceAccountKey.json")
        self.firebase_admin = firebase_admin.initialize_app(self.cred, {
            'databaseURL': "https://fire-management-system-13bcd-default-rtdb.firebaseio.com/",
            'storageBucket': "fire-management-system-13bcd.appspot.com"
        })
        self.bucket = storage.bucket()

    def get_image(self,image_name):
        full_path = f"Resources/Manpower/{image_name}"
        blob = self.bucket.blob(full_path)
        image_data = blob.download_as_bytes()
        return image_data


    def get_all_data(self):
        ref = db.reference('/')
        return ref.get()
    
    def get_all_fires(self):
        ref = db.reference('Fire')
        return ref.get()
    
    
    def create_new_fire(self):
        ref = db.reference()
        new_fire_id = ref.child('Fire').push().key
        current_datetime = datetime.now().replace(microsecond=0).isoformat() + 'Z'
        new_fire_data = {
            'location': {
                'latitude': 27.702722, 
                'longitude': 85.317160
            },
            'time_detected': current_datetime[:10] + '     ' + current_datetime[11:16],
            'date_detected': current_datetime[:10],
            'severity': 'High',
            'condition': 'Not Assigned',
            'resources_assigned': {
                'manpower': {},
                'vehicles': {}
            }
        }
        ref.child('Fire').child(new_fire_id).set(new_fire_data)
        return new_fire_id
    

    def update_fire_condition(self, fire_id):
        ref = db.reference()
        fire_ref = ref.child('Fire').child(fire_id)
        fire_data = fire_ref.get()
        if fire_data is not None:
            fire_data['condition'] = 'Already Assigned'
            fire_ref.set(fire_data)
        else:
            print(f"Fire entry with ID '{fire_id}' does not exist.")
    

    def delete_fire(self, fire_id):
        ref = db.reference()
        fire_ref = ref.child('Fire').child(fire_id)
        fire_data = fire_ref.get()
        if fire_data is not None:
            fire_ref.delete()
        else:
            print(f"Fire entry with ID '{fire_id}' does not exist.")

    def find_total_fire_cases(self):
        ref = db.reference()
        fire_ref = ref.child('Fire')
        fire_data = fire_ref.get()
        if fire_data is not None:
            return len(fire_data)
        else:
            return 0
        
    
    def find_fire_by_id(self, fire_id):
        ref = db.reference()
        fire_ref = ref.child('Fire').child(fire_id)
        return fire_ref.get()
    
    def get_all_assigned_resources(self):
        fire_ref = db.reference('Fire')
        for fire_id, fire_data in fire_ref.get().items():
            if 'resources_assigned' in fire_data:
                manpower_data = fire_data['resources_assigned']['manpower']
                vehicle_data = fire_data['resources_assigned']['vehicles']
        return manpower_data, vehicle_data

    def assign_resources(self, fire_id, manpower_data, vehicle_data):
        ref = db.reference()
        fire_ref = ref.child('Fire').child(fire_id)
        fire_data = fire_ref.get()
        if fire_data is not None:
            if 'resources_assigned' not in fire_data:
                fire_data['resources_assigned'] = {'manpower': {}, 'vehicles': {}}

            fire_data['resources_assigned']['manpower'] = manpower_data
            fire_data['resources_assigned']['vehicles'] = vehicle_data

            fire_ref.update({'resources_assigned': fire_data['resources_assigned']})
        else:
            print(f"Fire entry with ID '{fire_id}' does not exist.")
    


    def get_remaining_resources(self):
        all_manpower = self.get_all_manpower()
        all_vehicles = self.get_all_vehicles()
        assigned_manpower_ids, assigned_vehicle_ids = self.get_assigned_resources_ids()
        remaining_manpower = {manpower_id: manpower_info for manpower_id, manpower_info in all_manpower.items() if manpower_id not in assigned_manpower_ids}
        remaining_vehicles = {vehicle_id: vehicle_info for vehicle_id, vehicle_info in all_vehicles.items() if vehicle_id not in assigned_vehicle_ids}

        return remaining_manpower, remaining_vehicles

    def get_all_manpower(self):
        manpower_ref = db.reference('Resources').child('Manpower')
        return manpower_ref.get()

    def get_all_vehicles(self):
        vehicle_ref = db.reference('Resources').child('Vehicles')
        return vehicle_ref.get()

    def get_assigned_resources_ids(self):
        fire_ref = db.reference('Fire')
        assigned_manpower_ids = []
        assigned_vehicle_ids = []
        for fire_data in fire_ref.get().values():
            if 'resources_assigned' in fire_data:
                assigned_manpower_ids.extend(fire_data['resources_assigned']['manpower'].keys())
                assigned_vehicle_ids.extend(fire_data['resources_assigned']['vehicles'].keys())
        return assigned_manpower_ids, assigned_vehicle_ids

    def get_assigned_and_available_resources_count(self):
        # Get assigned manpower and vehicle IDs
        assigned_manpower_ids, assigned_vehicle_ids = self.get_assigned_resources_ids()

        # Get total manpower and vehicle counts
        total_manpower_count = self.get_total_manpower_count()
        total_vehicle_count = self.get_total_vehicle_count()

        # Calculate assigned manpower and vehicle counts
        assigned_manpower_count = len(assigned_manpower_ids)
        assigned_vehicle_count = len(assigned_vehicle_ids)

        # Calculate available manpower and vehicle counts
        available_manpower_count = total_manpower_count - assigned_manpower_count
        available_vehicle_count = total_vehicle_count - assigned_vehicle_count

        return {
            'assigned_manpower_count': assigned_manpower_count,
            'assigned_vehicle_count': assigned_vehicle_count,
            'available_manpower_count': available_manpower_count,
            'available_vehicle_count': available_vehicle_count
        }

    def get_total_manpower_count(self):
        # Get all manpower resources
        all_manpower = self.get_all_manpower()

        # Count the total number of manpower resources
        total_manpower_count = len(all_manpower) if all_manpower else 0

        return total_manpower_count

    def get_total_vehicle_count(self):
        # Get all vehicle resources
        all_vehicles = self.get_all_vehicles()

        # Count the total number of vehicle resources
        total_vehicle_count = len(all_vehicles) if all_vehicles else 0

        return total_vehicle_count

    def get_assigned_resources_ids(self):
        # Get a reference to the "Fire" node
        fire_ref = db.reference('Fire')

        # Initialize lists to store assigned manpower and vehicle IDs
        assigned_manpower_ids = []
        assigned_vehicle_ids = []

        # Iterate through each fire entry
        for fire_data in fire_ref.get().values():
            # Check if the fire entry has 'resources_assigned' field
            if 'resources_assigned' in fire_data:
                # Retrieve assigned manpower and vehicle IDs
                assigned_manpower_ids.extend(fire_data['resources_assigned']['manpower'].keys())
                assigned_vehicle_ids.extend(fire_data['resources_assigned']['vehicles'].keys())

        return assigned_manpower_ids, assigned_vehicle_ids

    def create_manpower(self, name, photo_url):
        manpower_id = self.generate_unique_id()
        manpower_data = {
            'name': name,
            'photo': photo_url
        }
        db.reference('Resources').child('Manpower').child(manpower_id).set(manpower_data)
        return manpower_id

    def create_vehicle(self, photo_url):
        vehicle_id = self.generate_unique_id()
        vehicle_data = {
            'photo': photo_url
        }
        return vehicle_id

    def generate_unique_id(self):
        unique_id = str(uuid.uuid4()).replace('-', '')[:6] 
        return unique_id
    
    def get_location_name(self, latitude, longitude):
        location_infor = rg.search((latitude, longitude))
        if location_infor:
            location_name = location_infor[0]['name']
            return location_name
        return "CHECK MAP"
    
    
    def process_fires_with_location_names(self):
        fire_data = self.get_all_fires()
        if fire_data:
            for fire_id, fire_info in fire_data.items():
                latitude = fire_info.get('location', {}).get('latitude')
                longitude = fire_info.get('location', {}).get('longitude')
                if latitude is not None and longitude is not None:
                    location_name = self.get_location_name(latitude, longitude)
                    fire_info['location_name'] = location_name
                else:
                    fire_info['location_name'] = "Location not available"
            return fire_data
        else:
            return None

    # def process_fires_with_location_names(self):
    #     return "HAHA"
    
    def get_resources_info(self, id, type):
        remaining_resources = self.get_remaining_resources()
        manpower_data, vehicle_data = remaining_resources
        if type == "manpower":
            resource_info = manpower_data.get(id)
            return resource_info
        elif type == "vehicles":
            vehicle_info = vehicle_data.get(id)
            return vehicle_info