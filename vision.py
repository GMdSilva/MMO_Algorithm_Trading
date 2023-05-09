import cv2
import imutils
import numpy as np
import pyautogui
import pytesseract
from win_interface import Windows_Interface
import game
import utils
import cons

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Vision(Windows_Interface):
    def __init__(self):
        super().__init__()

    def capture_text(self, coords):
        x, y, w, h = (cons.COORDS[coords][0],
                               cons.COORDS[coords][1],
                               cons.COORDS[coords][2],
                               cons.COORDS[coords][3],)
        #x, y, w, h = (coords[0], coords[1], coords[2], coords[3])
        im = self.background_screenshot()
        im = im[y:y + h, x:x + w]
        im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2GRAY)
        cv2.imwrite('result2.png', im)
        im = imutils.resize(im, width=200)
        cv2.imwrite('result3.png', im)
        blur = cv2.GaussianBlur(im, (7, 7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        result = 255 - thresh
        data = pytesseract.image_to_string(result, lang='eng', config='--psm 6')
        lines = data.split('\n')
        return lines

    def read_resources(self, resource):
        print(resource)
        str_arr = self.capture_text(resource)
        print(str_arr)
        lines = utils.sanitize_numbers(str_arr)
        try:
            lines = int(lines[0])
        except:
            print(lines)
            print('Resource is not a int')
            lines = utils.get_resource_checks(resource)
            return lines
        return lines


    def check_if_image_on_screen(self, template):
        img_rgb = self.background_screenshot()
        template = cv2.imread(template)
        #h, w = template.shape[:-1]
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = .9
        flag = False
        for i in res:
            if i.any() > threshold:
                flag = True
        return flag
        # loc = np.where(res >= threshold)
        # for pt in zip(*loc[::-1]):  # Switch columns and rows
        #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        #
        # cv2.imwrite('result.png', img_rgb)


# def check_if_image_on_screen(image_path):
#     image_found = False
#     image = pyautogui.locateOnScreen(image_path)
#     # Check the boolean variable before checking for the image:
#     if pyautogui.locateOnScreen(image_path, region=image, confidence=.9) is not None:
#         image_found = True
#     return image_found

# def capture_text(coords):
#     x, y, width, height = (cons.COORDS[coords][0],
#                            cons.COORDS[coords][1],
#                            cons.COORDS[coords][2],
#                            cons.COORDS[coords][3],)
#     im = pyautogui.screenshot(region=(x, y, width, height))
#     im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2GRAY)
#     im = imutils.resize(im, width=200)
#     blur = cv2.GaussianBlur(im, (7, 7), 0)
#     thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     result = 255 - thresh
#     data = pytesseract.image_to_string(result, lang='eng', config='--psm 6')
#     lines = data.split('\n')
#     return lines