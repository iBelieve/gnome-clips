from gi.repository import Gtk, Gdk

from .history import ClipboardHistory
from .historylist import HistoryList


class HistoryPopup(Gtk.Window):
    def __init__(self, clipboard_history: ClipboardHistory):
        super().__init__(title='Clips', resizable=False,
                         skip_pager_hint=True, skip_taskbar_hint=True)
        self.clipboard = clipboard_history.clipboard
        self.clipboard_history = clipboard_history

        self.setup_ui()
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(500, 600)

    # UI Setup

    def setup_ui(self):
        self.setup_header()
        self.setup_list()

    def setup_header(self):
        headerbar = Gtk.HeaderBar()
        self.filter_entry = Gtk.Entry(placeholder_text='Filter...', hexpand=True)
        self.filter_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "edit-find-symbolic")
        self.filter_entry.connect('changed', self.on_filter_changed)
        headerbar.set_custom_title(self.filter_entry)
        self.set_titlebar(headerbar)

    def setup_list(self):
        self.list = HistoryList(self.clipboard_history)
        self.list.connect('row-activated', self.on_row_select)
        self.add(self.list.scrolled())

    # Signal handlers

    def do_key_release_event(self, event: Gdk.Event):
        Gtk.Window.do_key_release_event(self, event)
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()
        elif len(event.string) > 0 and not self.filter_entry.props.is_focus:
            self.filter_entry.set_text(event.string)
            self.filter_entry.set_position(len(event.string))
            self.filter_entry.grab_focus_without_selecting()

    def do_focus_out_event(self, event):
        self.destroy()
        return Gtk.Window.do_focus_out_event(self, event)

    def on_row_select(self, listbox, row):
        self.destroy()
        self.clipboard.paste(row.item)

    def on_filter_changed(self, entry):
        self.listbox.set_filter(entry.props.text)
