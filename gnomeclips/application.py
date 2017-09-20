import os

from gi.repository import GLib, Gtk, Gio

from .history import ClipboardHistory
from .keybindings import Keybindings
from .popup import HistoryPopup
from .utils import USER_DATA_DIR, AUTOSTART_DIR, AUTOSTART_FILE, present_window
from .window import Window


class Application(Gtk.Application):
    window: Window = None
    popup: HistoryPopup = None
    history: ClipboardHistory = None

    def __init__(self, version, pkgdatadir, libdir):
        super().__init__(application_id='org.gnome.Clips')

        self.version = version
        self.pkgdatadir = pkgdatadir
        self.libdir = libdir

        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)

        self.settings = Gio.Settings(schema_id='org.gnome.Clips')

        GLib.set_application_name('Clips')
        GLib.set_prgname('gnome-clips')

    # Signal handlers

    def do_startup(self):
        Gtk.Application.do_startup(self)
        if not os.path.exists(USER_DATA_DIR):
            os.mkdir(USER_DATA_DIR)
        if self.is_enabled:
            self.hold()
        self.history = ClipboardHistory(libdir=self.libdir, enabled=self.is_enabled)
        self.keybindings = Keybindings()
        self.update_daemon()
        self.update_keybindings()

    def do_activate(self):
        Gtk.Application.do_activate(self)
        if self.window is None:
            self.window = Window(self, self.history)
            self.window.connect('destroy', self.on_window_destroyed)
        self.window.show_all()

    def show_popup(self):
        if self.popup is not None:
            return
        self.popup = HistoryPopup(application=self, clipboard_history=self.history)
        self.popup.connect('destroy', self.on_popup_destroyed)
        self.popup.show_all()
        present_window(self.popup)

    def on_popup_destroyed(self, popup):
        self.popup = None

    def on_window_destroyed(self, window):
        self.window = None

    # Daemon management

    @property
    def is_enabled(self):
        return self.settings.get_boolean('is-enabled')

    @is_enabled.setter
    def is_enabled(self, enabled):
        if enabled != self.is_enabled:
            if enabled:
                self.hold()
            else:
                self.release()
        self.settings.set_boolean('is-enabled', enabled)
        self.history.set_enabled(enabled)
        self.update_daemon()
        self.update_keybindings()

    def update_daemon(self):
        target = os.path.join(AUTOSTART_DIR, AUTOSTART_FILE)

        if self.is_enabled:
            if not os.path.exists(target):
                if os.path.islink(target):
                    os.remove(target)
                os.symlink(os.path.join(self.pkgdatadir, AUTOSTART_FILE), target)
        else:
            if os.path.exists(target):
                os.remove(target)

    def update_keybindings(self):
        if self.is_enabled:
            self.keybindings.add('<Ctrl><Shift>V', self.show_popup)
        else:
            self.keybindings.remove_all()
