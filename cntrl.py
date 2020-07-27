from win32api import keybd_event
from pynput import keyboard
# from pyWinCoreAudio import *
# from win10toast import ToastNotifier


class Ls:
    def __init__(self):
        self.kpress = {keyboard.Key.space: 0xb3, keyboard.Key.left: 0xb1, keyboard.Key.up: 0xaf,
                       keyboard.Key.right: 0xb0, keyboard.Key.down: 0xae}   # keys to media keys
        self.kpress = {x.value.vk: self.kpress[x] for x in self.kpress.keys()}  # extract the values of the special keys
        self.kpress[ord('M')] = 0xAD

        # for dev in AudioDevices:
        #     if dev.id == u'{0.0.0.00000000}.{8e681bfb-d3c5-4c99-8528-8494b70c0715}':
        #         speakers = dev.render_endpoints[0]
        #         print(speakers.name)
            
        #     elif dev.id == u'{0.0.0.00000000}.{cc93aa5e-405a-4dca-a3ed-d0d1efadd906}':
        #         headphones = dev.render_endpoints[0]
        #         print(headphones.name)
        
        # self.toggler = {keyboard.Key.up: headphones, keyboard.Key.down: speakers}
        # self.toggler = {x.value.vk: self.toggler[x] for x in self.toggler.keys()}

        # self.toaster = ToastNotifier()
        self.ctrl = False
        self.shift = False
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
        # print(dir(key))
        # print(key)
        if self.is_control(key):
            # print('Pressed')
            self.ctrl = True
        
        # elif self.is_shift(key):
        #     self.shift = True
            
        # elif 'value' in dir(key):
        #     if key.value not in list(self.kpress.values()): # disable overide if hotkey isn't pressed
        #         self.ctrl = False

        # if self.ctrl and self.is_alt(key):
        if self.is_caps(key):
            self.enabled = not self.enabled
            # self.toaster.show_toast('Media Controller',
            #                         'Media keys are {}'.format('enabled' if self.enabled else 'disabled'), duration=1.5,
            #                         threaded=True)

    def on_release(self, key):
        """
        checks if the control key was released
        :param key: key being released
        """
        if self.is_control(key):
            # print('Released')
            self.ctrl = False
        
        # elif self.is_shift(key):
        #     self.shift = False

    def fil(self, msg, data):
        """
        activate media keys based on received keys
        :param msg: msg received
        :param data: data received
        """
        # print(data.flags)
        if self.enabled and self.ctrl and data.vkCode in self.kpress.keys() and data.flags < 2:
            if self.shift:
                print(self.toggler[data.vkCode].set_default)
                self.toggler[data.vkCode].set_default()

            else:
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
    def is_shift(k):
        """
        checks whether a key that was pressed is control
        :param k: key pressed
        """
        return k == keyboard.Key.shift_l or k == keyboard.Key.shift_r

    @staticmethod
    def is_caps(k):
        """
        checks whether the key that was pressed is alt
        :param k: key pressed
        """
        return k == keyboard.Key.caps_lock


if __name__ == '__main__':
    Ls()
