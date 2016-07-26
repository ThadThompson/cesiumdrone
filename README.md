# Cesium Drone

A proof of concept web based GCS built on [DroneKit Python](https://github.com/dronekit/dronekit-python) and [Cesium](https://cesiumjs.org)

Inspired by [Tower Web](https://github.com/dronekit/tower-web)

![Screenshot](screenshots/1.PNG)

## Running

```
git clone https://github.com/ThadThompson/cesiumdrone.git
cd cesiumdrone
pip install -r requirements.txt
python main.py
```

Then open <http://localhost:8008/> in a browser.

The connection string for the drone is at the top of main.py. It is currently setup to run with the defaults for the
simulator as described in the [DroneKit documentation](http://python.dronekit.io/develop/sitl_setup.html).

Notes: 

This was thrown together over a couple of hours on the weekend - it is not production quality code.

I'm using the CesiumAir airplane model, but this will currently only work with a copter (due to takeoff modes). Also, the plane doesn't correctly orient to the direction the quad would fly so it looks a little hokey. I'm currently just using it as a placeholder until I come up with a copter model.

## License

MIT/Apache-2.0
