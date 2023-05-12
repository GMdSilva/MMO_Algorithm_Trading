from tesserocr import PyTessBaseAPI
import cv2
import cons
import numpy as np
from PIL import Image
import asyncio
from win_interface import Windows_Interface
import utils

class Vision(Windows_Interface):
    def __init__(self):
        super().__init__()
        self.image = self.background_screenshot()

    def capture_text(self, coords, update=False):
        x, y, w, h = (coords[0],
                      coords[1],
                      coords[2],
                      coords[3],)
        if update:
            self.image = self.background_screenshot()
        image = self.image[y:y + h, x:x + w]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # OCR
        img = Image.fromarray(thresh)
        with PyTessBaseAPI() as api:
            api.SetImage(img)
            data = api.GetUTF8Text()
        #data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
        lines = data.split('\n')
        return lines[0]

    def get_each_price(self, offer_type, image):
        self.image = image

        def getConstant(offer_type):
            MARKET_COORDS = {
                'ask': [1303, 500, 59, 13],
                'bid': [1303, 681, 59, 13]
            }
            return MARKET_COORDS[offer_type]

        coords = getConstant(offer_type)

        def background(f):
            def wrapped(*args, **kwargs):
                return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

            return wrapped

        @background
        def get_uni_prices(i, coords):
            coords_temp = coords
            if i > 0:
                coords_temp[1] += 16
            data = self.capture_text(coords_temp)
            price = data
            return price

        loop = asyncio.get_event_loop()  # Have a new event loop

        looper = asyncio.gather(*[get_uni_prices(i, coords) for i in range(0, 7)])  # Run the loop

        results = loop.run_until_complete(looper)
        return results

    def read_resources(self, resource):
        coords = cons.COORDS[resource]
        str_arr = self.capture_text(coords)
        lines = ''.join(filter(str.isdigit, str_arr))
        try:
            lines = int(lines)
        except:
            print(lines)
            print('Resource is not a int')
            utils.get_resource_checks(resource)
        return lines

    # @staticmethod
    # def check_if_image_on_screen(template, threshold=.9):
    #     img_rgb = Windows_Interface.background_screenshot()
    #     template = cv2.imread(template)
    #     # img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    #     # h, w = template.shape[:-1]
    #     res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_TOZERO)
    #     # print(res)
    #     # cv2.imshow('image', template)
    #     # cv2.waitKey(0)
    #     flag = False
    #     if np.amax(res) > threshold:
    #         flag = True
    #         return flag
    #     return flag
    @staticmethod
    def check_if_image_on_screen(template, threshold=.9):
        flag = False
        img_rgb = Windows_Interface.background_screenshot()
        assert img_rgb is not None, "file could not be read, check with os.path.exists()"
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        assert template is not None, "file could not be read, check with os.path.exists()"
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        results = []
        for pt in zip(*loc[::-1]):
            results.append(pt)
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        if len(results) > 0:
            flag = True
            return flag
            print('achou')
        return flag

#check_if_image_on_screen('the_devil.JPG')
