from enum import IntFlag

from gi.repository import Gio, GLib


# ShellActionMode stolen from gnome-shell
class ShellActionMode(IntFlag):
    NONE = 0  # block action
    NORMAL = 1 << 0  # allow action when in window mode, e.g. when the focus is in an application window
    OVERVIEW = 1 << 1  # allow action while the overview is active
    LOCK_SCREEN = 1 << 2  # allow action when the screen is locked, e.g. when the screen shield is shown
    UNLOCK_SCREEN = 1 << 3  # allow action in the unlock dialog
    LOGIN_SCREEN = 1 << 4  # allow action in the login screen
    SYSTEM_MODAL = 1 << 5  # allow action when a system modal dialog (e.g. authentification or session dialogs) is open
    LOOKING_GLASS = 1 << 6  # allow action in looking glass
    POPUP = 1 << 7  # allow action while a shell menu is open
    ALL = 0xFF  # always allow action


class Keybindings:
    callbacks = dict()

    def __init__(self):
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.proxy = Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None,
                                            'org.gnome.Shell',
                                            '/org/gnome/Shell',
                                            'org.gnome.Shell', None)
        self.proxy.connect('g-signal', self.on_signal)

    def add(self, keybinding, callback):
        uid = self.proxy.GrabAccelerator('(su)', '<Ctrl><Shift>V', ShellActionMode.ALL)
        self.callbacks[uid] = callback

    def remove_all(self):
        for action in self.callbacks.keys():
            self.proxy.UngrabAccelerator('(u)', action)
        self.callbacks = dict()

    def on_signal(self, proxy, sender, signal, parameters: GLib.Variant):
        if signal == 'AcceleratorActivated':
            callback = self.callbacks[parameters[0]]
            callback()
