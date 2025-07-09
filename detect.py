import cv2 as cv
import numpy as np
import pyautogui


def detect_death_screen(image_path: str) -> bool:
    """
    Detect if a death screen appears on the user's screen.
    :param image_path: Path to the death screen file to be detected.
    :return: True if the death screen is found on the screen, False otherwise.
    """
    death_screen = cv.imread(image_path, cv.IMREAD_COLOR)
    if death_screen is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")

    screenshot = pyautogui.screenshot()

    frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2GRAY)

    if frame.shape[0] > 1080:  # >1080p
        scale = 0.5
        frame = cv.resize(frame, None, fx=scale, fy=scale)
        death_screen = cv.resize(death_screen, None, fx=scale, fy=scale)

    result = cv.matchTemplate(frame, death_screen, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    return len(loc[0]) > 0
