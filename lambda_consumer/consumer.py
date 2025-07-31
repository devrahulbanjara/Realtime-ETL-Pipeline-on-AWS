import boto3
import json
import base64
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client("s3")
bucket_name = os.getenv("bucket_name")
final_prefix = "sensor_data/batch_"
buffer_cache = []

if not bucket_name:
    print("Error: 'bucket_name' not set in environment variables.")
    exit(1)

def lambda_handler(event, context):
    # Decode and parse incoming Kinesis records
    records = []
    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"])
        try:
            records.append(json.loads(payload))
        except:
            print("Invalid JSON payload.")
    
    print(f"Received {len(records)} records")

    # Add to buffer
    buffer_cache.extend(records)
    print(f"Buffer now has {len(buffer_cache)} records")

    if len(buffer_cache) >= 700:
        batch = buffer_cache[:700]
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        uid = uuid.uuid4().hex[:8]
        s3_key = f"{final_prefix}{timestamp}_{uid}.json"

        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(batch)
        )
        print(f"Uploaded 700-record batch to {s3_key}")

        # Remove flushed records efficiently
        del buffer_cache[:700]
        print(f"Buffer now has {len(buffer_cache)} remaining records")

    return {"statusCode": 200}