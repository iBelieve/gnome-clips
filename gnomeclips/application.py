import os

from gi.repository import GLib, Gtk, Gio

from .history import ClipboardHistory
from .utils import USER_DATA_DIR, AUTOSTART_DIR, AUTOSTART_FILE
from .window import Window


class Application(Gtk.Application):
    history: ClipboardHistory = None

    def __init__(self, version, pkgdatadir, libdir):
        super().__init__(application_id='org.gnome.Clips')

        self.version = version
        self.pkgdatadir = pkgdatadir
        self.libdir = libdir

        self.settings = Gio.Settings(schema_id='org.gnome.Clips')

        GLib.set_application_name('Clips')
        GLib.set_prgname('gnome-clips')

    # Signal handlers

    def do_startup(self):
        Gtk.Application.do_startup(self)
        if not os.path.exists(USER_DATA_DIR):
            os.mkdir(USER_DATA_DIR)
        self.update_daemon()
        self.history = ClipboardHistory(libdir=self.libdir, enabled=self.is_enabled)

    def do_activate(self):
        Gtk.Application.do_activate(self)
        window = Window(self, self.history)
        window.show_all()

    # Daemon management

    @property
    def is_enabled(self):
        return self.settings.get_boolean('is-enabled')

    @is_enabled.setter
    def is_enabled(self, enabled):
        self.settings.set_boolean('is-enabled', enabled)
        self.history.set_enabled(enabled)
        self.update_daemon()

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
