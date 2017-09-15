from gi.repository import Gtk, Gdk
from .history import ClipboardHistory


class Window(Gtk.Window):
    list_items = []
    filter = ''

    def __init__(self, clipboard_history: ClipboardHistory):
        super().__init__(title='Clips', resizable=False,
                         skip_pager_hint=True, skip_taskbar_hint=True)
        self.clipboard = clipboard_history.clipboard
        self.clipboard_history = clipboard_history
        self.clipboard_history.connect('changed', lambda history: self.update_ui())

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
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox.set_header_func(self.list_divider_func)
        self.listbox.connect('row-activated', self.on_row_select)

        scrolled.add(self.listbox)
        self.add(scrolled)

    # Signal handlers

    def do_show(self):
        Gtk.Window.do_show(self)
        self.update_ui()

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
        print('Row selected', row.item)
        self.destroy()
        self.clipboard.paste(row.item)

    def on_filter_changed(self, entry):
        self.filter = entry.props.text

        def filter_func(row):
            return len(self.filter) == 0 or self.filter in row.item

        self.listbox.set_filter_func(filter_func)

    # Miscellaneous methods

    def update_ui(self):
        if not self.props.visible:
            return

        for list_item in self.list_items:
            self.listbox.remove(list_item)
        self.list_items = []

        for item in reversed(self.clipboard_history.items):
            list_item = HistoryItem(item)
            list_item.show_all()
            self.listbox.add(list_item)
            if len(self.list_items) == 0:
                list_item.grab_focus()
            self.list_items.append(list_item)

    # Copied from GNOME Tweaks
    def list_divider_func(self, row, before):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))


class HistoryItem(Gtk.ListBoxRow):
    def __init__(self, item):
        super().__init__()
        self.item = item

        self.label = Gtk.Label(margin=8, xalign=0, label=item)
        self.label.set_line_wrap(True)
        self.add(self.label)
