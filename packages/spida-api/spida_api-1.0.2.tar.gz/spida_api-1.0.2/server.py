import os

import requests
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from dotenv import load_dotenv

from spida_api.spida_api import SpidaAPI
from spida_api.webhook_client import WebhookClient

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
socketio = SocketIO(app, cors_allowed_origins="*")

# Read SPIDA API values from .env
SPIDA_SERVER = os.getenv("SPIDA_SERVER")
SPIDA_API_KEY = os.getenv("SPIDA_API_KEY")
SPIDA_USERNAME = os.getenv('SPIDA_USERNAME')
SPIDA_PASSWORD = os.getenv('SPIDA_PASSWORD')
SPIDA_COMPANY_ID = os.getenv('SPIDA_COMPANY_ID')

spida_api = SpidaAPI(SPIDA_USERNAME, SPIDA_PASSWORD, SPIDA_SERVER)
spida_api.switch_company(SPIDA_COMPANY_ID)
# Initialize Webhook Client
client = WebhookClient(url_server=SPIDA_SERVER, api_key=SPIDA_API_KEY)

# Store webhook events in memory (You could use Redis or a database instead)
webhook_events = []

@app.route("/api/get_form/<form_id>", methods=["GET"])
def get_form(form_id):
    response_json = spida_api.get_form(form_id)

    return jsonify(response_json)

@app.route("/api/update_form", methods=["PUT"])
def update_form():
    data = request.get_json()
    form_id = data.get("formId")

    if not form_id:
        return jsonify({"error": "Missing formId"}), 400

    response_json = spida_api.update_form(form_id, data["form"])

    return jsonify(response_json)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/view_webhooks", methods=["GET"])
def view_webhooks():
    response = client.view_webhooks()

    try:
        return jsonify(response.json())
    except requests.exceptions.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from SPIDA API", "status_code": response.status_code,
                        "text": response.text}), 500


@app.route("/api/register_webhook", methods=["POST"])
def register_webhook():
    data = request.get_json()

    response = client.register_webhook(
        target_url=data["url"],
        channel=data["channel"],
        event=data.get("event", ".*")  # Default to ".*" if not provided
    )

    return jsonify(response.json())


@app.route("/api/unregister_webhook", methods=["POST"])
def unregister_webhook():
    data = request.get_json()
    client.unregister_webhook(data["hook_ids"])
    return jsonify({"status": "success"})


@app.route("/webhooks", methods=["POST"])
def receive_webhook():
    """Handles incoming webhook events from SPIDA."""
    data = request.json
    webhook_events.insert(0, data)  # Store event (newest first)

    # Limit stored events to 100 to prevent excessive memory usage
    if len(webhook_events) > 100:
        webhook_events.pop()

    # Broadcast event to all connected clients
    socketio.emit("new_webhook_event", data)
    print(f"Received webhook event: {data}")

    return jsonify({"status": "received"}), 200


@app.route("/api/webhook_events", methods=["GET"])
def get_webhook_events():
    """Returns the list of received webhook events."""
    return jsonify({"events": webhook_events})


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5003)
