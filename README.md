# Cerruto_Indoor_Localization_System

Indoor localization system project

Francesco Cerruto - 1000005927

## Alert

Please install v. 1.0.6 of esp32 by Espresif Systems to work with camera module installed on elegoo car to modify esp32 code

Please install v. 2.0.5 of esp32 byEspressif Systems to work with external camera module

## Car configuration

H-Bridge: TB series

Gyroscope: MPU6050

## Resource

Elegoo Smart car code

**https://www.elegoo.com/blogs/arduino-projects/elegoo-smart-robot-car-kit-v4-0-tutorial**

Turn esp32 camera into web camera

**https://www.rogerfrost.com/use-a-github-library-and-arduino-ide-to-create-an-esp32-camera-web-server/**

ArUco marker generation

**https://pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/**

ArUco marker detection from camera

**https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/**

## Project structure

### Aruco_Code folder

Python scripts to generate and detect (from video) ArUco marker

### Elegoo_Documentation folder

Documentation given by Elegoo

### Original_Arduino_Code folder

Robot code given by Elegoo

### Original_Esp32_Code folder

Camera code given by Elegoo

### Web_Camera_Code folder

Arduino code to stream esp32 view on a web serber

## Idea

1) Control car via website

**Set target point and retrieve car position (based on aruco code sequence scan)**

3) Position and view rendering

**Render camera data**
