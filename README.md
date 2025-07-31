# Realtime ETL Pipeline on AWS

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Kinesis%20%7C%20Lambda%20%7C%20S3-orange.svg)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready, real-time ETL pipeline built on AWS for processing truck sensor data at scale. Ingests streaming sensor data from a fleet of trucks, processes it in real-time using AWS Lambda, and stores batched results in Amazon S3.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Truck Sensors  │───▶│  Data Producer  │───▶│  Kinesis Stream │───▶│ Lambda Consumer │
│   (Fleet Data)  │    │   (Simulator)   │    │   (Real-time)   │    │  (Batch Proc.)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                                                                    │
                                                                                    ▼
                                                                      ┌─────────────────┐
                                                                      │   Amazon S3     │
                                                                      │  (Data Lake)    │
                                                                      └─────────────────┘
```

### Components

- **Data Producer**: Python simulator generating truck sensor data
- **Amazon Kinesis**: Real-time data streaming service
- **AWS Lambda**: Serverless data processing and batching
- **Amazon S3**: Object storage for data persistence

## Features

- Real-time data ingestion from multiple trucks
- Auto-scaling Lambda functions for variable loads
- Intelligent batching (700 records per batch)
- Built-in error handling and retry mechanisms
- Cost-optimized serverless architecture
- Comprehensive sensor data capture (tire pressure, engine metrics, GPS, health status)

## Project Structure

```
Realtime-ETL-Pipeline-on-AWS/
├── infrastructure/
│   ├── kinesis_data_stream_setup.py   # Kinesis stream provisioning
│   └── s3_bucket_setup.py             # S3 bucket creation
├── lambda_consumer/
│   └── consumer.py                    # Data processing and batching
├── producer/
│   └── producer.py                    # Truck sensor data simulator
├── main.py                           # Application entry point
├── pyproject.toml                    # Project dependencies
├── .env.example                      # Environment template
└── README.md
```

## Prerequisites

- Python 3.8+
- UV Package Manager
- AWS Account with appropriate permissions
- AWS CLI configured

### Required AWS Permissions
- Amazon Kinesis (CreateStream, PutRecord, DescribeStream)
- AWS Lambda (CreateFunction, InvokeFunction, UpdateFunctionCode)
- Amazon S3 (CreateBucket, PutObject, GetObject)
- CloudWatch Logs (CreateLogGroup, CreateLogStream, PutLogEvents)

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/Realtime-ETL-Pipeline-on-AWS.git
cd Realtime-ETL-Pipeline-on-AWS
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your AWS configuration
```

### Environment Configuration
```bash
# AWS Configuration
region=us-east-1                           # AWS region for resources
stream_name=truck-sensor-stream            # Kinesis stream name
bucket_name=your-unique-bucket-name-2025   # S3 bucket (must be globally unique)
```

## Quick Start

### 1. Provision Infrastructure
```bash
python infrastructure/s3_bucket_setup.py
python infrastructure/kinesis_data_stream_setup.py
```

### 2. Deploy Lambda Function
Package and deploy the consumer Lambda function to AWS Lambda Console or via AWS CLI.

### 3. Start Data Generation
```bash
python producer/producer.py
```

### 4. Monitor Pipeline
- CloudWatch Logs: Monitor Lambda execution
- Kinesis Console: View stream metrics
- S3 Console: Verify batch file creation

## Configuration

### Kinesis Stream
- Shard Count: 1 shard (supports ~1,000 records/second)
- Retention Period: 24 hours
- Partition Key: Truck ID

### Lambda Function
- Runtime: Python 3.9+
- Memory: 512 MB
- Timeout: 5 minutes
- Batch Size: 100 records per invocation

### S3 Storage Pattern
```
sensor_data/
├── batch_2025-01-15T14-30-25_a1b2c3d4.json
├── batch_2025-01-15T14-31-02_e5f6g7h8.json
└── batch_2025-01-15T14-31-45_i9j0k1l2.json
```

## Data Schema

### Truck Sensor Record Structure
```json
{
  "truck_id": "TRUCK_001",
  "timestamp": "2025-01-15 14:30:25",
  "tire_pressure_fl": 32.5,
  "tire_pressure_fr": 31.8,
  "tire_pressure_rl": 33.2,
  "tire_pressure_rr": 32.1,
  "engine_temp": 95.7,
  "oil_pressure": 45.3,
  "fuel_level": 78.9,
  "brake_temp": 85.2,
  "transmission_temp": 82.4,
  "battery_voltage": 13.8,
  "coolant_temp": 88.1,
  "speed": 65.4,
  "engine_rpm": 2150,
  "miles_since_maintenance": 12450,
  "ambient_temp": 22.3,
  "vibration_level": 0.3,
  "fuel_consumption_rate": 8.7,
  "latitude": 27.717234,
  "longitude": 85.324567,
  "health_status": "NORMAL"
}
```

