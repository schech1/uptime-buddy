#!/bin/bash

# Install Python and pip (if not already installed)
sudo apt update
sudo apt install -y python3 python3-pip

# Install virtualenv (if not already installed)
sudo apt install -y python3-venv

# Navigate to the application directory
cd /opt/uptime-mate/backend/

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/uptime-buddy.service > /dev/null <<EOF
[Unit]
Description=Uptime Buddy Flask Application
After=network.target

[Service]
User=<your_username>
WorkingDirectory=/opt/uptime-mate/backend/
Environment="UPTIME_KUMA_URL=<your_uptime_kuma_url>"
Environment="USERNAME=<your_username>"
Environment="PASSWORD=<your_password>"
Environment="TOKEN=<your_token>"
Environment="MFA=<your_mfa_value>"
ExecStart=/opt/uptime-mate/backend/venv/bin/python /opt/uptime-mate/backend/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Replace placeholders with actual values in the service file
sudo sed -i "s|<your_username>|$(whoami)|g" /etc/systemd/system/uptime-buddy.service
sudo sed -i "s|<your_uptime_kuma_url>|http://192.168.34:3002|g" /etc/systemd/system/uptime-buddy.service  # Replace with your actual URL
sudo sed -i "s|<your_username>|christoph|g" /etc/systemd/system/uptime-buddy.service  # Replace with your actual username
sudo sed -i "s|<your_password>|12345678A|g" /etc/systemd/system/uptime-buddy.service  # Replace with your actual password
sudo sed -i "s|<your_token>|dbl3z7|g" /etc/systemd/system/uptime-buddy.service  # Replace with your actual token
sudo sed -i "s|<your_mfa_value>|false|g" /etc/systemd/system/uptime-buddy.service  # Replace with your actual MFA value

# Reload systemd
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable uptime-buddy
sudo systemctl start uptime-buddy

echo "Uptime Buddy setup complete."