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
from ..i18n import tr

SYSTEM_PRESETS_DIR = "/usr/share/fastfetch/presets"

class PresetsView(Adw.PreferencesPage):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager

        self._curated_buttons = []
        self._system_buttons = []

        self._build_curated_group()
        self._build_system_group()
        self._build_backup_group()

    def _build_curated_group(self):
        self.curated_group = Adw.PreferencesGroup(
            title=tr("presets_curated_group"),
            description=tr("presets_curated_desc")
        )

        for key, preset in BUILTIN_PRESETS.items():
            row = Adw.ActionRow(
                title=preset["name"],
                subtitle=preset["desc"]
            )
            row.set_icon_name(preset.get("icon", "emblem-favorite-symbolic"))

            apply_btn = Gtk.Button(label=tr("presets_load_btn"))
            apply_btn.add_css_class("suggested-action")
            apply_btn.set_valign(Gtk.Align.CENTER)
            apply_btn.connect("clicked", self._create_curated_handler(key, preset["name"]))
            row.add_suffix(apply_btn)
            self._curated_buttons.append(apply_btn)

            row.set_activatable(True)
            row.connect("activated", self._create_curated_handler(key, preset["name"]))

            self.curated_group.add(row)

        self.add(self.curated_group)

    def _create_curated_handler(self, key: str, name: str):
        def handler(*_):
            self.config_manager.apply_preset(key)
            root = self.get_root()
            if hasattr(root, "show_toast"):
                root.show_toast(f"Loaded '{name}' preset!")
        return handler

    def _build_system_group(self):
        self.system_group = Adw.PreferencesGroup(
            title=tr("presets_system_group"),
            description=tr("presets_system_desc")
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

            load_btn = Gtk.Button(label=tr("presets_load_btn"))
            load_btn.set_valign(Gtk.Align.CENTER)
            load_btn.connect("clicked", self._create_system_handler(ppath, name))
            row.add_suffix(load_btn)
            self._system_buttons.append(load_btn)

            row.set_activatable(True)
            row.connect("activated", self._create_system_handler(ppath, name))

            self.system_group.add(row)

        self.add(self.system_group)

    def _create_system_handler(self, ppath: str, name: str):
        def handler(*_):
            try:
                with open(ppath, "r", encoding="utf-8") as f:
                    clean = strip_jsonc(f.read())
                data = json.loads(clean)
                self.config_manager.apply_preset_from_dict(data)
                root = self.get_root()
                if hasattr(root, "show_toast"):
                    root.show_toast(tr("toast_preset_loaded", name=name))
            except Exception as e:
                print(f"[FetchCraft] Error loading preset {ppath}: {e}")
                root = self.get_root()
                if hasattr(root, "show_toast"):
                    root.show_toast(f"Failed to parse preset: {e}")
        return handler

    def _build_backup_group(self):
        self.backup_group = Adw.PreferencesGroup(
            title=tr("presets_backup_group"),
            description=tr("presets_backup_desc")
        )

        self.backup_row = Adw.ActionRow(
            title=tr("presets_restore_row"),
            subtitle=tr("presets_restore_sub")
        )
        self.backup_row.set_icon_name("document-revert-symbolic")

        self.restore_btn = Gtk.Button(label=tr("presets_restore_btn"))
        self.restore_btn.set_valign(Gtk.Align.CENTER)
        self.restore_btn.connect("clicked", self._on_restore_clicked)
        self.backup_row.add_suffix(self.restore_btn)

        has_bak = self.config_manager.has_backup()
        self.restore_btn.set_sensitive(has_bak)

        self.backup_group.add(self.backup_row)
        self.add(self.backup_group)

    def retranslate(self):
        self.curated_group.set_title(tr("presets_curated_group"))
        self.curated_group.set_description(tr("presets_curated_desc"))
        for btn in self._curated_buttons:
            btn.set_label(tr("presets_load_btn"))

        if hasattr(self, "system_group"):
            self.system_group.set_title(tr("presets_system_group"))
            self.system_group.set_description(tr("presets_system_desc"))
            for btn in self._system_buttons:
                btn.set_label(tr("presets_load_btn"))

        self.backup_group.set_title(tr("presets_backup_group"))
        self.backup_group.set_description(tr("presets_backup_desc"))
        self.backup_row.set_title(tr("presets_restore_row"))
        self.backup_row.set_subtitle(tr("presets_restore_sub"))
        self.restore_btn.set_label(tr("presets_restore_btn"))

    def _on_restore_clicked(self, _btn):
        if self.config_manager.restore_backup():
            root = self.get_root()
            if hasattr(root, "show_toast"):
                root.show_toast(tr("toast_backup_restored"))
