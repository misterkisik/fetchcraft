"""
FetchCraft Modules View
Manage enabled Fastfetch modules, customize order, keys, and formats.
"""

from typing import Any, Dict, List, Optional
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

from ..models import MODULE_REGISTRY, ModuleDefinition
from ..config_manager import ConfigManager
from ..i18n import tr

class ModuleAddDialog(Adw.Window):
    def __init__(self, parent: Gtk.Window, on_select_callback):
        super().__init__(transient_for=parent, modal=True)
        self.set_title(tr("modules_dialog_title"))
        self.set_default_size(520, 600)
        self.on_select_callback = on_select_callback

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        header = Adw.HeaderBar()
        content.append(header)

        # Search bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(tr("modules_search_placeholder"))
        self.search_entry.set_margin_start(16)
        self.search_entry.set_margin_end(16)
        self.search_entry.set_margin_top(8)
        self.search_entry.set_margin_bottom(8)
        self.search_entry.connect("search-changed", self._on_search_changed)
        content.append(self.search_entry)

        # Scrolled preferences page
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        self.pref_page = Adw.PreferencesPage()
        self._groups: List[Adw.PreferencesGroup] = []
        scrolled.set_child(self.pref_page)
        content.append(scrolled)

        self.set_content(content)
        self._populate_modules()

    def _populate_modules(self, filter_text: str = ""):
        # Group by category
        categories: Dict[str, List[ModuleDefinition]] = {}
        filter_lower = filter_text.strip().lower()

        for mod in MODULE_REGISTRY:
            if filter_lower:
                if filter_lower not in mod.name.lower() and filter_lower not in mod.id.lower() and filter_lower not in mod.description.lower():
                    continue
            categories.setdefault(mod.category, []).append(mod)

        # Clear old groups cleanly
        for g in self._groups:
            self.pref_page.remove(g)
        self._groups.clear()

        for cat_name, mods in categories.items():
            group = Adw.PreferencesGroup(title=cat_name)
            for mod in mods:
                row = Adw.ActionRow(
                    title=mod.name,
                    subtitle=f"{mod.description} ({mod.id})"
                )
                row.set_icon_name(mod.icon)

                add_btn = Gtk.Button.new_from_icon_name("list-add-symbolic")
                add_btn.add_css_class("suggested-action")
                add_btn.set_valign(Gtk.Align.CENTER)
                add_btn.set_tooltip_text(f"Add {mod.name}")
                add_btn.connect("clicked", self._create_add_handler(mod.id))
                row.add_suffix(add_btn)

                # Clicking row also adds
                row.set_activatable(True)
                row.connect("activated", self._create_add_handler(mod.id))

                group.add(row)
            self.pref_page.add(group)
            self._groups.append(group)

    def _create_add_handler(self, mod_id: str):
        def handler(*_):
            self.on_select_callback(mod_id)
            self.close()
        return handler

    def _on_search_changed(self, entry):
        self._populate_modules(entry.get_text())


class ModuleEditDialog(Adw.Window):
    def __init__(self, parent: Gtk.Window, mod_item: Any, index: int, on_save_callback):
        super().__init__(transient_for=parent, modal=True)
        self.set_title(tr("modules_edit_dialog_title"))
        self.set_default_size(460, 360)
        self.mod_item = mod_item
        self.index = index
        self.on_save_callback = on_save_callback

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        header = Adw.HeaderBar()
        content.append(header)

        page = Adw.PreferencesPage()
        group = Adw.PreferencesGroup(title=tr("modules_edit_dialog_title"))

        # Determine type
        if isinstance(mod_item, str):
            self.mod_type = mod_item
            current_key = ""
            current_format = ""
        else:
            self.mod_type = mod_item.get("type", "")
            current_key = mod_item.get("key", "")
            current_format = mod_item.get("format", "")

        # Type row (read only)
        type_row = Adw.ActionRow(title=tr("modules_edit_type"), subtitle=self.mod_type)
        group.add(type_row)

        # Custom Key / Label
        self.key_entry = Adw.EntryRow(title=tr("modules_edit_key"))
        self.key_entry.set_text(current_key)
        group.add(self.key_entry)

        # Format string
        self.format_entry = Adw.EntryRow(title=tr("modules_edit_format"))
        self.format_entry.set_text(current_format)
        group.add(self.format_entry)

        # Action buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_margin_top(18)
        btn_box.set_halign(Gtk.Align.END)

        cancel_btn = Gtk.Button(label=tr("btn_cancel"))
        cancel_btn.connect("clicked", lambda _: self.close())
        btn_box.append(cancel_btn)

        save_btn = Gtk.Button(label=tr("btn_save"))
        save_btn.add_css_class("suggested-action")
        save_btn.connect("clicked", self._on_save)
        btn_box.append(save_btn)

        page.add(group)
        content.append(page)
        content.append(btn_box)
        self.set_content(content)

    def _on_save(self, _btn):
        key = self.key_entry.get_text().strip()
        fmt = self.format_entry.get_text().strip()

        if not key and not fmt:
            new_item = self.mod_type
        else:
            if isinstance(self.mod_item, dict):
                new_item = dict(self.mod_item)
            else:
                new_item = {"type": self.mod_type}
            if key:
                new_item["key"] = key
            else:
                new_item.pop("key", None)
            if fmt:
                new_item["format"] = fmt
            else:
                new_item.pop("format", None)

        self.on_save_callback(self.index, new_item)
        self.close()


