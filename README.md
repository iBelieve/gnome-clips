GNOME Clips
===========

Simple clipboard manager inspired by [Pastebot](https://tapbots.com/pastebot) for macOS.

![Screenshot](/screenshot.png?raw=true)

### Current Features

* Simple app window to view history and enable/disable the paste popup and history monitoring
* Global shortcut (Ctrl+Shift+V) to open poup showing clipboard history
* Click an item to paste it into the currently selected text area/field
* Start typing to filter the clipboard history
* Press enter to paste the first item, or use the arrow keys to select past clipboard items
* Press escape or switch to another window to dismiss the popup

### To Do

* Sort out uinput permissions

### How it works

The app launches using the X11 GDK backend so we can monitor the clipboard even without the app window open. 
We hook into GNOME shell and register a global key binding that opens the history popup. When the user selects a 
list item, it is set as the current clipboard item, the window is closed, and after 0.1s, Ctrl+V is triggered, 
pasting the text the user picked into the currently selected widget.

### Dependencies

* Python 3
* PyGObject

### Installation

    mkdir build; cd build
    meson ..
    ninja
    [sudo] ninja install
    
Make sure the `uinput` module is loaded and `/dev/uinput` is readable/writable by your user (used to trigger 
the paste action).

Now open GNOME Clips and flip the switch to on in the header bar!