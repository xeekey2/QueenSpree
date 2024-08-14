import pyautogui
import keyboard
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Configure tesseract executable path (if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def getText(screenshot):
    # Convert PIL image to numpy array
    screenshot_np = np.array(screenshot)
    # Convert RGB to BGR (as OpenCV expects images in BGR format)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    # Convert to HSV color space
    hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2HSV)

    # Define range of orange color in HSV
    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([15, 255, 255])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(screenshot_np, screenshot_np, mask=mask)

    # Convert the result to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Enhance contrast
    contrast = cv2.convertScaleAbs(gray, alpha=2, beta=0)

    # Apply binary threshold
    _, thresh = cv2.threshold(contrast, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Perform OCR using Tesseract
    txt = pytesseract.image_to_string(thresh, config="--psm 6 digits")
    return txt, thresh

def print_mouse_position_and_screenshot():
    # Get the current mouse position
    x, y = pyautogui.position()
    print(f"Mouse position: (X: {x}, Y: {y})")

    # Define the border dimensions
    border_width = 134
    border_height = 35

    # Calculate the coordinates of the rectangle
    left = x - border_width // 2
    top = y - border_height // 2
    right = x + border_width // 2
    bottom = y + border_height // 2

    # Print the coordinates in the desired format
    print(f"top_right_region = ({left}, {top}, {right}, {bottom})")

    # Capture a screenshot of the specified region
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    # Perform OCR on the preprocessed region
    extracted_text, preprocessed_image = getText(screenshot)
    print("Extracted text:", extracted_text)

    # Show the screenshot and the preprocessed image
    screenshot_np = np.array(screenshot)
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(screenshot_np)
    plt.title('Original Screenshot')
    
    plt.subplot(1, 2, 2)
    plt.imshow(preprocessed_image, cmap='gray')
    plt.title('Preprocessed Image')
    
    plt.show()

# Setting up hotkey binding
keyboard.add_hotkey('F6', print_mouse_position_and_screenshot)

print("Press 'F6' to get the current mouse position, region coordinates, and perform OCR.")
print("Press 'Esc' to exit.")

# Keep the script running to listen for hotkeys
keyboard.wait('esc')
