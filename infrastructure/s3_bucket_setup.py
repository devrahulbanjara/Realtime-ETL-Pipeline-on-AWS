import boto3
import botocore.exceptions
import os
from dotenv import load_dotenv

def create_bucket(name, region="us-east-1"):
    s3 = boto3.client("s3", region_name=region)

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=name)
        else:
            s3.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"Bucket '{name}' created successfully.")

    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "BucketAlreadyOwnedByYou":
            print(f"Bucket '{name}' already exists and is owned by you.")
        elif error_code == "BucketAlreadyExists":
            print(f"Bucket '{name}' already exists globally. Choose a unique name.")
        else:
            print(f"Failed to create bucket: {e}")

if __name__ == "__main__":
    load_dotenv()

    bucket_name = os.getenv("BUCKET_NAME")
    region = os.getenv("AWS_REGION", "us-east-1")

    if not bucket_name:
        print("Error: 'BUCKET_NAME' environment variable not set.")
        exit(1)

    create_bucket(bucket_name, region)