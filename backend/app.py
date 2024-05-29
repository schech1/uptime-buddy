from flask import Flask, jsonify
from uptime_kuma_api import UptimeKumaApi
import os


app = Flask(__name__)



# Configure Uptime Kuma API client
UPTIME_KUMA_URL = os.getenv("UPTIME_KUMA_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not all([UPTIME_KUMA_URL, USERNAME, PASSWORD]):
    raise ValueError("UPTIME_KUMA_URL, USERNAME, and PASSWORD environment variables must be provided.")

# Initialize the Uptime Kuma API client
api = UptimeKumaApi(UPTIME_KUMA_URL)
api.login(USERNAME, PASSWORD)

@app.route('/monitors', methods=['GET'])
def get_monitors():
    try:
        monitors = api.get_monitors()
        response = []
        print(monitors)
        for monitor in monitors:
            # Extract required fields
            monitor_info = {
                "id": monitor.get("id"),
                "host": str(monitor.get("hostname")),
                "alias": monitor.get("name"),
                "online": monitor.get("active"),
                "interval": monitor.get("interval")
            }
            response.append(monitor_info)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/monitor/<int:monitor_id>/beats', methods=['GET'])
def get_beats(monitor_id):
    try:
        # Fetch the beats for the specified monitor ID
        heartbeats = api.get_monitor_beats(monitor_id, 24)
        return jsonify(heartbeats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/monitor/<int:monitor_id>', methods=['GET'])
def get_monitor(monitor_id):
    try:
        # Fetch the monitor details
        monitor = api.get_monitor(monitor_id)
        return jsonify(monitor)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5005)
