import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import threading
import re
import numpy as np
import cv2
from PIL import ImageGrab
import pytesseract
import winsound
from datetime import datetime
import time

# Configure tesseract executable path (if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.02

last_right_num = None

class Timer:
    def __init__(self, delay, label, beep_var):
        self.delay = delay
        self.initial_delay = delay  # Store the initial delay
        self.label = label
        self.beep_var = beep_var
        self.thread = None
        self.running = False
        self.lock = threading.Lock()
        self.reset_event = threading.Event()

    def start(self):
        with self.lock:
            if self.running:
                return
            self.running = True
            self.reset_event.clear()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        with self.lock:
            if not self.running:
                return
            self.running = False
        if self.thread is not None:
            self.thread.join()

    def reset(self):
        with self.lock:
            self.reset_event.set()

    def run(self):
        while self.running:
            for remaining in range(self.delay // 1000, 0, -1):
                if not self.running:
                    return
                if self.reset_event.is_set():
                    self.reset_event.clear()
                    break
                self.label.config(text=f"Next injection in: {remaining} seconds")
                time.sleep(1)
            else:
                if self.running:
                    self.label.config(text="Injecting...")
                    if self.beep_var.get():
                        winsound.Beep(1000, 500)  # Beep sound for 500ms at 1000Hz
                    print("alt_pressed ran from run(self)")
                    if auto_inject_var.get():
                        on_alt_pressed()  # Call the alt press function
            self.delay = self.initial_delay  # Reset the delay to the initial value

class Script:
    def __init__(self, timer, status_label, delay_entry):
        self.running = False
        self.timer = timer
        self.status_label = status_label
        self.delay_entry = delay_entry

    def start(self):
        if self.running:
            return  # Prevents starting the script multiple times
        self.delay = int(self.delay_entry.get())
        self.timer.delay = self.delay
        self.timer.initial_delay = self.delay  # Update the initial delay
        self.running = True
        self.status_label.config(text="Running", fg='green')
        setup_hotkeys()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.timer.stop()
        self.status_label.config(text="Stopped", fg='red')
        timer_label.config(text="Next injection in: N/A")
        remove_hotkeys()

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

# Shared flag to prevent multiple calls
alt_pressed_lock = threading.Lock()
is_processing_alt_press = False  # Flag to prevent re-entrance
last_alt_press_time = None  # Timestamp to track last alt press time

def on_alt_pressed():
    global is_processing_alt_press, last_alt_press_time
    current_time = datetime.now()
    with alt_pressed_lock:
        if not script.running or is_processing_alt_press:
            return
        if last_alt_press_time and (current_time - last_alt_press_time).total_seconds() < 1:
            return  # Prevent processing if called within 1 second
        is_processing_alt_press = True
        last_alt_press_time = current_time

    try:
        print("Running alt_pressed function")  # Debug print

        hatch_count_region = get_hatch_count_region()
        screen_capture = capture_screen(region=hatch_count_region)
        extracted_text = getText(screen_capture)
        hatch_count = parse_single_number(extracted_text)
        inject_queens(hatch_count)

        if auto_inject_var.get() and script.running:
            print("Resetting timer")  # Debug print
            script.timer.reset()  # Reset and start the timer after manual alt press
            script.timer.start()  # Ensure the timer starts if not already running
        else:
            script.timer.start()  # Start the timer if not auto injecting
    finally:
        is_processing_alt_press = False

def create_overlords():
    global last_right_num
    while True:
        if script.running and overlord_var.get():
            print("Checking for supply block...")  # Debug print
            top_right_region = get_top_right_region()
            screen_capture = capture_screen(region=top_right_region)
            extracted_text = perform_ocr(screen_capture)
            print(f"OCR Text: {extracted_text}")  # Debug print
            left_num, right_num = parse_numbers(extracted_text)
            print(f"Parsed Numbers - Left: {left_num}, Right: {right_num}")  # Debug print

            # Determine the trigger threshold based on the right number
            trigger_threshold = float('inf')  # Default to infinity
            if left_num is not None and right_num is not None:
                if right_num >= 100 and right_num < 200:
                    trigger_threshold = 12
                elif 50 <= right_num < 100:
                    trigger_threshold = 8
                elif right_num > 80:  # For numbers over 80
                    trigger_threshold = 4  # Or any other threshold you want

            # Check if the conditions are met and if the right number is different from the last seen right number
            if (left_num is not None and right_num is not None and
                right_num >= 30 and right_num < 200 and  # Conditions for the right number
                (right_num - left_num) <= trigger_threshold and
                right_num != last_right_num):  # Check only the right number

                print(f"Creating Overlord at: {left_num} / {right_num}")  # Debug print
                
                # Perform key presses based on the right number
                pyautogui.press('5')  # Press the '5' key
                print("Pressed '5' key")  # Debug print
                time.sleep(0.1)  # Wait for 100 milliseconds
                pyautogui.press('s')  # Press the 's' key
                print("Pressed 's' key")  # Debug print
                time.sleep(0.1)  # Wait for 100 milliseconds
                pyautogui.press('v')  # Press the 'v' key
                print("Pressed 'v' key")  # Debug print
                
                # If the right number is over 80, press 'v' again
                if right_num > 80:
                    time.sleep(0.1)  # Wait for 100 milliseconds
                    pyautogui.press('v')  # Press the 'v' key again
                    print("Pressed 'v' key again")  # Debug print

                # Update the last seen right number
                last_right_num = right_num

        # Delay between captures
        time.sleep(1)

def get_top_right_region():
    top_right_region = (2402, 23, 2536, 57)
    return top_right_region

def get_hatch_count_region():
    hatch_count_region = (1086, 1102, 1156, 1136)
    return hatch_count_region

def capture_screen(region=None):
    screen = ImageGrab.grab(bbox=region)
    return screen

def perform_ocr(image):
    # Perform OCR on the captured image
    text = pytesseract.image_to_string(image)
    return text

def getText(screenshot):
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([15, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    res = cv2.bitwise_and(screenshot_np, screenshot_np, mask=mask)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    contrast = cv2.convertScaleAbs(gray, alpha=2, beta=0)
    _, thresh = cv2.threshold(contrast, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    txt = pytesseract.image_to_string(thresh, config="--psm 6 digits")
    return txt

def parse_numbers(text):
    numbers = re.findall(r'\b\d+\b', text)
    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])
    return None, None

def parse_single_number(text):
    print("Extracted text:", text)
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    return 0

def is_window_active(window_title):
    try:
        return window_title in pyautogui.getActiveWindowTitle()
    except:
        return False

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        script.stop()
        gui.destroy()

# Function to inject queens based on hatch count
def inject_queens(hatch_count):
    if is_window_active(game_title):
        start_x, start_y = pyautogui.position()
        pyautogui.moveTo(1280, 540)
        pyautogui.press('2')
        time.sleep(0.1)
        for _ in range(hatch_count):
            pyautogui.write('v', interval=0.025)
            pyautogui.press('backspace')
            pyautogui.click()
        pyautogui.moveTo(start_x, start_y)

# Initial settings
game_title = "StarCraft II"
injection_delay = 32000  # 32 seconds

# Create the GUI
gui = tk.Tk()
gui.title("StarCraft II Script")

auto_inject_var = tk.BooleanVar()
beep_var = tk.BooleanVar()
overlord_var = tk.BooleanVar()

tk.Checkbutton(gui, text="Auto inject after delay?", variable=auto_inject_var).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
tk.Checkbutton(gui, text="Play beep after delay?", variable=beep_var).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')
tk.Checkbutton(gui, text="Create overlords when close to supply block?", variable=overlord_var).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')

tk.Label(gui, text="Injection Delay (ms):").grid(row=3, column=0, padx=10, pady=5, sticky='w')
delay_entry = tk.Entry(gui, state='normal')
delay_entry.insert(0, str(injection_delay))
delay_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(gui, text="Start", command=lambda: script.start()).grid(row=4, column=0, padx=10, pady=10)
tk.Button(gui, text="Stop", command=lambda: script.stop()).grid(row=4, column=1, padx=10, pady=10)

status_label = tk.Label(gui, text="Stopped", fg='red')
status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

timer_label = tk.Label(gui, text="Next injection in: N/A", fg='blue')
timer_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

gui.protocol("WM_DELETE_WINDOW", on_closing)
gui.geometry("400x300")

# Initialize timer and script objects
timer = Timer(injection_delay, timer_label, beep_var)
script = Script(timer, status_label, delay_entry)

# Start the overlord creation thread
overlord_thread = threading.Thread(target=create_overlords)
overlord_thread.daemon = True
overlord_thread.start()

# Manual check for Alt key press
def check_alt_pressed():
    if keyboard.is_pressed('alt'):
        on_alt_pressed()
    gui.after(100, check_alt_pressed)

def setup_hotkeys():
    keyboard.add_hotkey('F11', script.toggle)
    keyboard.add_hotkey('F8', script.start)
    keyboard.add_hotkey('F9', script.stop)

def remove_hotkeys():
    keyboard.remove_hotkey('F11')
    keyboard.remove_hotkey('F8')
    keyboard.remove_hotkey('F9')

# Ensure GUI is always shown
def ensure_gui_visible():
    if not gui.winfo_exists():
        gui.deiconify()
    gui.after(1000, ensure_gui_visible)

ensure_gui_visible()
setup_hotkeys()
gui.after(50, check_alt_pressed)  # Start manual check for Alt key press
gui.mainloop()
remove_hotkeys()
