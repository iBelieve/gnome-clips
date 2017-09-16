import os

from gi.repository import GLib, Gtk

USER_DATA_DIR = os.path.join(GLib.get_user_data_dir(), 'gnome-clips')
AUTOSTART_DIR = os.path.join(GLib.get_user_config_dir(), 'autostart')
AUTOSTART_FILE = 'org.gnome.Clips.Autostart.desktop'


def present_window(window: Gtk.Window):
    if window.is_active():
        return

    timestamp = Gtk.get_current_event_time()
    if timestamp == 0:
        from gi.repository import GdkX11
        timestamp = GdkX11.x11_get_server_time(window.get_window())

    window.present_with_time(timestamp)
