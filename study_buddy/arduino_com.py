# import time
# import serial


# def read_data(baudrate=9600):
#     arduino_data = serial.Serial("com9", baudrate=baudrate)

#     time.sleep(1)

#     while True:
#         while arduino_data.inWaiting() == 0:
#             pass
#         data_packet = arduino_data.readline()
#         datastr = str(data_packet, "utf-8").strip("\r\n")
#         print(datastr)


# def write_data(baudrate=9600):
#     arduino = serial.Serial(port='COM9', baudrate=baudrate, timeout=.1)
#     def write_read(x):
#         arduino.write(bytes(x, "utf-8"))
#         time.sleep(0.05)
#         data = arduino.readline()
#         return data
#     while True:
#         stuff = input("Enter stuff: ") # Taking input from user
#         print(f"Stuff from Python: {stuff}")
#         value = write_read(stuff)
#         print(f"Stuff back from Arduino: {value}") # printing the value


# if __name__ == "__main__":
#     # read_data(baudrate=115200)
#     write_data(baudrate=115200)

import serial
import time

arduino = serial.Serial(port='COM9', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


while True:
    num = input("Enter a number: ")
    value = write_read(num)
    print(str(value, "utf-8"))
