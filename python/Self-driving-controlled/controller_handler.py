from evdev import InputDevice, categorize, ecodes
import ser
import threading
import sys

class Gamepad:

    def __init__(self, event, type, port):

        self.connection = ser.Cereal(port)
        self.controller = InputDevice(event)
        self.type = type
        self.stopEvent = threading.event
        self.thread = threading.Thread(target=self.events, args=())
        self.thread.start()

        if self.type == "ps4":
            self.xBtn = 304
            self.cBtn = 305
            self.tBtn = 307
            self.sBtn = 208

            self.up_down = 17
            self.left_right = 16

            self.options = 315
            self.share = 314
            self.psBtn = 316

            self.r1 = 311
            self.r2b = 313
            self.r2 = 5
            self.r2_state = False
            self.r3 = 318

            self.l1 = 310
            self.l2b = 312
            self.l2 = 2
            self.l2_state = False
            self.l3 = 317

            self.lstickX = 0
            self.lstickX_default = 127
            self.lstickX_left_state = False
            self.lstickX_right_state = False
            self.lstickY = 1
            self.lstickY_default = 126

            self.rstickX = 3
            self.rstickX_default = 125
            self.rstickX_left_state = False
            self.rstickX_right_state = False
            self.rstickY = 4
            self.rstickY_default = 129
            self.rstickY_left_state = False
            self.rstickY_right_state = False

            self.joystick_wiggle = 10



    def read(self):

        if self.type == "ps4":

            for event in self.controller.read_loop():

                if event.type == ecodes.EV_KEY:

                    if event.value == 1:

                        if event.code == self.xBtn:
                            print("X")
                        elif event.code == self.cBtn:
                            print("C")
                        elif event.code == self.tBtn:
                            print("T")
                        elif event.code == self.sBtn:
                            print("S")

                        elif event.code == self.options:
                            print("Options")
                        elif event.code == self.share:
                            print("Share")
                        elif event.code == self.psBtn:
                            print("Playstation")
                            print("Stopping functions...")
                            self.stopEvent.set()
                            sys.exit()

                        elif event.code == self.r1:
                            print("R1")
                        elif event.code == self.r3:
                            print("R3")

                        elif event.code == self.l1:
                            print("L1")
                        elif event.code == self.l3:
                            print("L3")

                    elif event.value == 0:

                        if event.code == self.r2b:
                            print("R2 Released")
                            self.r2_state = False
                        elif event.code == self.l2b:
                            print("L2 Released")
                            self.l2_state = False

                if event.type == ecodes.EV_ABS:

                    if event.value != 0 and event.code == self.r2 or event.code == self.l2:

                        if event.code == self.r2:
                            print("R2 = " + str(event.value))
                            self.r2_state = True

                        elif event.code == self.l2:
                            print("L2 = " + str(event.value))
                            self.l2_state = True

                    elif event.code == self.lstickX:

                        if event.value > self.lstickX_default + self.joystick_wiggle:
                            print("Left stickX = " + str(event.value))
                            self.lstickX_right_state = True
                        elif  event.value < self.lstickX_default - self.joystick_wiggle:
                            print("Left stickX = " + str(event.value))
                            self.lstickX_left_state = True

                    elif event.code == self.lstickY:
                        if event.value > self.lstickY_default + self.joystick_wiggle:
                            print("Left stickY = " + str(event.value))
                        elif event.value < self.lstickY_default - self.joystick_wiggle:
                            print("Left stickY = " + str(event.value))

                    elif event.code == self.rstickX:

                        if event.value > self.rstickX_default + self.joystick_wiggle:
                            print("Right stickX = " + str(event.value))
                            #self.connection.step_motor_right()
                        elif event.value < self.rstickX_default - self.joystick_wiggle:
                            print("Right StickX = " + str(event.value))
                            #self.connection.step_motor_left()
                        elif self.rstickX_default - self.joystick_wiggle < event.value < self.rstickX_default + self.joystick_wiggle:
                            self.rstickX_up_state, self.rstickX_down_state = False

                    elif event.code == self.rstickY:

                        if event.value > self.rstickY_default + self.joystick_wiggle:
                            print("Right stickY = " + str(event.value))
                            self.rstickY_right_state = True
                        elif event.value < self.rstickY_default - self.joystick_wiggle:
                            print("Right stickY = " + str(event.value))
                            self.rstickY_left_state = True
                        elif self.rstickY_default - self.joystick_wiggle < event.value < self.rstickY_default + self.joystick_wiggle:
                            self.rstickY_left_state, self.rstickY_right_state = False


                    elif event.value == 1:

                        if event.code == self.up_down:
                            print("Down")
                        elif event.code == self.left_right:
                            print("Right")

                    elif event.value == -1:

                        if event.code == self.up_down:
                            print("up")
                        elif event.code == self.left_right:
                            print("Left")


    def events(self):
        while not self.stopEvent.is_set():
            if self.r2_state = True:
                self.connection.forward()
            if self.l2_state = True:
                self.connection.reverse()
            if self.lstickX_left_state = True:
                self.connection.left()
            if self.lstickX_right_state = True:
                self.connection.right()
            if self.rstickX_up_state = True:
                self.connection.servo_right()
            if self.rstickX_down_state = True:
                self.connection.servo_left()
