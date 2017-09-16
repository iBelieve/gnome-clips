from gi.repository import Gtk, Pango

from .history import ClipboardHistory


class HistoryList(Gtk.ListBox):
    list_items = []

    def __init__(self, clipboard_history: ClipboardHistory):
        super().__init__(selection_mode=Gtk.SelectionMode.NONE)
        self.clipboard_history = clipboard_history
        self.clipboard_history.connect('changed', lambda history: self.update_ui())

        self.set_header_func(self.list_divider_func)
        self.update_ui()

    def scrolled(self):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self)
        return scrolled

    # Miscellaneous methods

    def set_filter(self, filter: str):
        if filter:
            def filter_func(row):
                return filter in row.item

            self.set_filter_func(filter_func)
        else:
            self.set_filter_func(None)

    def update_ui(self):
        for list_item in self.list_items:
            self.remove(list_item)
        self.list_items = []

        for item in reversed(self.clipboard_history.items):
            list_item = HistoryItem(item)
            list_item.show_all()
            self.add(list_item)
            if len(self.list_items) == 0:
                list_item.grab_focus()
            self.list_items.append(list_item)

    # Copied from GNOME Tweaks
    def list_divider_func(self, row, before):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))


class HistoryItem(Gtk.ListBoxRow):
    def __init__(self, item: str):
        super().__init__()
        self.item = item
        self.label = Gtk.Label(margin=8, xalign=0, halign=Gtk.Align.FILL,
                               ellipsize=Pango.EllipsizeMode.END,
                               label=item.replace('\n', ' '))
        self.label.set_line_wrap(True)
        self.label.set_lines(2)
        self.add(self.label)
