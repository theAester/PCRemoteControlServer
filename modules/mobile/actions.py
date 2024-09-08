import json
from pyautogui import FailSafeException

class Actions:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.timestamp = 0

    def handle_action(self, actionstr):
        obj = json.loads(actionstr)
        match obj['type']:
            case "begin":
                self.timestamp = 0
            case "end":
                pass
            case "nop":
                pass # nop
            case "motion":
                try:
                    self.handle_motion(obj)
                except FailSafeException:
                    print("Warning: do not get close to the corners with the cursor")
                except Exception as e:
                    print("Warning: " + str(e))
            case "vscroll":
                self.handle_vscroll(obj)
            case "hscroll":
                self.handle_hscroll(obj)
            case "mouse-down":
                self.handle_mouse_down(obj)
            case "mouse-up":
                self.handle_mouse_up(obj)
            case "press":
                self.handle_press(obj)
            case "hold":
                self.handle_hold(obj)
            case "release":
                self.handle_release(obj)

    def handle_motion(self, obj):
        x = float(obj['x'])
        y = float(obj['y'])
        ts = int(obj['timestamp'])
        if self.timestamp == 0:
            self.timestamp = ts
            self.wrapper.move_mouse(x,y)
        else:
            dur = ts - self.timestamp
            dur /= 1000
            self.timestamp = ts
            self.wrapper.move_mouse_smooth(x,y,dur)
        

    def handle_mouse_down(self, obj):
        button = obj['button']
        self.wrapper.mouse_down(button)

    def handle_mouse_up(self, obj):
        button = obj['button']
        self.wrapper.mouse_up(button)

    def handle_vscroll(self, obj):
        value = int(obj['value'])
        self.wrapper.scroll(value)

    def handle_hscroll(self, obj):
        value = int(obj['value'])
        self.wrapper.hscroll(value)

    def handle_press(self, obj):
        val = obj['key']
        self.wrapper.press_key(val)

    def handle_hold(self, obj):
        val = obj['key']
        self.wrapper.hold_key(val)

    def handle_release(self, obj):
        val = obj['key']
        self.wrapper.release_key(val)