### Data Validation Rules
- Tire Pressure: 28.0 - 35.0 PSI
- Engine Temperature: 70.0 - 120.0°F
- Speed: 0 - 120 MPH
- Health Status: NORMAL | WARNING | URGENT

## Deployment

### Lambda Function Deployment

#### AWS Console Upload
```bash
cd lambda_consumer
zip -r ../lambda_function.zip .
```
Upload via AWS Lambda Console with handler set to `consumer.lambda_handler`.

#### AWS CLI Deployment
```bash
aws lambda create-function \
    --function-name truck-sensor-processor \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-execution-role \
    --handler consumer.lambda_handler \
    --zip-file fileb://lambda_function.zip

aws lambda create-event-source-mapping \
    --function-name truck-sensor-processor \
    --event-source-arn arn:aws:kinesis:REGION:ACCOUNT:stream/truck-sensor-stream \
    --starting-position LATEST \
    --batch-size 100
```

## Monitoring

### CloudWatch Metrics
- Kinesis: IncomingRecords, OutgoingRecords, WriteProvisionedThroughputExceeded
- Lambda: Duration, Errors, Throttles, IteratorAge
- S3: NumberOfObjects, BucketSizeBytes

### Alerting
Set up CloudWatch alarms for:
- Lambda function errors > threshold
- Kinesis iterator age > 30 seconds
- S3 upload failures

## Troubleshooting

### Common Issues

#### Stream not found error
```bash
aws kinesis describe-stream --stream-name truck-sensor-stream
```

#### Lambda function timeout
```bash
aws lambda update-function-configuration \
    --function-name truck-sensor-processor \
    --timeout 300
```

#### S3 access denied
```bash
aws iam attach-role-policy \
    --role-name lambda-execution-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

## Performance Considerations

### Throughput Optimization
- Kinesis Shards: Scale based on ingestion rate (1,000 records/second per shard)
- Lambda Concurrency: Configure reserved concurrency to prevent throttling
- Batch Size: Optimize for cost-effective S3 operations

### Cost Optimization
- S3 Storage Classes: Use Intelligent Tiering
- Lambda Memory: Right-size based on processing requirements
- Kinesis Retention: Adjust based on replay requirements

### Scaling Recommendations
| Metric | Threshold | Action |
|--------|-----------|--------|
| Records/sec | > 800 per shard | Add Kinesis shards |
| Lambda Duration | > 4 minutes | Increase memory allocation |
| Error Rate | > 1% | Investigate root cause |
| S3 Upload Latency | > 5 seconds | Check network and IAM permissions |

## Security

### IAM Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:PutRecord",
        "kinesis:PutRecords"
      ],
      "Resource": "arn:aws:kinesis:*:*:stream/truck-sensor-stream"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

### Data Encryption
- In Transit: TLS encryption for all AWS services
- At Rest: S3 default encryption (AES-256 or KMS)
- Kinesis: Server-side encryption with AWS KMS

### Network Security
- Deploy Lambda functions in VPC for isolation
- Use VPC endpoints for AWS service communication
- Implement proper security groups and NACLs

## Advanced Features

### Auto-scaling Configuration
```python
def get_optimal_batch_size(record_count):
    if record_count < 100:
        return 50
    elif record_count < 500:
        return 200
    else:
        return 700
```

### Data Partitioning
```
s3://bucket/year=2025/month=01/day=15/hour=14/batch_*.json
```

### Real-time Analytics Integration
- Amazon Kinesis Analytics: SQL queries on streaming data
- Amazon QuickSight: Real-time dashboards
- Amazon Elasticsearch: Log analytics and search

## Contributing

### Development Setup
```bash
git clone https://github.com/devrahulbanjara/Realtime-ETL-Pipeline-on-AWS
git checkout -b feature/your-feature-name
uv sync
```

### Contribution Process
1. Create an issue describing the enhancement or bug
2. Use descriptive branch names (`feature/add-monitoring`, `fix/lambda-timeout`)
3. Ensure code passes linting and tests
4. Update documentation as needed
5. Submit PR with clear description

## License

This project is licensed under the GPL License. See the [LICENSE](LICENSE) file for details.

---

*This is a learning project*
*Last Updated: July 2025*