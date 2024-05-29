# uptime-buddy
Uptime monitoring on Apple Watch

# Installation via Docker

After you installed the UptimeBuddy-App from Apple AppStore, you should deploy a backend for the app to talk to.
This also requires that you have a running instance of uptime-kuma.

## Docker compose

```yaml
version: '3.8'

services:
  uptime-buddy-api:

    image: schech1/uptime-buddy-api:beta
    ports:
      - "5005:5005"
    environment:
      - UPTIME_KUMA_URL=YOUR_UPTIME_KUMA_URL # e.g. http://192.168.1.34:3002/
      - USERNAME=YOUR_UPTIME_KUMA_USERNAME
      - PASSWORD=YOUR_UPTIME_KUMA_PASSWORD
```

## Settings on the iOS-App
After deploying the docker container, set the address of the service as the backend url.
The container runs on port 5005.