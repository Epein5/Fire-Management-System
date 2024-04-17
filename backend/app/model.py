from pydantic import BaseModel

class FireCreate(BaseModel):
    name: str
    photo_url: str

class VehicleCreate(BaseModel):
    photo_url: str

class AssignResourcesRequest(BaseModel):
    fire_id: str
    manpower_data: list[str]
    vehicle_data: list[str]