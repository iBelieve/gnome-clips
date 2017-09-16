import os

from gi.repository import GLib

USER_DATA_DIR = os.path.join(GLib.get_user_data_dir(), 'gnome-clips')
AUTOSTART_DIR = os.path.join(GLib.get_user_config_dir(), 'autostart')
AUTOSTART_FILE = 'org.gnome.Clips.Autostart.desktop'


def guess_language(snippet: str):
    try:
        from pygments.lexers import guess_lexer
        from pygments.lexer import Lexer

        lexer: Lexer = guess_lexer(snippet)
        return repr(lexer)
    except:
        return None
