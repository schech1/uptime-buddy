import logging
from flask import Flask, jsonify, request, abort
from uptime_kuma_api import UptimeKumaApi, MonitorStatus
import os
import datetime
from waitress import serve
import platform,json,psutil,cpuinfo

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.port = 5005
        self.setup_logging()
        self.configure_api_client()
        self.setup_routes()
        
    def setup_logging(self):
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_format)
        self.logger = logging.getLogger(__name__)

    def configure_api_client(self):
        self.UPTIME_KUMA_URL = os.getenv("UPTIME_KUMA_URL")
        self.USERNAME = os.getenv("USERNAME")
        self.PASSWORD = os.getenv("PASSWORD")
        self.TOKEN = os.getenv("TOKEN")
        self.MFA = os.getenv("MFA")
        self.LOGIN_TOKEN = ""

        if not all([self.UPTIME_KUMA_URL, self.TOKEN]):
            raise ValueError("UPTIME_KUMA_URL and TOKEN environment variables must be provided.")

        # Initialize the Uptime Kuma API client    
        self.api = UptimeKumaApi(self.UPTIME_KUMA_URL)
        if self.MFA == "false" or self.MFA is None:
            tkn = self.api.login(self.USERNAME, self.PASSWORD)
            if tkn:
                self.logger.info("Successfully connected to Uptime Kuma instance")
            else:
                self.logger.warning("Could not connect to Uptime Kuma instance. Check URL and credentials!")

        elif self.MFA == "true":
            self.logger.info("You have MFA enabled in UptimeKuma. Make sure to apply the MFA token in the Uptime Mate iOS-App")
        else:
            self.logger.info("Invalid value for MFA. Allowed values true/false")
            
    def require_api_token(self, func):
        def wrapper(*args, **kwargs):
            token = request.args.get('token')
            if token != self.TOKEN:
                self.logger.warning("Forbidden access attempt with token: %s", token)
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def setup_routes(self):
        @self.app.route('/mfasetup', methods=['POST'])
        @self.require_api_token
        def setup_mfa():
            self.logger.info("Accessing /mfasetup endpoint")
            if not self.LOGIN_TOKEN:
                data = request.json
                if not data or '2facode' not in data:
                    self.logger.error("2FA Code is required")
                    return jsonify({"error": "2FA Code is required"}), 400
                
                token = data.get('2facode', '').strip()
                if not token:
                    self.logger.error("2FA Code cannot be empty")
                    return jsonify({"error": "2FA Code cannot be empty"}), 400
                
                try:
                    self.LOGIN_TOKEN = self.api.login(self.USERNAME, self.PASSWORD, token=token)
                except Exception as e:
                    self.logger.error("Wrong 2FA token: %s", str(e))
                    return jsonify({"message": "Wrong 2FA token"}), 403
            else:
                self.logger.info("MFA already set up")
                return jsonify({"message": "MFA already set up"}), 403  

            self.logger.info("2FA token stored successfully")
            return jsonify({"message": "2FA token stored successfully"}), 200

        @self.app.route('/monitors', methods=['GET'])
        @self.require_api_token
        def get_monitors():
            self.logger.info("Accessing /monitors endpoint")
            try:
                monitors = self.api.get_monitors()
                response = []
                for monitor in monitors:
                    # Get the current time in UTC and format it as ISO 8601
                    utc_now = datetime.datetime.utcnow()
                    iso_utc_now = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    # Extract required fields
                    monitor_info = {
                        "id": monitor.get("id"),
                        "host": str(monitor.get("hostname")),
                        "alias": monitor.get("name"),
                        "active": monitor.get("active"),
                        "interval": monitor.get("interval"),
                        "lastUpdate": iso_utc_now,
                        "type": monitor.get("type")
                    }
                    response.append(monitor_info)
                return jsonify(response)
            except Exception as e:
                self.logger.error("Error in /monitors: %s", str(e))
                return jsonify({"error": str(e)}), 500

        @self.app.route('/status', methods=['GET'])
        @self.require_api_token
        def status():
            self.logger.info("Accessing /status endpoint")
            return jsonify({"status": "available"}), 200

        @self.app.route('/monitor/<int:monitor_id>/beats', methods=['GET'])
        @self.require_api_token
        def get_beats(monitor_id):
            self.logger.info("Accessing /monitor/%d/beats endpoint", monitor_id)
            try:
                # Fetch the beats for the specified monitor ID
                heartbeats = self.api.get_monitor_beats(monitor_id, 12)
                last_10_heartbeats = heartbeats[-10:]
                return jsonify(last_10_heartbeats)
            except Exception as e:
                self.logger.error("Error in /monitor/%d/beats: %s", monitor_id, str(e))
                return jsonify({"error": str(e)}), 500

        @self.app.route('/online_hosts', methods=['GET'])
        @self.require_api_token
        def online_hosts():
            self.logger.info("Accessing /online_hosts endpoint")
            try:
                online_count = 0
                total_count = 0
                paused_count = 0
                monitors = self.api.get_monitors()
                for monitor in monitors:
                    if not monitor.get("active"):
                        paused_count +=1
                    heartbeats = self.api.get_monitor_beats(monitor.get("id"), 12)
                    if heartbeats:
                        last_heartbeat = heartbeats[-1]  # Get the last heartbeat
                        if last_heartbeat.get("status") == MonitorStatus.UP and monitor.get("active"):
                            online_count += 1
                    total_count += 1
                return jsonify({"on": online_count, "total": total_count, "paused": paused_count})
            except Exception as e:
                self.logger.error("Error in /online_hosts: %s", str(e))
                return jsonify({"error": str(e)}), 500

        @self.app.route('/monitor/<int:monitor_id>', methods=['GET'])
        @self.require_api_token
        def get_monitor(monitor_id):
            self.logger.info("Accessing /monitor/%d endpoint", monitor_id)
            try:
                # Fetch the monitor details
                monitor = self.api.get_monitor(monitor_id)
                return jsonify(monitor)
            except Exception as e:
                self.logger.error("Error in /monitor/%d: %s", monitor_id, str(e))
                return jsonify({"error": str(e)}), 500




        @self.app.route('/system', methods=['GET'])
        @self.require_api_token
        def getSystemInfo():
            self.logger.info("Accessing /system endpoint")
            systemInfo = {}

            # Determine OS name
            pName = platform.uname().system
            if "darwin" in pName.lower():
                pName = "macOS"
            
            # System Information
            systemInfo["os"] = pName
            systemInfo["osArch"] = platform.uname().machine

            # CPU Information
            systemInfo["cpu"] = cpuinfo.get_cpu_info()["brand_raw"]
            systemInfo["cpuCores"] = psutil.cpu_count(logical=False)
            systemInfo["cpuThreads"] = psutil.cpu_count(logical=True)

            # RAM Information
            ram = psutil.virtual_memory()
            systemInfo["ram"] = round(ram.total / 1024**3, 2)
            systemInfo["ramPercent"] = round(ram.percent, 2)

            # Disk Information
            disk = psutil.disk_usage("/")
            systemInfo["disk"] = round(disk.total / 1024**3, 2)
            systemInfo["diskUsed"] = round((disk.total - disk.free) / 1024**3, 2)
            systemInfo["diskFree"] = round(disk.free / 1024**3, 2)
            systemInfo["diskPercent"] = round((disk.total - disk.free) / disk.total * 100, 2)
            systemInfo["cputemp"]  = psutil.sensors_temperatures()

            # Backend version
            version_file_path = '/app/VERSION'

            try:
                with open(version_file_path) as version_file:
                    app_version = version_file.read().strip()
                    systemInfo["version"] = app_version[1:]

            except FileNotFoundError:
                self.logger.info(f"VERSION file not found at {version_file_path}")

        
            return jsonify(systemInfo)





    def run(self):
        self.logger.info("Starting the backend...")
        serve(self.app, host="0.0.0.0", port=self.port, threads=8)
        self.logger.info(f"Uptime Mate backend started on port: {self.port}")

if __name__ == "__main__":
    main = Main()
    main.run()