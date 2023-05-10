import win32api
import win32con
import config
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import numpy as np

class Windows_Interface:
    def __init__(self):
        self.hwnd = self.get_handle()

    def get_handle(self, char_name=config.char_name):
        toplist, winlist = [], []

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)

        game_window = [(hwnd, title) for hwnd, title in winlist if char_name in title.lower()]
        # just grab the hwnd for first window matching firefox
        game_handle = game_window[0]
        hwnd = game_handle[0]
        return hwnd

    def right_click(self, coords):
        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                #coords = win32gui.ScreenToClient(self.hwnd, coords)
                win32gui.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN, 0, win32api.MAKELONG(coords[0],coords[1]))
                win32gui.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(coords[0],coords[1]))

    def left_click(self, coords):
        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                # coords = win32gui.ScreenToClient(self.hwnd, coords)
                win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, win32api.MAKELONG(coords[0],coords[1]))
                win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coords[0],coords[1]))

    def send_keys(self, msg):
        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                for c in msg:
                    win32api.SendMessage(self.hwnd, win32con.WM_CHAR, ord(str(c)), 0)

    def delete(self):
        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                for i in range(0, 10):
                    win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_BACK, 0)
                    win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_BACK, 0)

    def send_enter(self):
        if win32gui.IsWindowVisible(self.hwnd):
            if 'Tibia' in win32gui.GetWindowText(self.hwnd):
                win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    @staticmethod
    def background_screenshot():

        hwnd = Windows_Interface.get_handle(Windows_Interface)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        #left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if result == 1:
            im.save("testa.png")
            im = np.array(im)
            im = im[:, :, ::-1].copy()
            return im
