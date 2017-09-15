GNOME Clips
===========

Simple clipboard manager inspired by [Pastebot](https://tapbots.com/pastebot) for macOS.

# Current Features

* Popup window showing clipboard history
* Click an item to paste it into the currently selected text area/field
* Start typing to filter the clipboard history
* Press enter to paste the first item, or use the arrow keys to select past clipboard items
* Press escape or switch to another window to dismiss the popup

# To Do

* Proper daemon that auto-starts
* Integrate with GNOME Shell to provide global keyboard shortcuts automatically
* Sort out uinput permissions

# How it works

The app launches using the X11 GDK backend so we can monitor the clipboard even without the app window open. 
We use a global keyboard shortcut to pop open the window. When the user selects a list item, it is set as the current 
clipboard item, the window is closed, and after 0.1s, Ctrl+V is triggered, pasting the text the user picked into the
currently selected widget.

# Dependencies

* Python 3
* PyGObject

# Installation

    mkdir build; cd build
    meson ..
    make
    [sudo] make install
    
Make sure the `uinput` module is loaded and `/dev/uinput` is readable/writable by your user (used to trigger 
the paste action).

Now go to GNOME Settings -> Keyboard, scroll to the bottom, and add a custom shortcut, setting the command 
to `gnome-clips` (or `/path/to/gnome-clips` if it's not in your system PATH), and pick a nice keyboard shortcut
(I use `Ctrl + Shift + V`).