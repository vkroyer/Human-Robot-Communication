
import serial
import time

arduino = serial.Serial(port='COM9', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def intent_detection():
    currently_rubberduck = False
    from intent import detect_intent_text
    while True:
        text = input("\nEnter some phrase: ")
        try:
            if text == "Go to sleep" and currently_rubberduck:
                mode = "0"
            else:
                mode = detect_intent_text(text)
            currently_rubberduck = True if mode=="2" else False
            value = write_read(mode)
            print(str(value, "utf-8"))
        except KeyError:
            print("Couldn't detect an intent")

def simple_commands():
    while True:
        mode = input("\nEnter the mode (0, 1, 2, 3, 4, or 5): ")
        if mode in "0 1 2 3 4 5".split():
            value = write_read(mode)
            print(str(value, "utf-8"))
        else:
            print("Choose a valid mode number")

def main():
    print("\nCHOOSE HOW TO SEND THE COMMANDS TO THE ARDUINO:\nFor simple commands (0,1,2,3,4,5), write 1\nFor intent detection with Google, write 2")
    while True:
        try:
            choice = int(input(">"))
            if choice in [1,2]:
                break
        except ValueError:
            print("Input number 1 or 2")
    if choice == 1:
        simple_commands()
    elif choice == 2:
        intent_detection()

if __name__  == "__main__":
    main()
