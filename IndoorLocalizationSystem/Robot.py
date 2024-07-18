import json
import sys
import socket
import time
from concurrent.futures import thread

from utility import read_aruco_code
import re


class Robot:
    def __init__(self):
        # info
        self.status = "STOP"
        self.last_position = -1
        self.target_position = -1
        self.sequence_aruco = []
        self.aruco_code_generated = [1, 2, 3, 4]

        # command
        self.cmd_no = 0

        # path cost - backward path
        # self.path_cost = []
        # self.reverse_sequence_aruco = []
        # self.reverse_path_cost = []
        # self.reference_sequence_scan = []

        # line perception
        # self.line = 0

        # connect to car Wi-Fi
        self.ip = "192.168.4.1"
        self.port = 100
        self.car = socket.socket()
        try:
             self.car.connect((self.ip, self.port))
        except:
            print("Error", sys.exc_info()[0])
            sys.exit()

    def scan_sequence(self):
        aruco = 0
        scan_completed = False
        self.send_cmd("switch_mode")
        self.status = "configuration"
        while not scan_completed:
            ids = read_aruco_code("http://192.168.4.1/capture")
            if ids is not None:
                if ids[0][0] in self.aruco_code_generated:
                    self.last_position = ids[0][0]
                    if self.last_position not in self.sequence_aruco:
                        self.sequence_aruco.append(self.last_position)
                        aruco += 1
                        if aruco == len(self.aruco_code_generated):
                            scan_completed = True

        self.send_cmd("stop_car")

        # backward path
        # self.reverse_sequence_aruco = [self.sequence_aruco[len(self.sequence_aruco) - 1 - index] for index in range(len(self.sequence_aruco))]

        # reference system
        # self.reference_sequence_scan = "principal"

        # compute path cost
        # self.build_path_cost()

    # def build_path_cost(self):
    #     for i in range(len(self.sequence_aruco)):
    #         index_forward = range(i + 1, len(self.sequence_aruco))
    #         index_backward = range(0, i)
    #         counter_forward = 0
    #         for j in index_forward:
    #             self.path_cost.append((self.sequence_aruco[i], self.sequence_aruco[j], j - i))
    #             counter_forward += 1
    #         for j in index_backward:
    #             counter_forward += 1
    #             self.path_cost.append((self.sequence_aruco[i], self.sequence_aruco[j], counter_forward))

    # def compute_reverse_path_cost(self, principal_cost):
    #     return len(self.sequence_aruco) - principal_cost

    def set_target(self, id_target):
        self.target_position = id_target
        if self.target_position != self.last_position:
            self.status = "running"
            ### AI
            # for (item_source, item_dest, path_cost) in self.path_cost:
                # if item_source == self.last_position and self.target_position == item_dest:
                    # reverse_cost = self.compute_reverse_path_cost(path_cost)
                    # if path_cost < reverse_cost:
                        # if self.reference_sequence_scan == "reverse":
                            # torno indietro
                            # self.reference_sequence_scan = "principal"
                            # self.invert_car_direction()
                            # time.sleep(0.5)
                    # else:
                        # if self.reference_sequence_scan == "principal":
                            # torno indietro
                            # self.reference_sequence_scan = "reverse"
                            # self.invert_car_direction()
                            # time.sleep(0.5)
            self.control()

    def control(self):
        self.send_cmd("switch_mode")
        while True:
            ids = read_aruco_code("http://192.168.4.1/capture")
            if ids is not None:
                if ids[0][0] in self.sequence_aruco:
                    self.last_position = ids[0][0]
                    if self.target_position == self.last_position:
                        self.send_cmd("stop_car")
                        self.last_position = self.target_position
                        self.status = "stop"
                        break

    # cmd given to car
    def send_cmd(self, do):
        self.cmd_no += 1
        msg = {"H": str(self.cmd_no)}

        # motor section
        if do == 'stop_car':
            msg.update({"N": 1, "D1": 0, "D2": 0, "D3": 1})
        elif do == "left":  # cmd not used
            msg.update({"N": 102, "D1": 3, "D2": 50})
        # switch mode
        elif do == "switch_mode":
            msg.update({"N": 101, "D1": 1})
        else:
            raise ValueError("Unrecognized command")

        # send command
        msg_json = json.dumps(msg)
        try:
            self.car.send(msg_json.encode())
        except:
            print("Error", sys.exc_info()[0])

    # def invert_car_direction(self):
    #     self.send_cmd("left")
    #     time.sleep(0.6)
    #     while True:
    #         self.read_line_sensor()
    #         if self.line >= 600:
    #             self.send_cmd("stop_car")
    #             break

    # def read_line_sensor(self):
    #     msg = {"H": 1, "N": 22, "D1": 1}
    #     # send command
    #     msg_json = json.dumps(msg)
    #     try:
    #         self.car.send(msg_json.encode())
    #         try:
    #             data = self.car.recv(1024).decode()
    #             if data != {"Heartbeat"} and data != {"Error"}:
    #                 data = data[1:]
    #                 data = data[:-1]
    #                 self.line = int(data)
    #
    #         except:
    #             print("Error")
    #     except:
    #         print("Error", sys.exc_info()[0])
