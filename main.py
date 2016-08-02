import sys
import os
import signal
import logging

from flask import *
from VehicleProxy import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Quite down the Flask logger
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

log = logging.getLogger(__name__)

# Configuration
SERVER_PORT = 8080
#VEHICLE_CONNECTION_STRING = 'udpin:127.0.0.1:14550'
VEHICLE_CONNECTION_STRING = 'tcp:127.0.0.1:5760'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WWW_DIR = os.path.join(BASE_DIR, "www")

app = Flask(__name__)
proxy = None


# Prevent caching
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#################################
# API


@app.route('/api/status')
def _get_status():
    ret = proxy.get_status()
    return jsonify(ret)


@app.route('/api/arm', methods=['POST'])
def _arm():
    proxy.arm()
    return jsonify(Received=True)


@app.route('/api/takeoff', methods=['POST'])
def _takeoff():
    proxy.takeoff()
    return jsonify(Received=True)


@app.route('/api/rtl', methods=['POST'])
def _rtl():
    proxy.rtl()
    return jsonify(Received=True)


@app.route('/api/goto', methods=['POST'])
def _goto():

    lat = float(request.values.get("Latitude"))
    lon = float(request.values.get("Longitude"))
    alt = float(request.values.get("Altitude"))
    proxy.goto(lat, lon, alt)
    return jsonify(Received=True)

#################################
# Static files


@app.route('/<path:path>')
def _www(path):
    return send_from_directory(WWW_DIR, path)


@app.route('/')
def _index():
    return send_from_directory(WWW_DIR, 'index.html')


def sigint_handler(signum, frame):
    print "Processing SIGINT"
    proxy.stop()
    sys.exit()


#################################
if __name__ == "__main__":

    # Install shutdown signal handler
    signal.signal(signal.SIGINT, sigint_handler)

    proxy = VehicleProxy("UAS_1", VEHICLE_CONNECTION_STRING)
    app.run(host='0.0.0.0', port=SERVER_PORT, threaded=True)
