from win32api import keybd_event
from pynput import keyboard


class Ls(object):
    def __init__(self):
        self.kpress = {keyboard.Key.space: 0xb3, keyboard.Key.left: 0xb1, keyboard.Key.up: 0xaf,
                     keyboard.Key.right: 0xb0, keyboard.Key.down: 0xae}
        self.kpress = {x.value.vk: self.kpress[x] for x in self.kpress.keys()}
        self.kpress[ord('M')] = 0xAD

        self.ctrl = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release,
                                          win32_event_filter=self.fil)
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        if self.is_control(key):
            self.ctrl = True

    def on_release(self, key):
        if self.is_control(key):
            self.ctrl = False

    def fil(self, msg, data):
        if self.ctrl and data.vkCode in self.kpress.keys() and data.flags < 2:
            self.key_event(self.kpress[data.vkCode])
            self.listener.suppress_event()

    @staticmethod
    def key_event(e):
        keybd_event(e, 0)

    @staticmethod
    def is_control(k):
        return k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r

if __name__ == '__main__':
    Ls()
