import requests
import traceback
import datetime
from flask import request, jsonify

# Apollo API endpoint (update to your Apollo server)
APOLLO_URL = "https://apollo.tornixtech.com/api/errors"

class ApolloTracker:
    def __init__(self, service_name, apollo_url=APOLLO_URL):
        self.service_name = service_name
        self.apollo_url = apollo_url

    def send_error(self, error_data):
        """Send error logs to Apollo"""
        try:
            response = requests.post(self.apollo_url, json=error_data)
            return response.status_code
        except requests.RequestException as e:
            print("Failed to send error to Apollo:", e)

    def handle_exception(self, e):
        """Capture and send errors"""
        error_data = {
            "service": self.service_name,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "error_type": type(e).__name__,
            "message": str(e),
            "stack_trace": traceback.format_exc(),
            "endpoint": request.path,
            "method": request.method,
            "ip": request.remote_addr,
            "user_agent": request.headers.get("User-Agent")
        }

        self.send_error(error_data)
        return jsonify({"error": "Internal Server Error"}), 500

    def register_error_handler(self, app):
        """Attach error handler to a Flask app"""
        app.register_error_handler(Exception, self.handle_exception)
