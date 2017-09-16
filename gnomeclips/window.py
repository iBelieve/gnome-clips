from gi.repository import Gtk

from .history import ClipboardHistory
from .historylist import HistoryList


class Window(Gtk.ApplicationWindow):
    def __init__(self, application, clipboard_history: ClipboardHistory):
        super().__init__(application=application, title="Clips")
        self.application = application
        self.clipboard_history = clipboard_history

        self.setup_ui()

    # UI Setup

    def setup_ui(self):
        self.paned = Gtk.Paned()
        self.setup_header()
        self.setup_sidebar()
        self.setup_content()
        self.setup_clipboard_list()
        self.add(self.paned)

    def setup_header(self):
        header = Gtk.HeaderBar(title="Clips", show_close_button=True)
        self.enabled_switch = Gtk.Switch(active=self.application.is_enabled)
        self.enabled_switch.connect('notify::active', self.on_enabled_toggled)
        header.pack_start(self.enabled_switch)

        clear_button: Gtk.Button = Gtk.Button.new_from_icon_name("edit-clear-all-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        clear_button.props.tooltip_text = "Clear the clipboard history"
        clear_button.connect("clicked", self.on_clear_clipboard)
        header.pack_end(clear_button)

        self.set_titlebar(header)

    def setup_sidebar(self):
        listbox = Gtk.ListBox()
        listbox.set_size_request(200, -1)
        listbox.add(ClipboardItem(self.clipboard_history))
        listbox.get_style_context().add_class("sidebar")

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(listbox)
        self.paned.pack1(scrolled, False, False)

    def setup_content(self):
        self.stack = Gtk.Stack()
        self.stack.set_size_request(600, 550)
        self.paned.pack2(self.stack, True, False)

    def setup_clipboard_list(self):
        self.history_list = HistoryList(self.clipboard_history)
        self.stack.add_named(self.history_list.scrolled(), 'clipboard')

    # Signal handlers

    def on_enabled_toggled(self, switch, paramspec):
        self.application.is_enabled = switch.props.active

    def on_clear_clipboard(self, buttom):
        self.clipboard_history.clear()


class ClipboardItem(Gtk.ListBoxRow):
    def __init__(self, clipboard_history: ClipboardHistory):
        super().__init__()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.add(Gtk.Label(label="Clipboard", margin=8, xalign=0, hexpand=True))
        self.count_label = Gtk.Label(label=str(len(clipboard_history.items)),
                                     margin_right=8, valign=Gtk.Align.CENTER)
        self.count_label.get_style_context().add_class(Gtk.STYLE_CLASS_DIM_LABEL)
        box.add(self.count_label)
        self.add(box)

        clipboard_history.connect("changed", self.on_history_changed)

    def on_history_changed(self, clipboard_history: ClipboardHistory):
        self.count_label.props.label = str(len(clipboard_history.items))
