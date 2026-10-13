"""
FetchCraft Live Preview Panel
Embeds a Vte.Terminal widget rendering real-time fastfetch output with debounced execution.
"""

import os
import re
import subprocess
import threading
from typing import Optional

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Gtk, Adw, Vte, Gdk, Pango, GLib

from .config_manager import ConfigManager
from .i18n import tr

CATPPUCCIN_PALETTE = [
    "#45475a", "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7", "#94e2d5", "#bac2de",
    "#585b70", "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7", "#94e2d5", "#a6adc8"
]

class PreviewPanel(Gtk.Box):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.config_manager = config_manager
        self._debounce_source_id: Optional[int] = None
        self._font_size: int = 10
        self._last_raw_output: str = ""

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)

        self._build_header()
        self._build_terminal()

        # Listen to config changes
        self.config_manager.add_change_listener(self.request_refresh)

        # Initial refresh
        GLib.idle_add(self.request_refresh)

    def _build_header(self):
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Title with terminal badge
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon = Gtk.Image.new_from_icon_name("utilities-terminal-symbolic")
        self.title_label = Gtk.Label(label=tr("preview_heading"))
        self.title_label.add_css_class("heading")
        title_box.append(icon)
        title_box.append(self.title_label)

        header_box.append(title_box)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header_box.append(spacer)

        # Spinner
        self.spinner = Gtk.Spinner()
        header_box.append(self.spinner)

        # Font zoom out
        self.zoom_out_btn = Gtk.Button.new_from_icon_name("zoom-out-symbolic")
        self.zoom_out_btn.set_tooltip_text(tr("preview_zoom_out_tip"))
        self.zoom_out_btn.connect("clicked", self._on_zoom_out)
        header_box.append(self.zoom_out_btn)

        # Font zoom in
        self.zoom_in_btn = Gtk.Button.new_from_icon_name("zoom-in-symbolic")
        self.zoom_in_btn.set_tooltip_text(tr("preview_zoom_in_tip"))
        self.zoom_in_btn.connect("clicked", self._on_zoom_in)
        header_box.append(self.zoom_in_btn)

        # Copy button
        self.copy_btn = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        self.copy_btn.set_tooltip_text(tr("preview_copy_tip"))
        self.copy_btn.connect("clicked", self._on_copy_clicked)
        header_box.append(self.copy_btn)

        # Manual Refresh button
        self.refresh_btn = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        self.refresh_btn.set_tooltip_text(tr("preview_refresh_tip"))
        self.refresh_btn.connect("clicked", lambda _: self.request_refresh(force=True))
        header_box.append(self.refresh_btn)

        self.append(header_box)

    def retranslate(self):
        self.title_label.set_label(tr("preview_heading"))
        self.zoom_out_btn.set_tooltip_text(tr("preview_zoom_out_tip"))
        self.zoom_in_btn.set_tooltip_text(tr("preview_zoom_in_tip"))
        self.copy_btn.set_tooltip_text(tr("preview_copy_tip"))
        self.refresh_btn.set_tooltip_text(tr("preview_refresh_tip"))

    def _build_terminal(self):
        frame = Gtk.Frame()
        frame.add_css_class("card")
        frame.set_hexpand(True)
        frame.set_vexpand(True)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.term = Vte.Terminal()
        self.term.set_hexpand(True)
        self.term.set_vexpand(True)
        self.term.set_cursor_blink_mode(Vte.CursorBlinkMode.OFF)
        self.term.set_mouse_autohide(True)
        self.term.set_scrollback_lines(2000)

        self._apply_terminal_style()

        scrolled.set_child(self.term)
        frame.set_child(scrolled)
        self.append(frame)

    def _apply_terminal_style(self):
        fg = Gdk.RGBA()
        fg.parse("#cdd6f4")
        bg = Gdk.RGBA()
        bg.parse("#181825")

        palette = []
        for h in CATPPUCCIN_PALETTE:
            c = Gdk.RGBA()
            c.parse(h)
            palette.append(c)

        self.term.set_colors(fg, bg, palette)
        self.term.set_font(Pango.FontDescription.from_string(f"monospace {self._font_size}"))

    def _on_zoom_in(self, _btn):
        if self._font_size < 18:
            self._font_size += 1
            self._apply_terminal_style()

    def _on_zoom_out(self, _btn):
        if self._font_size > 7:
            self._font_size -= 1
            self._apply_terminal_style()

    def _on_copy_clicked(self, _btn):
        if not self._last_raw_output:
            return
        # Strip ANSI escape codes
        plain_text = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", self._last_raw_output)
        clipboard = self.get_display().get_clipboard()
        clipboard.set(plain_text)

        # Notify parent window if toast overlay available
        root = self.get_root()
        if hasattr(root, "show_toast"):
            root.show_toast("Copied terminal output to clipboard!")

    def request_refresh(self, force: bool = False):
        """Debounced preview refresh."""
        if self._debounce_source_id is not None:
            GLib.source_remove(self._debounce_source_id)
            self._debounce_source_id = None

        if force:
            self._execute_fastfetch()
        else:
            self._debounce_source_id = GLib.timeout_add(120, self._on_debounce_timer)

    def _on_debounce_timer(self) -> bool:
        self._debounce_source_id = None
        self._execute_fastfetch()
        return GLib.SOURCE_REMOVE

    def _execute_fastfetch(self):
        self.spinner.start()
        tmp_config_path = self.config_manager.write_temp_preview()

        def worker():
            try:
                res = subprocess.run(
                    ["fastfetch", "-c", tmp_config_path],
                    capture_output=True,
                    text=False,
                    timeout=5
                )
                raw_bytes = res.stdout if res.returncode == 0 else (res.stdout + b"\n" + res.stderr)
                raw_str = raw_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                raw_bytes = f"\x1b[31mError running fastfetch: {e}\x1b[0m\r\n".encode("utf-8")
                raw_str = str(e)

            GLib.idle_add(self._update_terminal_content, raw_bytes, raw_str)

        threading.Thread(target=worker, daemon=True).start()

    def _update_terminal_content(self, raw_bytes: bytes, raw_str: str):
        self._last_raw_output = raw_str
        self.spinner.stop()

        # Normalize line endings to \r\n for VTE
        normalized = raw_bytes.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")

        self.term.reset(True, True)
        self.term.feed(normalized)
        return False
