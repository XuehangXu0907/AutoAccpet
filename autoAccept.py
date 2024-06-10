import cv2
import numpy as np
import pyautogui
import time
import logging
from filelock import FileLock

# Configure logging
logging.basicConfig(filename='auto_accept.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the template image of the accept button
try:
    accept_button_template = cv2.imread('accept_button.png', 0)
    if accept_button_template is None:
        raise FileNotFoundError("Template image not found. Ensure 'accept_button.png' is in the correct directory.")
except Exception as e:
    logging.error(f"Error loading template image: {e}")
    exit()

w, h = accept_button_template.shape[::-1]

def detect_accept_button():
    try:
        # Take a screenshot of the screen
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # Perform template matching
        res = cv2.matchTemplate(screenshot, accept_button_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            # If the accept button is found, return its position
            return pt[0], pt[1], w, h
        return None
    except Exception as e:
        logging.error(f"Error in detecting accept button: {e}")
        return None

def click_accept_button(x, y, w, h):
    try:
        # Wait for 4 seconds before clicking
        time.sleep(4)

        # Calculate the center of the accept button
        click_x = x + w // 2
        click_y = y + h // 2

        # Store the current mouse position
        current_mouse_x, current_mouse_y = pyautogui.position()

        # Move the mouse to the accept button and click
        pyautogui.moveTo(click_x, click_y)
        pyautogui.click()

        # Return the mouse to its original position
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
    except Exception as e:
        logging.error(f"Error in clicking accept button: {e}")

def auto_accept_queue():
    logging.info("Auto accept script started.")
    last_click_time = 0

    while True:
        current_time = time.time()
        result = detect_accept_button()

        if result and (current_time - last_click_time >= 10):
            x, y, w, h = result
            click_accept_button(x, y, w, h)
            logging.info("Accepted the queue!")
            last_click_time = current_time

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    lock_file = "auto_accept.lock"
    lock = FileLock(lock_file)

    try:
        with lock.acquire(timeout=0):  # Immediately fail if the lock is held
            auto_accept_queue()
    except Exception:
        logging.error("Another instance is already running.")
        print("Another instance is already running.")
