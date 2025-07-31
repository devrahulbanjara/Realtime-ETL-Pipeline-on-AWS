import boto3
import botocore.exceptions
import os

def create_kinesis_stream(stream_name, shard_count=1, region="us-east-1"):
    kinesis = boto3.client("kinesis", region_name=region)

    try:
        response = kinesis.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count
        )
        print(f"Creating Kinesis stream '{stream_name}' with {shard_count} shard(s)...")

        # Wait until stream becomes active
        waiter = kinesis.get_waiter('stream_exists')
        waiter.wait(StreamName=stream_name)
        print(f"Kinesis stream '{stream_name}' is now active.")

    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceInUseException':
            print(f"Stream '{stream_name}' already exists.")
        else:
            print(f"Failed to create stream: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "truck-sensor-stream")
    SHARD_COUNT = int(os.getenv("KINESIS_SHARD_COUNT", "1"))
    REGION = os.getenv("AWS_REGION", "us-east-1")

    if not STREAM_NAME:
        print("Error: KINESIS_STREAM_NAME environment variable not set.")
        exit(1)

    create_kinesis_stream(STREAM_NAME, SHARD_COUNT, REGION)