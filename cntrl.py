from win32api import keybd_event
from pynput import keyboard
from win10toast import ToastNotifier


class Ls:
    def __init__(self):
        self.kpress = {keyboard.Key.space: 0xb3, keyboard.Key.left: 0xb1, keyboard.Key.up: 0xaf,
                       keyboard.Key.right: 0xb0, keyboard.Key.down: 0xae}   # keys to media keys
        self.kpress = {x.value.vk: self.kpress[x] for x in self.kpress.keys()}  # extract the values of the special keys
        self.kpress[ord('M')] = 0xAD

        self.toaster = ToastNotifier()
        self.ctrl = False
        self.enabled = True
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

        if self.ctrl and self.is_alt(key):
            self.enabled = not self.enabled
            self.toaster.show_toast('Media Controller',
                                    'Media keys are {}'.format('enabled' if self.enabled else 'disabled'), duration=1.5,
                                    threaded=True)

    def on_release(self, key):
        """
        checks if the control key was released
        :param key: key being released
        """
        if self.is_control(key):
            self.ctrl = False

    def fil(self, msg, data):
        """
        activate media keys based on received keys
        :param msg: msg received
        :param data: data received
        """
        if self.enabled and self.ctrl and data.vkCode in self.kpress.keys() and data.flags < 2:
            self.key_event(self.kpress[data.vkCode])    # simulate media key press
            self.listener.suppress_event()  # stop the keys from getting sent to the rest of the system

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
        checks whether a key that was pressed is control
        :param k: key pressed
        """
        return k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r

    @staticmethod
    def is_alt(k):
        """
        checks whether the key that was pressed is alt
        :param k: key pressed
        """
        return k == keyboard.Key.alt_l or k == keyboard.Key.alt_r


if __name__ == '__main__':
    Ls()
