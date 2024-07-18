import os

from flask import Flask, render_template, request, Response, redirect, flash
from Robot import Robot
import threading
from utility import localize_car, robot_camera_view


app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

robot = Robot()

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template("homepage.html")
    robot.scan_sequence()
    return redirect("/")


@app.route('/localize')
def localize():
        return render_template("localize.html", state = robot.status, last_position = robot.last_position, target_position = robot.target_position)


@app.route('/control', methods = ['GET', 'POST'])
def control():
    aruco_markers_description = str(robot.sequence_aruco)
    aruco_markers_description = aruco_markers_description.replace(" ", '')
    if request.method == 'GET':
        return render_template("control.html", aruco_markers = aruco_markers_description)

    print(request.form.get('target_position_set'))
    if int(request.form.get('target_position_set')) in robot.sequence_aruco:
        robot.set_target(int(request.form.get('target_position_set')))
    return render_template("control.html", aruco_markers = aruco_markers_description)


@app.route('/scene_view')
def scene_view():
    return Response(localize_car(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/robot_view')
def robot_view():
    return Response(robot_camera_view(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/update_robot_status')
def update_robot_status():
    return [robot.status, str(robot.last_position), str(robot.target_position)]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
