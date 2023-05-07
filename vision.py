import cv2
import imutils
import numpy as np
import pyautogui
import pytesseract

import game
import utils
import cons

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def capture_text(coords):
    x, y, width, height = (cons.COORDS[coords][0],
                           cons.COORDS[coords][1],
                           cons.COORDS[coords][2],
                           cons.COORDS[coords][3],)
    im = pyautogui.screenshot(region=(x, y, width, height))
    im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2GRAY)
    im = imutils.resize(im, width=200)
    blur = cv2.GaussianBlur(im, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    result = 255 - thresh
    data = pytesseract.image_to_string(result, lang='eng', config='--psm 6')
    lines = data.split('\n')
    return lines


def read_resources(resource):
    str_arr = capture_text(resource)
    lines = utils.sanitize_numbers(str_arr)
    try:
        lines = int(lines[0])
    except:
        print('Resource is not a int')
        lines = utils.get_resource_checks(resource)
        return lines
    return lines


def check_if_image_on_screen(image_path):
    image_found = False
    image = pyautogui.locateOnScreen(image_path)
    # Check the boolean variable before checking for the image:
    if pyautogui.locateOnScreen(image_path, region=image, confidence=.9) is not None:
        image_found = True
    return image_found
