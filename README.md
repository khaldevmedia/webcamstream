# Webcam streamer

## Description

A lightweight web app that allows you to stream live video from your webcam to the local network using OpenCV.

## Specs

- Streams video from the webcam to the local network.
- Uses SQLite to save logs of connection timestamps and IPs.

## Use

#### Run the app

> python3 app.py

#### Then use one of these URLs in your browser (assuming that the local IP of the machine that runs the app is `192.168.0.44`):

##### Homepage (live stream):

> 192.168.0.44:5000

##### Log of connections' history:

> 192.168.0.44:5000/log

##### IPs of users and the number of connections per user:

> 192.168.0.44:5000/ips

## Notes

- The app was tested on **Ubuntu 22.04.4 LTS server**.
- `log.db` should be created in the same directory as `app.py` after the very first run.
- The app uses Flask's development server which is not suitable for production. However, it works fine for personal use by one user.
- The app can handle one stream at a time. Handling simultaneous streams requires the use of a full-fledged server like Apache. Also, the video source of your device (the camera) might not be able to handle multiple read requests at the same time.
- Currently, the app doesn't support streaming audio. A future update may include this functionality, probably by using python libraries like `pyaudio` or `sounddevice`.

## External access:

You can combine this app with a setup that allows you to access your local network from outside. **Wireguard** private VPN is a good solution. It provides secure connection to your local network through an encrypted tunnel. This combination was tested with this app, and it allowed successful access to the video stream from outside the local network.
