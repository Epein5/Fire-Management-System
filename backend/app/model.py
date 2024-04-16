from pydantic import BaseModel

class FireCreate(BaseModel):
    name: str
    photo_url: str

class VehicleCreate(BaseModel):
    photo_url: str
