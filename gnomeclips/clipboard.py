import subprocess
from threading import Timer
from gi.repository import Gtk, Gdk, GLib, GObject


# Based on GPaste's clipboard code
class Clipboard(GObject.Object):
    text: str = GObject.Property(type=str)

    def __init__(self, libdir):
        super().__init__()
        self.libdir = libdir
        self.clipboard: Gtk.Clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.connect("owner-change", self.on_ownership_change)

        display: Gdk.Display = Gdk.Display.get_default()
        requires_active_polling = not display.request_selection_notification(Gdk.SELECTION_CLIPBOARD)

        if requires_active_polling:
            GLib.source_set_name_by_id(GLib.timeout_add_seconds(1, self.poll_clipboard), '[Clips] poll clipboard')

        if self.clipboard.wait_is_text_available() or self.clipboard.wait_is_uris_available():
            self.clipboard.request_text(self.on_receive_text)

    def set_text(self, text):
        self.clipboard.set_text(text, -1)

    def paste(self, text=None):
        if text is not None:
            self.set_text(text)
        timer = Timer(0.1, lambda: subprocess.call([f'{self.libdir}/gnome-clips-paste']))
        timer.start()

    # Signal handlers

    def on_ownership_change(self, clipboard, event):
        self.clipboard.request_text(self.on_receive_text)

    def on_receive_text(self, clipboard, text):
        if text != self.text:
            self.text = text

    # Repeating events

    def poll_clipboard(self):
        if self.text is not None:
            self.clipboard.request_text(self.on_receive_text)
        return True  # continue polling