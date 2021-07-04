from win32api import keybd_event, GetKeyState
from pynput import keyboard


class Ls:
    def __init__(self):
        self.kpress = {keyboard.Key.space: 0xb3, keyboard.Key.left: 0xb1, keyboard.Key.up: 0xaf,
                       keyboard.Key.right: 0xb0, keyboard.Key.down: 0xae}   # keys to media keys
        self.kpress = {x.value.vk: self.kpress[x] for x in self.kpress.keys()}  # extract the values of the special keys
        self.kpress[ord('M')] = 0xAD
        
        self.toggler = {keyboard.Key.up: headphones, keyboard.Key.down: speakers}
        self.toggler = {x.value.vk: self.toggler[x] for x in self.toggler.keys()}

        self.ctrl = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release,
                                          win32_event_filter=self.fil)
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        """
        checks whether control and alt are pressed
        :param key: key being pressed
        """
        if self.is_control(key):
            self.ctrl = True
        
        elif 'value' in dir(key):
            if key.value.vk not in list(self.kpress.values()): # disable overide if hotkey isn't pressed
                self.ctrl = False


    def on_release(self, key):
        """
        checks if the control key was released
        :param key: key being released
        """
        if self.is_control(key):
            self.ctrl = False
        
        elif self.is_shift(key):
            self.shift = False

    def fil(self, msg, data):
        """
        activate media keys based on received keys
        :param msg: msg received
        :param data: data received
        """
        # print(data.flags)
        if not self.is_caps_on() and self.ctrl and data.vkCode in self.kpress.keys() and data.flags < 2:
            self.key_event(self.kpress[data.vkCode])    # simulate media key press
            self.listener.suppress_event()  # stop the keys from getting sent to the rest of the system
    


    @staticmethod
    def is_caps_on():
        """
        return true if caps lock is enabled
        """
        return GetKeyState(keyboard.Key.caps_lock.value.vk)
    
    @staticmethod
    def key_event(e):
        """
        press key
        :param e: key to press
        """
        keybd_event(e, 0)

    @staticmethod
    def is_control(k):
        """
        return true if control was pressed
        :param k: key pressed
        """
        return k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r



if __name__ == '__main__':
    Ls()
