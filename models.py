from pydantic import BaseModel


class SensorData(BaseModel):
    temperature: float
    humidity: float
    soilMoisture: float


class RoverControl(BaseModel):
    cmd: str


class ActivateSensor(BaseModel):
    cmd: str