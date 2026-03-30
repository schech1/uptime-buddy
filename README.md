# Uptime Mate


<p align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/schech1/uptime-buddy?style=flat">
<a href="https://hub.docker.com/r/schech1/uptime-buddy-api"><img src="https://img.shields.io/docker/pulls/schech1/uptime-buddy-api" alt="Docker pulls"></a>
<img alt="Static Badge" src="https://img.shields.io/badge/OS-WatchOS-green">
<img alt="Static Badge" src="https://img.shields.io/badge/OS-iOS-green">
<a target="_blank" href="https://github.com/schech1/uptime-buddy"><img src="https://img.shields.io/github/last-commit/schech1/uptime-buddy"/></a>
</p>


<p align="center">
<a href="https://apps.apple.com/de/app/uptime-mate/id6503297780"><img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="App Store Link"></a>
</p>


------------
<table>
  <tr>
    <td align="center">
      <strong>BREAKING NEWS</strong><br><br>
      <strong>Uptime Mate is back.</strong><br><br>
      The Apple Watch app has been completely rebuilt and is now compatible with <strong>Uptime Kuma v2</strong>.<br>
      It now connects directly to Uptime Kuma via <strong>WebSockets</strong>, so the extra Docker backend is no longer required.<br><br>
      This repository will be cleaned up and primarily used to share a <strong>TestFlight link (coming soon)</strong> for future beta releases.
      Since the App got a complete rework, I expect bugs to appear at the beginning.
      You can still use this repo to create issues for bugs found in the AppleWatch or iPhone App.
    </td>
  </tr>
</table>


------------
Uptime Mate is an uptime monitoring tool for your Apple Watch, designed to keep you informed about the status of your services. 
Uptime Mate, requires a lightweight docker backend to run.


|<img src="images/uptime-buddy-2.png" alt="Apple Watch with Uptime Mate" style="width:90%;">|<img src="images/uptime-buddy-3.png" alt="Apple Watch with Uptime Mate" style="width:90%;">|<img src="images/uptime-buddy-4.png" alt="Apple Watch with Uptime Mate" style="width:90%;">|
|:---:|:---:|:---:|
|<img src="images/uptime-buddy-1.png" alt="Apple Watch with Uptime Mate" style="width:90%;">|<img src="images/uptime-buddy-5.png" alt="Apple Watch with Uptime Mate" style="width:90%;">|<img src="images/uptime-buddy-6.png" alt="Apple Watch with Uptime Mate" style="width:90%;">|





## Settings on the iOS App

- Set your UptimeKuma Instance in the iOS App and your login credentials.
- Check the Backened
- Configure the watch
- Done


<img src="images/uptime-buddy-ios.PNG" alt="Apple Watch with Uptime Buddy" style="width:30%;">



## The Apple Watch and iOS App

Uptime Mate consists of an iOS app and an Apple Watch app.
The iOS app is needed to set up the backend address and login credentials
When the iOS app is installed, the Apple Watch app can be installed via the Watch app of the iPhone.

Uptime Mate comes with Complications and SmartStack support.
The current update frequency of the Widgets is 15 minutes (due to WidgetKit limitations).


## Symbols on the Apple Watch

The following SF Symbols are used to illustrate the monitor type:

<img src="images/sfSymbols.png" alt="Apple Watch with Uptime Mate" style="width:30%;">

## Complications

Uptime Mate supports different complications on the WatchFace.

<table>
  <tr>
    <td style="text-align: center;">
      <img src="images/complication-cicular.png" alt="Circular" style="width: 100%;">
      <p>Circular</p>
    </td>
    <td style="text-align: center;">
      <img src="images/complication-corner.png" alt="Corner" style="width: 100%;">
      <p>Corner</p>
    </td>
    <td style="text-align: center;">
      <img src="images/complication-rectangular-1.png" alt="Rectangular Big" style="width: 100%;">
      <p>Rectangular Big</p>
    </td>
  </tr>
</table>


<table>
  <tr>
<td style="text-align: center;">
      <img src="images/complication-rectangular-2.png" alt="Rectangular Small" style="width: 100%;">
      <p>Rectangular Small</p>
    <td style="text-align: center;">
      <img src="images/complication-rectangular-dashed.png" alt="Rectangular Big" style="width: 100%;">
      <p>Rectangular Dashed</p>
    </td>
    <td style="text-align: center;">
      <img src="images/complication-circular-dashed.png" alt="Rectangular Small" style="width: 100%;">
      <p>Circular Dashed</p>
    </td>
  </tr>
</table>



## Data Privacy

Uptime Mate does not save, share or forward any data.

- Everything runs locally, no hidden backend, etc.
- All data is just displayed and cached on your Apple Watch. All data is gone, when the App is deleted.
- Only read requests are done to Websockets! (`getMonitors`, `getHearbeats`). 
- No write/modifications are done on UptimeKuma. 


The Apple Watch App requests the follwing data from Uptime Kuma:
- List of Monitors with ```status, name, type, lastUpdate and id```
- List of the last 60 Heartbeats (```ID, status, pingResponse, heartbeatTimestamp```)


## Related Projects

This project is based on Uptime Kuma and uptime-kuma-api.

[Uptime Kuma](https://github.com/louislam/uptime-kuma): A self-hosted monitoring tool to monitor uptime for websites, applications and services.


## Contributing

Contributions are welcome.

## Support Me

If you enjoy using this app, please consider leaving a 
[Rating on the App Store!](https://apps.apple.com/app/id6503297780?action=write-review)

If you encounter any issues or have questions, please open an issue on this GitHub repository.
