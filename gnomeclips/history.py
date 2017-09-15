import os
import json
from gi.repository import GObject
from .clipboard import Clipboard


class ClipboardHistory(GObject.Object):
    __gsignals__ = {
        'changed': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    items = []

    def __init__(self, libdir, datadir):
        super().__init__()
        self.path = os.path.join(datadir, 'history')
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.items = json.load(f)

        self.clipboard = Clipboard(libdir)
        self.clipboard.connect('notify::text', self.on_text_changed)
        if self.clipboard.text is None and len(self.items) > 0:
            self.clipboard.text = self.items[-1]

    # Signal handlers

    def on_text_changed(self, clipboard, paramspec):
        # If the text already existed in the clipboard, we remove it and re-add
        # it to the top, effectively moving it to the top of the history
        if clipboard.text in self.items:
            self.items.remove(clipboard.text)
        self.items.append(clipboard.text)
        with open(self.path, 'w') as f:
            json.dump(self.items, f)
        self.emit('changed')
