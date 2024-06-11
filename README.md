# Uptime Buddy

Uptime Buddy is in beta testing phase.
You can join the beta via TestFlight
[https://testflight.apple.com/join/okTxZGX1](https://testflight.apple.com/join/okTxZGX1)

Uptime Buddy is an uptime monitoring tool for your Apple Watch, designed to keep you informed about the status of your services. 
Uptime Buddy, requires a backend REST API.

<div style="display: flex; flex-wrap: wrap; gap: 20px;">
  <img src="images/uptime-buddy-2.png" alt="Apple Watch with Uptime Buddy" style="width:30%;">
  <img src="images/uptime-buddy-3.png" alt="Apple Watch with Uptime Buddy" style="width:30%;">
  <img src="images/uptime-buddy-5.png" alt="Apple Watch with Uptime Buddy" style="width:30%;">
</div>

<div style="display: flex; flex-wrap: wrap; gap: 20px;">
  <img src="images/uptime-buddy-1.png" alt="Apple Watch with Uptime Buddy" style="width:30%;">
  <img src="images/uptime-buddy-4.png" alt="Apple Watch with Uptime Buddy" style="width:30%;">
</div>


## Important changes
**Be sure to install the latest version of Uptime Buddy on your phone and app via TestFlight.**
**Pull the latest docker image, because the authentication implementation had breaking changes!**

## Installation via Docker

Uptime Buddy requires a running instance of [Uptime Kuma](https://github.com/louislam/uptime-kuma)!
Be sure to set up Uptime Kuma correctly and provide the address, username and password of your Uptime Kuma instance to the docker compose file.


Follow the steps below to set up the backend for Uptime Buddy.

## Prerequisites in the Uptime Buddy iOS-App

For authentication, start the Uptime Buddy iOS-App before you deploy the docker-container.
On first start, a token will be generated and displayed in the app.
Add the token to the docker-compose file or docker-run command.
Then deploy the container as described below.

## Docker Compose
Create a `docker-compose.yml` file with the following content to deploy the backend:

```yaml
services:
  uptime-buddy-api:
    image: schech1/uptime-buddy-api:latest
    ports:
      - "5005:5005"
    environment:
      - UPTIME_KUMA_URL=YOUR_UPTIME_KUMA_URL # e.g. http://192.168.1.34:3002/
      - USERNAME=YOUR_UPTIME_KUMA_USERNAME
      - PASSWORD=YOUR_UPTIME_KUMA_PASSWORD
      - TOKEN=SECRET_TOKEN # Created by iOS-App
```

The docker image supports `amd64` and `arm64` architecture.
Tested on Raspberry Pi 5 and Intel NUC 10.

Replace the environment variables with your actual Uptime Kuma URL, username, and password.

## Deploying the Backend
### Using docker-compose

Save the docker-compose.yml file.

Run the following command in the directory containing the docker-compose.yml file:

```sh
docker-compose up -d
```

This command will pull the necessary Docker image and start the backend service on port 5005.

### Using docker run (alternative)
```bash
docker run -d --name uptime-buddy-api -p 5005:5005 -e UPTIME_KUMA_URL=YOUR_UPTIME_KUMA_URL -e USERNAME=YOUR_UPTIME_KUMA_USERNAME -e PASSWORD=YOUR_UPTIME_KUMA_PASSWORD -e TOKEN=YOUR_TOKEN schech1/uptime-buddy-api:latest

```
## Settings on the iOS App
After deploying the Docker container, open the Uptime Buddy companion app on your iPhone and configure the backend URL.
Use the address of the server where you deployed this container, including the port (e.g., http://your-server-ip:5005).


<br>
<img src="images/uptime-buddy-ios.PNG" alt="Apple Watch with Uptime Buddy" style="width:30%;">


## The Apple Watch and iOS App

Uptime Buddy consists of an iOS app and an Apple Watch app.
The iOS app is needed to set up the backend adress.
When the iOS app is installed, the Apple Watch app can be install via the Watch app of the iPhone.

Uptime Buddy comes with Complication and SmartStack support.
The current update frequency of the Widgets is 15 minutes.
In future versions this will frequency will be individually adjustable, to extend battery life of the Apple Watch.

## Data Privacy

Uptime Buddy does not save, share or forward any data. The data that is fetched from the backend is only displayed on your device.
The Apple Watch or iOS apps do not store any data locally on the devices, except the address of your backend. This is needed to keep
setting over reboots. 

## Next planned Updates

- API token for backend authorization
- UI improvements on iOS app
- Better user feedback when backend is down




## Related Projects

This project is based on Uptime Kuma and uptime-kuma-api.

[Uptime Kuma](https://github.com/louislam/uptime-kuma): A self-hosted monitoring tool to monitor uptime for websites, applications and services.

[uptime-kuma-api](https://github.com/lucasheld/uptime-kuma-api): A Python API for Uptime Kuma.


## Contributing

Contributions are welcome.

## Support

If you encounter any issues or have questions, please open an issue on this GitHub repository.