import os
import sys
import time

import pyautogui


def screenshot(name, duration):
    time.sleep(3)
    target_folder = f"images"

    screenshot_path = os.path.join(target_folder, f"{name}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    print(f"Screenshot saved to {screenshot_path}")
    time.sleep(duration - 3)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        duration = int(sys.argv[2])
        screenshot(name, duration)
    else:
        print("Please provide a folder name as an argument.")
