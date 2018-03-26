import serial

class Cereal:

    def __init__(self, port):

        self.port = port

        self.ser = serial.Serial(self.port, 115200)

        self.close_serial()
        self.open_serial()

    def open_serial(self):
        self.ser.open()

    def close_serial(self):
        self.ser.close()

    def forward(self):
        self.ser.write('w'.encode('utf-8'))

    def left(self):
        self.ser.write('q'.encode('utf-8'))

    def right(self):
        self.ser.write('e'.encode('utf-8'))

    def reverse(self):
        self.ser.write('s'.encode('utf-8'))

    def stop(self):
        self.ser.write('x'.encode('utf-8'))

    def back_left(self):
        self.ser.write('a'.encode('utf-8'))

    def back_right(self):
        self.ser.write('d'.encode('utf-8'))

    def servo_left(self):
        self.ser.write(','.encode('utf-8'))

    def servo_right(self):
        self.ser.write('.'.encode('utf-8'))

    def servo_return_position(self):
        self.ser.write('/'.encode('utf-8'))

    def step_motor_right(self):
        self.ser.write('6'.encode('utf-8'))

    def step_motor_left(self):
        self.ser.write('5'.encode('utf-8'))
