"""
FetchCraft Application Entry Point
"""

import sys
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GLib

from .window import MainWindow

class FetchCraftApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.cleanarch.FetchCraft",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.connect("startup", self._on_startup)
        self.connect("activate", self._on_activate)

    def _on_startup(self, _app):
        self.set_accels_for_action("win.about", ["F1"])

    def _on_activate(self, _app):
        win = self.props.active_window
        if not win:
            win = MainWindow(self)
        win.present()

def main():
    app = FetchCraftApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
