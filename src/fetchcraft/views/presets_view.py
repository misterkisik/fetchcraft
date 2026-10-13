"""
FetchCraft Presets View
Allows loading curated built-in styles, community themes, and system fastfetch examples.
"""

import os
import glob
import json
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..models import BUILTIN_PRESETS
from ..config_manager import ConfigManager, strip_jsonc

SYSTEM_PRESETS_DIR = "/usr/share/fastfetch/presets"

class PresetsView(Adw.PreferencesPage):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager

        self._build_curated_group()
        self._build_system_group()
        self._build_backup_group()

    def _build_curated_group(self):
        group = Adw.PreferencesGroup(
            title="Curated FetchCraft Presets",
            description="Polished themes ready for Arch Linux desktops, minimal rices, and terminals."
        )

        for key, preset in BUILTIN_PRESETS.items():
            row = Adw.ActionRow(
                title=preset["name"],
                subtitle=preset["desc"]
            )
            row.set_icon_name(preset.get("icon", "emblem-favorite-symbolic"))

            apply_btn = Gtk.Button(label="Load Preset")
            apply_btn.add_css_class("suggested-action")
            apply_btn.set_valign(Gtk.Align.CENTER)
            apply_btn.connect("clicked", self._create_curated_handler(key, preset["name"]))
            row.add_suffix(apply_btn)

            row.set_activatable(True)
            row.connect("activated", self._create_curated_handler(key, preset["name"]))

            group.add(row)

        self.add(group)

    def _create_curated_handler(self, key: str, name: str):
        def handler(*_):
            self.config_manager.apply_preset(key)
            root = self.get_root()
            if hasattr(root, "show_toast"):
                root.show_toast(f"Loaded '{name}' preset!")
        return handler

    def _build_system_group(self):
        group = Adw.PreferencesGroup(
            title="Fastfetch System Presets",
            description="Official presets installed on your system in /usr/share/fastfetch/presets/."
        )

        if not os.path.isdir(SYSTEM_PRESETS_DIR):
            return

        presets = glob.glob(os.path.join(SYSTEM_PRESETS_DIR, "*.jsonc"))
        for ppath in sorted(presets):
            fname = os.path.basename(ppath)
            name = fname.replace(".jsonc", "").capitalize()

            row = Adw.ActionRow(
                title=name,
                subtitle=f"System preset: {fname}"
            )
            row.set_icon_name("system-run-symbolic")

            load_btn = Gtk.Button(label="Load")
            load_btn.set_valign(Gtk.Align.CENTER)
            load_btn.connect("clicked", self._create_system_handler(ppath, name))
            row.add_suffix(load_btn)

            row.set_activatable(True)
            row.connect("activated", self._create_system_handler(ppath, name))

            group.add(row)

        self.add(group)

    def _create_system_handler(self, ppath: str, name: str):
        def handler(*_):
            try:
                with open(ppath, "r", encoding="utf-8") as f:
                    clean = strip_jsonc(f.read())
                data = json.loads(clean)
                self.config_manager.apply_preset_from_dict(data)
                root = self.get_root()
                if hasattr(root, "show_toast"):
                    root.show_toast(f"Loaded '{name}' system preset!")
            except Exception as e:
                print(f"[FetchCraft] Error loading preset {ppath}: {e}")
                root = self.get_root()
                if hasattr(root, "show_toast"):
                    root.show_toast(f"Failed to parse preset: {e}")
        return handler

    def _build_backup_group(self):
        group = Adw.PreferencesGroup(
            title="Configuration Backup",
            description="FetchCraft automatically creates a backup whenever you apply changes."
        )

        self.backup_row = Adw.ActionRow(
            title="Restore Previous Backup",
            subtitle="Revert ~/.config/fastfetch/config.jsonc to config.jsonc.bak"
        )
        self.backup_row.set_icon_name("document-revert-symbolic")

        restore_btn = Gtk.Button(label="Restore Backup")
        restore_btn.set_valign(Gtk.Align.CENTER)
        restore_btn.connect("clicked", self._on_restore_clicked)
        self.backup_row.add_suffix(restore_btn)

        has_bak = self.config_manager.has_backup()
        restore_btn.set_sensitive(has_bak)

        group.add(self.backup_row)
        self.add(group)

    def _on_restore_clicked(self, _btn):
        if self.config_manager.restore_backup():
            root = self.get_root()
            if hasattr(root, "show_toast"):
                root.show_toast("Restored configuration from backup!")
