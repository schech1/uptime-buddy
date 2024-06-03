from flask import Flask, jsonify
from uptime_kuma_api import UptimeKumaApi
import os
import datetime


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
             # Get the current time in UTC and format it as ISO 8601
            utc_now = datetime.datetime.utcnow()
            iso_utc_now = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            # Extract required fields
            monitor_info = {
                "id": monitor.get("id"),
                "host": str(monitor.get("hostname")),
                "alias": monitor.get("name"),
                "online": monitor.get("active"),
                "interval": monitor.get("interval"),
                "lastUpdate": iso_utc_now
            }
            response.append(monitor_info)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "available"}), 200

@app.route('/monitor/<int:monitor_id>/beats', methods=['GET'])
def get_beats(monitor_id):
    try:
        # Fetch the beats for the specified monitor ID
        heartbeats = api.get_monitor_beats(monitor_id, 12)
        last_10_heartbeats = heartbeats[-10:]
        return jsonify(last_10_heartbeats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/online_hosts', methods=['GET'])
def online_hosts():
    try:
        online_count = 0
        total_count = 0
        monitors = api.get_monitors()
        for monitor in monitors:
            heartbeats = api.get_monitor_beats(monitor.get("id"), 12)
            last_10_heartbeats = heartbeats[-10:]
            for heartbeat in last_10_heartbeats:
                if heartbeat.get("status") == "<MonitorStatus.UP: 1>":
                    online_count += 1
            total_count += 1
        return jsonify({"online_hosts": online_count, "total_monitors": total_count})
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
