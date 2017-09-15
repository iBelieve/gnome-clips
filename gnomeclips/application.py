import os
from gi.repository import GLib, Gtk
from .history import ClipboardHistory
from .window import Window


class Application(Gtk.Application):
    history: ClipboardHistory = None

    def __init__(self, version, libdir):
        super().__init__(application_id='org.gnome.Clips')

        self.version = version
        self.libdir = libdir
        self.datadir = os.path.join(GLib.get_user_data_dir(), 'gnome-clips')

        GLib.set_application_name('Clips')
        GLib.set_prgname('gnome-clips')

    # Signal handlers

    def do_startup(self):
        Gtk.Application.do_startup(self)
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)
        self.history = ClipboardHistory(libdir=self.libdir, datadir=self.datadir)

    def do_activate(self):
        Gtk.Application.do_activate(self)
        window = Window(self.history)
        window.show_all()

