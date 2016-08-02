import threading
import logging
import time

from dronekit import connect, VehicleMode,LocationGlobalRelative

log = logging.getLogger(__name__)


class VehicleProxy(object):
    """ A simple proxy wrapping communication with a DroneKit Vehicle object. """

    def __init__(self, name, connection_string):
        self._name = name
        self._connection_string = connection_string
        self._vehicle = None

        self._stop_thread = threading.Event()

        self._thread = threading.Thread(None, self._thread_loop, self._name + "_Thread", ())
        self._thread.Daemon = True
        self._thread.start()

    def stop(self):
        self._stop_thread.set()

    def _thread_loop(self):

        while not self._stop_thread.isSet():
            if not self._vehicle:
                log.debug(self._vehicle)
                try:
                    log.debug("Connecting to vehicle at {}".format(self._connection_string))
                    vehicle = connect(self._connection_string, wait_ready=True, rate=10, baud=57600)

                    # Testing
                    vehicle.parameters['ARMING_CHECK'] = 0
                    vehicle.flush()

                    self._vehicle = vehicle
                    log.debug("Connected!")
                except:
                    log.exception("Timed out connecting to vehicle")

            time.sleep(1)

        if self._vehicle is not None:
            self._vehicle.close()
            self._vehicle = None

    def get_status(self):
        v = self._vehicle

        if not v:
            return {"Connected": False}

        status = {"Connected": True,
                  "Armed": v.armed,
                  "Armable": v.is_armable,
                  "Mode": v.mode.name,
                  "Status": v.system_status.state,
                  "Latitude": v.location.global_relative_frame.lat,
                  "Longitude": v.location.global_relative_frame.lon,
                  "Altitude": v.location.global_relative_frame.alt,
                  "Heading": v.heading
                  }

        if v.battery:
            status["Battery"] = {
                "Voltage": v.battery.voltage,
                "Current": v.battery.current,
                "Level": v.battery.level
            }

        if v.attitude:
            status["Attitude"] = {
                "Yaw": v.attitude.yaw,
                "Pitch": v.attitude.pitch,
                "Roll": v.attitude.roll
            }

        return status

    def arm(self):
        if not self._vehicle:
            return

        try:

            # Copter should arm in GUIDED mode
            self._vehicle.mode = VehicleMode("GUIDED")

            self._vehicle.armed = True
            self._vehicle.flush()
        except:
            log.exception("Unable to Arm")

    def takeoff(self):
        if not self._vehicle:
            return

        try:
            # Takeoff to a height of 10 meters
            self._vehicle.simple_takeoff(10)
            self._vehicle.flush()
        except:
            log.exception("Unable to takeoff")

    def rtl(self):
        if not self._vehicle:
            return

        try:
            self._vehicle.mode = VehicleMode("RTL")
            self._vehicle.flush()
        except:
            log.exception("Unable to set mode to RTL")

    def goto(self, lat, lon, altitude):
        if not self._vehicle:
            return

        try:
            self._vehicle.airspeed = 5

            point = LocationGlobalRelative(lat, lon, altitude)
            self._vehicle.simple_goto(point)

            self._vehicle.flush()
        except:
            log.exception("Unable to GOTO point")
