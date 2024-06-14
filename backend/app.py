from flask import Flask, jsonify, request, abort
from uptime_kuma_api import UptimeKumaApi, MonitorStatus
import os
import datetime


app = Flask(__name__)

# Configure Uptime Kuma API client
UPTIME_KUMA_URL =  "http://192.168.1.34:3002" # os.getenv("UPTIME_KUMA_URL") 
USERNAME = "test" #os.getenv("USERNAME")
PASSWORD = "123" # os.getenv("PASSWORD")
TOKEN = "123" # os.getenv("TOKEN")
MFA = True

if not all([UPTIME_KUMA_URL, USERNAME, PASSWORD, TOKEN]):
    raise ValueError("UPTIME_KUMA_URL, USERNAME, and PASSWORD environment variables must be provided.")

if not MFA:
    # Initialize the Uptime Kuma API client
    api = UptimeKumaApi(UPTIME_KUMA_URL)
    tkn = api.login(USERNAME, PASSWORD, token="612539")
    print(tkn)
    api.login_by_token(tkn)



def require_api_token(func):
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        if token != TOKEN:
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


stored_tokens = {}

@app.route('/mfasetup', methods=['POST'])
def setup_mfa():
    data = request.json
    if not data or 'token' not in data:
        return jsonify({"error": "Token is required"}), 400
    
    token = data['token']
    print(token)
    
    user_id = 'user123'
    stored_tokens[user_id] = token
    
    return jsonify({"message": "2FA token stored successfully"}), 200


@app.route('/monitors', methods=['GET'])
@require_api_token
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
                "lastUpdate": iso_utc_now,
                "type": monitor.get("type")
            }
            response.append(monitor_info)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
@require_api_token
def status():
    return jsonify({"status": "available"}), 200


@app.route('/monitor/<int:monitor_id>/beats', methods=['GET'])
@require_api_token
def get_beats(monitor_id):
    try:
        # Fetch the beats for the specified monitor ID
        heartbeats = api.get_monitor_beats(monitor_id, 12)
        last_10_heartbeats = heartbeats[-10:]
        return jsonify(last_10_heartbeats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/online_hosts', methods=['GET'])
@require_api_token
def online_hosts():
    try:
        online_count = 0
        total_count = 0
        monitors = api.get_monitors()
        for monitor in monitors:
            heartbeats = api.get_monitor_beats(monitor.get("id"), 12)
            if heartbeats:
                last_heartbeat = heartbeats[-1]  # Get the last heartbeat
                if last_heartbeat.get("status") == MonitorStatus.UP:
                    online_count += 1
            total_count += 1
        return jsonify({"on": online_count, "total": total_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/monitor/<int:monitor_id>', methods=['GET'])
@require_api_token
def get_monitor(monitor_id):
    try:
        # Fetch the monitor details
        monitor = api.get_monitor(monitor_id)
        return jsonify(monitor)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5005)
