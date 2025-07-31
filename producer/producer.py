import boto3
import json
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv("region")
stream_name = os.getenv("stream_name")

if not region_name or not stream_name:
    print("Error: 'region_name' or 'stream_name' not set in environment variables.")
    exit(1)

kinesis = boto3.client("kinesis", region_name=region_name)

def simulate_truck_data(truck_id):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    base_lat = 27.7172
    base_lon = 85.3240

    return {
        "truck_id": f"TRUCK_{str(truck_id).zfill(3)}",
        "timestamp": now,
        "tire_pressure_fl": round(random.uniform(28.0, 35.0), 2),
        "tire_pressure_fr": round(random.uniform(28.0, 35.0), 2),
        "tire_pressure_rl": round(random.uniform(28.0, 35.0), 2),
        "tire_pressure_rr": round(random.uniform(28.0, 35.0), 2),
        "engine_temp": round(random.uniform(70.0, 120.0), 2),
        "oil_pressure": round(random.uniform(20.0, 80.0), 2),
        "fuel_level": round(random.uniform(0.0, 100.0), 2),
        "brake_temp": round(random.uniform(70.0, 250.0), 2),
        "transmission_temp": round(random.uniform(70.0, 250.0), 2),
        "battery_voltage": round(random.uniform(11.5, 14.5), 2),
        "coolant_temp": round(random.uniform(70.0, 130.0), 2),
        "speed": round(random.uniform(0, 120), 2),
        "engine_rpm": random.randint(600, 4000),
        "miles_since_maintenance": random.randint(0, 20000),
        "ambient_temp": round(random.uniform(-10.0, 45.0), 2),
        "vibration_level": round(random.uniform(0.0, 1.5), 2),
        "fuel_consumption_rate": round(random.uniform(5.0, 15.0), 2),
        "latitude": round(base_lat + random.uniform(-0.01, 0.01), 6),
        "longitude": round(base_lon + random.uniform(-0.01, 0.01), 6),
        "health_status": random.choice(["NORMAL", "WARNING", "URGENT"])
    }
    
def start_streaming():
    counter = 1
    while counter<=30:
        for truck_id in range(1, 11):
            data = simulate_truck_data(truck_id)
            kinesis.put_record(
                StreamName=stream_name,
                Data=json.dumps(data),
                PartitionKey=str(truck_id)
            )
            print(f"[{counter}] Sent data for Truck-{truck_id}: {data['timestamp']}")
        time.sleep(1)
        counter += 1
    return None

if __name__ == "__main__":
    start_streaming()