import cv2 as cv
import numpy as np
import pyautogui


def detect_death_screen(image_path: str) -> bool:
    """
    Detect if a death screen appears on the user's screen.
    :param image_path: Path to the death screen file to be detected.
    :return: True if the death screen is found on the screen, False otherwise.
    """
    death_screen = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    if death_screen is None:
        print(f"Image at {image_path} could not be loaded.")
        raise FileNotFoundError

    screenshot = pyautogui.screenshot()
    frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2GRAY)

    result = cv.matchTemplate(frame, death_screen, cv.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(result >= threshold)

    return len(loc[0]) > 0
