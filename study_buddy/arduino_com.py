import time
import serial


def read_data(baudrate=9600):
    arduino_data = serial.Serial("com9", baudrate=baudrate)

    time.sleep(1)

    while True:
        while arduino_data.inWaiting() == 0:
            pass
        data_packet = arduino_data.readline()
        datastr = str(data_packet, "utf-8").strip("\r\n")
        print(datastr)


def write_data(baudrate=9600):
    arduino = serial.Serial(port='COM9', baudrate=baudrate, timeout=.1)
    def write_read(x):
        arduino.write(x)
        time.sleep(0.05)
        data = arduino.readline()
        return data
    while True:
        stuff = bytes(str(int(input("Enter stuff: "))+50), "utf-8") # Taking input from user
        print(stuff)
        value = write_read(stuff)
        print(value) # printing the value


if __name__ == "__main__":
    # read_data(baudrate=115200)
    write_data(baudrate=115200)