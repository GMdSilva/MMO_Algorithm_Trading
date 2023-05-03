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
    game.bye_confirmation_box()
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
    game.bye_confirmation_box()
    lines = capture_text(resource)
    lines = ''.join(filter(str.isdigit, lines[0]))
    lines = int(lines)
    return lines
