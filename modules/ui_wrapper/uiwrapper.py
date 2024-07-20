import pyautogui
import pydirectinput
import ctypes
import time

class UiWrapper:

    def __init__(self):
        pydirectinput.PAUSE = 0
        pyautogui.PAUSE = 0

    # Keyboard actions
    def press_key(self, key):
        if key == "win" or not pydirectinput.press(key):
            pyautogui.press(key)

    def hold_key(self, key):
        if key == "win" or not pydirectinput.keyDown(key):
            pyautogui.keyDown(key)

    def release_key(self, key):
        if key == "win" or not pydirectinput.keyUp(key):
            pyautogui.keyUp(key)

    

    def type_text(self, text):
        pydirectinput.write(text)

    # Mouse actions
    def move_mouse(self, x, y):
        pyautogui.moveRel(x, y)

    def move_mouse_smooth(self, x, y, duration):
        pyautogui.moveRel(x, y, duration)

    def mouse_down(self, button):
        pyautogui.mouseDown(button=button)

    def mouse_up(self, button):
        pyautogui.mouseUp(button=button)

    def click_mouse(self, button='left'):
        pyautogui.click(button=button)

    def scroll(self, amount):
        pyautogui.scroll(amount)

    def hscroll(self, amount):
        pyautogui.hscroll(amount)

    # Volume control
    def change_volume(self, volume_level):
        volume = int(volume_level * 65535 / 100)  # Convert percentage to 0-65535 range
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0, (volume << 16) | 0xA0000)

    # Brightness control
    def change_brightness(self, brightness_level):
        brightness = int(brightness_level * 100 / 100)  # Convert percentage to 0-100 range
        monitors = ctypes.windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR
        num_monitors = ctypes.c_uint()
        hmonitor = ctypes.windll.user32.MonitorFromWindow(ctypes.windll.user32.GetDesktopWindow(), 0)
        if monitors(hmonitor, ctypes.byref(num_monitors)):
            hPhysicalMonitorsArray = (ctypes.c_uint * num_monitors.value)()
            ctypes.windll.dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, num_monitors.value, hPhysicalMonitorsArray)
            for i in range(num_monitors.value):
                ctypes.windll.dxva2.SetMonitorBrightness(hPhysicalMonitorsArray[i], brightness)