# Apollo Tracker

Apollo Tracker is a lightweight Flask middleware for tracking and reporting errors to **Apollo**, an internal error tracking system similar to Sentry.

## Features

- 🛠 **Automatic Error Tracking**: Captures and reports all unhandled exceptions.
- 🚀 **Flask Integration**: Works seamlessly with Flask applications.
- 📡 **Send Errors to Apollo**: Forwards error logs to an Apollo backend.
- 🔍 **Includes Request Metadata**: Logs IP address, user agent, endpoint, and method.
- 📦 **Simple Installation**: Just `pip install apollo-tracker`.

## Installation

You can install `apollo-tracker` using `pip`:

```bash
pip install apollo-tracker
```

## Usage

### 1. Setup `ApolloTracker` in Your Flask App

To start tracking errors in your Flask app, follow these steps:

1. **Import the ApolloTracker class**:
    ```python
    from apollo_tracker import ApolloTracker
    ```

2. **Initialize the tracker with your service name**:
    ```python
    tracker = ApolloTracker(service_name="my-flask-service")
    ```

3. **Register the error handler**:
    ```python
    tracker.register_error_handler(app)
    ```

### 2. Example Flask App Setup

```python
from flask import Flask
from apollo_tracker import ApolloTracker  # import the tracker class

app = Flask(__name__)

# Initialize ApolloTracker with your service name
tracker = ApolloTracker(service_name="my_project_id")

# Register the error handler to track errors globally
tracker.register_error_handler(app)

@app.route('/')
def home():
    # Simulate an error
    1 / 0  # This will raise a ZeroDivisionError

if __name__ == "__main__":
    app.run(debug=True)
```

### 3. Error Handling

- The `ApolloTracker` class automatically captures unhandled exceptions in your Flask app.
- When an error occurs, it sends detailed information (like the error type, message, stack trace, request path, and user agent) to the Apollo server.

## Configuration

The `APOLLO_URL` is defined by default in the `ApolloTracker` class as:

```python
APOLLO_URL = "https://apollo.tornixtech.com/api/errors"
```

You don't need to change this unless necessary, as the class will automatically use this URL to send error logs.

---

This should integrate smoothly with your existing `README.md` and provide clear setup instructions for users. Let me know if you need any other adjustments!