# Notification Engine

A Python-based notification system using RabbitMQ and OneSignal.

## Features

- Asynchronous message processing
- RabbitMQ integration for message queuing
- OneSignal integration for push notifications
- Singleton pattern implementation for resource management
- Environment-based configuration

## Prerequisites

- Python 3.9+
- Poetry
- RabbitMQ server
- OneSignal account

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd notification-engine
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Create a `.env` file with the following variables:

```env
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
ONESIGNAL_APP_ID=your_app_id
ONESIGNAL_API_KEY=your_api_key
```

## Usage

1. Activate the Poetry environment:

```bash
poetry shell
```

2. Run the application:

```bash
python -m src.notification_engine.main
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