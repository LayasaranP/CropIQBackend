from fastapi import FastAPI, status, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from models import SensorData, RoverControl, ActivateSensor
from pydantic import ValidationError
from typing import Optional

app = FastAPI(
    title="ESP32 Server",
    description="Handles ESP32 sensor data and rover control commands",
    version="1.0.0",
)

templates = Jinja2Templates(directory='templates')

latest_data: Optional[SensorData] = None
rover_command = "STOP"
sensor_cmd = ""


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "Internal server error", "details": str(exc)},
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "CropIQ Home"
    })


@app.post("/sensor-data", status_code=status.HTTP_200_OK)
async def get_sensor_data_esp32(data: SensorData):
    try:
        global latest_data
        latest_data = data
        return {
            "status": "success",
            "message": "Sensor data received successfully",
            "received_data": data.dict()
        }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@app.get("/latest-sensor-data", status_code=status.HTTP_200_OK)
async def send_data_client_client():
    # if latest_data is None:
    #     raise HTTPException(status_code=404, detail="No sensor data received yet")
    # num1 = random.randrange(20, 30, 3)
    # num2 = random.randrange(20, 30, 3)
    # num3 = random.randrange(20, 30, 3)

    sensor = {
        "temperature": num1,
        "humidity": num2,
        "soil_moisture": num3
    }
    return {
        "status": "success",
        "message": "Latest sensor data retrieved successfully",
        "latest_data": sensor
    }


@app.post("/rover-control", status_code=status.HTTP_200_OK)
async def get_rover_control_client(cmd: RoverControl):
    try:
        global rover_command
        rover_command = cmd.cmd
        print(rover_command)
        return {
            "status": "success",
            "message": "Rover command received successfully",
            "rover_control": cmd.dict()
        }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@app.get("/arduino-command", status_code=status.HTTP_200_OK)
async def send_rover_command_esp32():
    return {
        "status": "success",
        "message": "Rover command retrieved successfully",
        "command": rover_command
    }


@app.post("/activate-soil-moisture", status_code=status.HTTP_200_OK)
async def get_sensor_command_client(command: ActivateSensor):
    try:
        global sensor_cmd
        sensor_cmd = command.cmd
        print(sensor_cmd)
        return {
            "status": "success",
            "message": "Soil moisture command received successfully",
            "sensor_command": sensor_cmd
        }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@app.get("/deploy-soil-moisture", status_code=status.HTTP_200_OK)
async def send_command_to_esp32():
    if not sensor_cmd:
        raise HTTPException(status_code=404, detail="No soil moisture command available")
    return {
        "status": "success",
        "message": "Soil moisture command retrieved successfully",
        "command": sensor_cmd
    }
