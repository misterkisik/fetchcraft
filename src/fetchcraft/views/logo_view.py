"""
FetchCraft Logo View
Configures ASCII / distro logos, custom logo files, and spacing.
"""

import os
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..models import POPULAR_LOGOS
from ..config_manager import ConfigManager

LOGO_TYPES = [
    ("auto", "Automatic (Default)"),
    ("builtin", "Fastfetch Built-in ASCII"),
    ("file", "Text / ASCII File"),
    ("kitty", "Kitty Terminal Graphics"),
    ("sixel", "Sixel Graphics Protocol"),
    ("chafa", "Chafa Terminal Characters"),
]

class LogoView(Adw.PreferencesPage):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self._updating = False

        self._build_logo_source_group()
        self._build_logo_layout_group()

        self.config_manager.add_change_listener(self._sync_from_config)
        self._sync_from_config()

    def _build_logo_source_group(self):
        self.source_group = Adw.PreferencesGroup(
            title="Logo Source &amp; Artwork",
            description="Select which distribution ASCII art or custom image to display."
        )

        labels = [name for _, name in POPULAR_LOGOS] + ["Other Built-in Name...", "Custom File..."]
        self._logo_keys = [code for code, _ in POPULAR_LOGOS]

        self.logo_combo = Adw.ComboRow(
            title="Distribution Logo",
            model=Gtk.StringList.new(labels)
        )
        self.logo_combo.connect("notify::selected", self._on_logo_changed)
        self.source_group.add(self.logo_combo)

        # Custom logo name entry (if "Other Built-in Name" is selected)
        self.custom_name_entry = Adw.EntryRow(title="Built-in Distro Name")
        self.custom_name_entry.set_visible(False)
        self.custom_name_entry.connect("changed", self._on_custom_name_changed)
        self.source_group.add(self.custom_name_entry)

        # Custom file row (if "Custom File" is selected)
        self.file_row = Adw.ActionRow(title="Logo File Path")
        self.file_entry = Gtk.Entry()
        self.file_entry.set_hexpand(True)
        self.file_entry.set_valign(Gtk.Align.CENTER)
        self.file_entry.set_placeholder_text("/path/to/ascii_or_image.txt")
        self.file_entry.connect("changed", self._on_file_path_changed)
        self.file_row.add_suffix(self.file_entry)

        browse_btn = Gtk.Button.new_from_icon_name("document-open-symbolic")
        browse_btn.set_valign(Gtk.Align.CENTER)
        browse_btn.set_tooltip_text("Browse Logo File...")
        browse_btn.connect("clicked", self._on_browse_file)
        self.file_row.add_suffix(browse_btn)

        self.file_row.set_visible(False)
        self.source_group.add(self.file_row)

        self.add(self.source_group)

    def _build_logo_layout_group(self):
        self.layout_group = Adw.PreferencesGroup(
            title="Logo Spacing &amp; Rendering",
            description="Fine-tune character padding between the logo and system metrics."
        )

        # Padding right
        adj = Gtk.Adjustment(value=2, lower=0, upper=15, step_increment=1, page_increment=1)
        self.padding_spin = Adw.SpinRow(title="Right Padding", adjustment=adj)
        self.padding_spin.set_subtitle("Number of empty columns between logo and text")
        self.padding_spin.connect("notify::value", self._on_padding_changed)
        self.layout_group.add(self.padding_spin)

        # Logo render type
        type_labels = [name for _, name in LOGO_TYPES]
        self._type_keys = [code for code, _ in LOGO_TYPES]

        self.type_combo = Adw.ComboRow(
            title="Logo Render Type",
            model=Gtk.StringList.new(type_labels)
        )
        self.type_combo.connect("notify::selected", self._on_type_changed)
        self.layout_group.add(self.type_combo)

        self.add(self.layout_group)

    def _sync_from_config(self):
        if self._updating:
            return
        self._updating = True

        curr_source = self.config_manager.get_logo_source()
        if curr_source in self._logo_keys:
            idx = self._logo_keys.index(curr_source)
            self.logo_combo.set_selected(idx)
            self.custom_name_entry.set_visible(False)
            self.file_row.set_visible(False)
        elif curr_source.startswith("/") or curr_source.startswith("~"):
            # File
            self.logo_combo.set_selected(len(self._logo_keys) + 1)
            self.file_entry.set_text(curr_source)
            self.file_row.set_visible(True)
            self.custom_name_entry.set_visible(False)
        else:
            # Custom built-in name
            self.logo_combo.set_selected(len(self._logo_keys))
            self.custom_name_entry.set_text(curr_source)
            self.custom_name_entry.set_visible(True)
            self.file_row.set_visible(False)

        # Padding
        curr_pad = self.config_manager.get_logo_padding_right()
        self.padding_spin.set_value(curr_pad)

        # Type
        curr_type = self.config_manager.get_logo_type()
        if curr_type in self._type_keys:
            self.type_combo.set_selected(self._type_keys.index(curr_type))
        else:
            self.type_combo.set_selected(0)

        self._updating = False

    def _on_logo_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if idx < len(self._logo_keys):
            self.custom_name_entry.set_visible(False)
            self.file_row.set_visible(False)
            self.config_manager.set_logo_source(self._logo_keys[idx])
        elif idx == len(self._logo_keys):
            # Other built-in
            self.custom_name_entry.set_visible(True)
            self.file_row.set_visible(False)
            name = self.custom_name_entry.get_text().strip()
            if name:
                self.config_manager.set_logo_source(name)
        else:
            # Custom file
            self.custom_name_entry.set_visible(False)
            self.file_row.set_visible(True)
            path = self.file_entry.get_text().strip()
            if path:
                self.config_manager.set_logo_source(path)

    def _on_custom_name_changed(self, entry):
        if self._updating or not entry.get_visible():
            return
        name = entry.get_text().strip()
        if name:
            self.config_manager.set_logo_source(name)

    def _on_file_path_changed(self, entry):
        if self._updating or not self.file_row.get_visible():
            return
        path = entry.get_text().strip()
        if path:
            self.config_manager.set_logo_source(path)

    def _on_browse_file(self, _btn):
        dialog = Gtk.FileDialog()
        dialog.set_title("Choose Logo Image or ASCII Art")
        root = self.get_root()

        def on_file_selected(_dialog, result):
            try:
                gfile = dialog.open_finish(result)
                if gfile:
                    path = gfile.get_path()
                    self.file_entry.set_text(path)
                    self.config_manager.set_logo_source(path)
            except Exception as e:
                print(f"[FetchCraft] File selection cancelled or error: {e}")

        dialog.open(root, None, on_file_selected)

    def _on_padding_changed(self, spin, _param):
        if self._updating:
            return
        pad = int(spin.get_value())
        self.config_manager.set_logo_padding_right(pad)

    def _on_type_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if 0 <= idx < len(self._type_keys):
            self.config_manager.set_logo_type(self._type_keys[idx])
