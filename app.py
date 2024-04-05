# CV2 Tutorial:
# https://www.youtube.com/watch?v=-4v4A550K3w
# --------------------------------------------

# Installed libraries
from flask import Flask, render_template, Response, request

# Python standard libraries
from datetime import datetime

# Local imports
from camera import VideoCamera
from log import Logger


app = Flask(__name__)
debug_mode = True


# Camera feed function to be used with the camera feed route
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame
               + b'\r\n\r\n')


# Handle 404 error
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")


########################################################################################
# --------------------------------------ROUTES------------------------------------------#
########################################################################################

# Index route
@app.route('/', methods=['GET'])
def index():
    # Get date and time now and put them in args variable to be sent to html template
    now = datetime.now()
    current_date = now.strftime('%A %d %B %Y')
    current_time = now.strftime('%H:%M:%S')
    args = {
        'date': current_date,
        'time': current_time
    }
    # Get The user's IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_addr = request.environ['REMOTE_ADDR']
    else:
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy

    # Make formated date-time from now to be inserted to the database
    formatted = str(now.strftime("%Y-%m-%d %H:%M:%S"))

    # Create Logger object
    logger = Logger("log.db")
    logger.create_table()

    # Create a new log
    log = (ip_addr, formatted)
    logger.create_log(log)

    return render_template('index.html', args=args)


# video_feed route. To be used in the src attribute of the img tag
@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Log route
@app.route('/log', methods=['GET'])
def logging():
    logger = Logger("log.db")
    logs = logger.get_all_logs()
    return render_template('log.html', logs=logs)


# Log route
@app.route('/ips', methods=['GET'])
def ips():
    logger = Logger("log.db")
    user_ips = logger.get_unique_ips()

    # Having this object will allow to detect if an unknown IP suaccessfully connected to the stream
    KNOWN_IPS = {
        # List your known IPs here as objects like this:
        '192.168.1.10': 'main-pc',
        '192.168.1.11': 'phone',
    }

    ips = []
    for user_ip in user_ips:
        if user_ip[0] in KNOWN_IPS:
            ips.append((user_ip[0], KNOWN_IPS[user_ip[0]], user_ip[1]))
        else:
            ips.append((user_ip[0], 'UNKNOWN DEVICE', user_ip[1]))
    return render_template('ips.html', ips=ips)


########################################################################################
# ------------------------------------RUN THE APP---------------------------------------#
########################################################################################

if __name__ == '__main__':
    app.run(debug=debug_mode, host='0.0.0.0', port='5000', threaded=True)
