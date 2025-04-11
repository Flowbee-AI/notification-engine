# Notification Engine

A notification engine using Celery and OneSignal for delivering notifications through multiple channels.

## Architecture

This system consists of two main components:

1. **API Server**: A FastAPI application that provides endpoints for submitting notification requests.
2. **Worker**: A Celery worker that processes notification tasks and sends them through OneSignal.

Both components use RabbitMQ as the message broker.

## Prerequisites

- Python 3.10+
- Poetry (dependency management)
- RabbitMQ
- MongoDB
- Docker & Docker Compose (optional, for containerized deployment)

## Configuration

Create a `.env` file in the root directory with the following environment variables:

```
# Environment
ENVIRONMENT=development
LOG_LEVEL=DEBUG
HEALTH_CHECK_PORT=8080

# MongoDB settings
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=notifications

# RabbitMQ settings
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
RABBITMQ_QUEUE_NAME=notification_queue
RABBITMQ_SSL=false
RABBITMQ_PREFETCH_COUNT=10
RABBITMQ_RETRY_COUNT=3
RABBITMQ_RETRY_DELAY=5

# OneSignal settings
ONESIGNAL_APP_ID=your-app-id
ONESIGNAL_REST_API_KEY=your-rest-api-key
ONESIGNAL_API_URL=https://onesignal.com/api/v1
ONESIGNAL_MAX_RETRIES=3
ONESIGNAL_RETRY_DELAY=1
```

## Installation

### Using Poetry

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Running the Application

### Local Development

1. Start the API server:

   ```bash
   python -m src.notification_engine.main
   ```

2. Start the Celery worker:
   ```bash
   celery -A src.notification_engine.worker worker --loglevel=info
   ```

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Build and start specific services
docker-compose up --build api worker

# Run in detached mode
docker-compose up -d
```

## API Usage

### Send a Notification

```bash
curl -X POST http://localhost:8000/api/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "contents": {"en": "Hello world"},
    "headings": {"en": "Test Notification"},
    "data": {"type": "test"},
    "external_ids": ["user123"]
  }'
```

Response:

```json
{
  "task_id": "5a4c194c-5a72-4e43-ba76-8b516f31aaf5",
  "status": "queued"
}
```

### Check Notification Status

```bash
curl http://localhost:8000/api/notifications/status/5a4c194c-5a72-4e43-ba76-8b516f31aaf5
```

Response:

```json
{
  "task_id": "5a4c194c-5a72-4e43-ba76-8b516f31aaf5",
  "status": "SUCCESS",
  "result": {
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "recipients": 1,
    "external_id": null
  }
}
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

Response:

```json
{
  "status": "healthy"
}
```

## Testing

Run the test script to send a test notification:

```bash
python -m src.notification_engine.scripts.test_notification
```

## Project Structure

```
notification-engine/
├── src/
│   └── notification_engine/
│       ├── config/
│       │   └── onesignal_config.py
│       ├── modules/
│       │   └── queue/
│       │       ├── rabbitmq.py
│       │       ├── queue_service.py
│       │       └── worker.py
│       └── main.py
├── pyproject.toml
└── README.md
```

## License

ISC

be63e7fa-9b09-4e83-bf5b-066dec89f53e
zOurXVGUcUgvrUeDcbDFXx6T0FI3