class ModulesView(Adw.PreferencesPage):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self._updating = False

        self.group = Adw.PreferencesGroup()
        self.group.set_title(tr("modules_group_title"))
        self.group.set_description(tr("modules_group_desc"))

        # Top bar with Add button
        self.add_btn = Gtk.Button.new_from_icon_name("list-add-symbolic")
        self.add_btn.set_label(tr("modules_add_btn"))
        self.add_btn.add_css_class("suggested-action")
        self.add_btn.connect("clicked", self._on_add_clicked)
        self.group.set_header_suffix(self.add_btn)

        self._rows: List[Adw.ActionRow] = []
        self.add(self.group)
        self._registry_map = {m.id.lower(): m for m in MODULE_REGISTRY}

        self.config_manager.add_change_listener(self._refresh_rows)
        self._refresh_rows()

    def retranslate(self):
        self.group.set_title(tr("modules_group_title"))
        self.group.set_description(tr("modules_group_desc"))
        self.add_btn.set_label(tr("modules_add_btn"))
        self._refresh_rows()

    def _on_add_clicked(self, _btn):
        root = self.get_root()
        dialog = ModuleAddDialog(root, self._on_module_added)
        dialog.present()

    def _on_module_added(self, mod_id: str):
        self.config_manager.add_module(mod_id)

    def _refresh_rows(self):
        if self._updating:
            return
        self._updating = True

        # Remove existing rows cleanly
        for r in self._rows:
            self.group.remove(r)
        self._rows.clear()

        modules = self.config_manager.get_modules()
        for idx, mod in enumerate(modules):
            row = self._create_row_for_module(idx, mod, len(modules))
            self.group.add(row)
            self._rows.append(row)

        self._updating = False

    def _create_row_for_module(self, idx: int, mod_item: Any, total: int) -> Adw.ActionRow:
        if isinstance(mod_item, str):
            mod_id = mod_item
            subtitle = mod_item
            has_custom_config = False
        elif isinstance(mod_item, dict):
            mod_id = mod_item.get("type", "custom")
            parts = []
            if "key" in mod_item:
                parts.append(f"Key: {mod_item['key']}")
            if "format" in mod_item:
                parts.append(f"Format: {mod_item['format']}")
            if "symbol" in mod_item:
                parts.append(f"Symbol: {mod_item['symbol']}")
            subtitle = " | ".join(parts) if parts else mod_id
            has_custom_config = True
        else:
            mod_id = str(mod_item)
            subtitle = mod_id
            has_custom_config = False

        mod_def = self._registry_map.get(mod_id.lower())
        title = mod_def.name if mod_def else mod_id.capitalize()
        icon_name = mod_def.icon if mod_def else "application-x-executable-symbolic"

        safe_title = GLib.markup_escape_text(f"{idx + 1}. {title}")
        safe_subtitle = GLib.markup_escape_text(subtitle) if subtitle else ""
        row = Adw.ActionRow(title=safe_title, subtitle=safe_subtitle)
        row.set_icon_name(icon_name)

        # Move Up button
        up_btn = Gtk.Button.new_from_icon_name("go-up-symbolic")
        up_btn.set_valign(Gtk.Align.CENTER)
        up_btn.set_tooltip_text(tr("modules_move_up"))
        up_btn.set_sensitive(idx > 0)
        up_btn.connect("clicked", lambda _, i=idx: self.config_manager.move_module_up(i))
        row.add_suffix(up_btn)

        # Move Down button
        down_btn = Gtk.Button.new_from_icon_name("go-down-symbolic")
        down_btn.set_valign(Gtk.Align.CENTER)
        down_btn.set_tooltip_text(tr("modules_move_down"))
        down_btn.set_sensitive(idx < total - 1)
        down_btn.connect("clicked", lambda _, i=idx: self.config_manager.move_module_down(i))
        row.add_suffix(down_btn)

        # Configure button (if supports settings)
        if mod_id not in ("break", "separator"):
            edit_btn = Gtk.Button.new_from_icon_name("document-edit-symbolic")
            edit_btn.set_valign(Gtk.Align.CENTER)
            edit_btn.set_tooltip_text(tr("modules_edit_tip"))
            edit_btn.connect("clicked", lambda _, i=idx, item=mod_item: self._on_edit_module(i, item))
            row.add_suffix(edit_btn)

        # Delete button
        del_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic")
        del_btn.set_valign(Gtk.Align.CENTER)
        del_btn.add_css_class("destructive-action")
        del_btn.set_tooltip_text(tr("modules_remove_tip"))
        del_btn.connect("clicked", lambda _, i=idx: self.config_manager.remove_module(i))
        row.add_suffix(del_btn)

        return row

    def _on_edit_module(self, idx: int, mod_item: Any):
        root = self.get_root()
        dialog = ModuleEditDialog(root, mod_item, idx, self._on_module_updated)
        dialog.present()

    def _on_module_updated(self, idx: int, new_item: Any):
        self.config_manager.update_module(idx, new_item)
