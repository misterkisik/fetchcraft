"""
FetchCraft Style View
Allows customization of terminal colors, key-value separators, and palette symbols.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..models import COLOR_NAMES, SEPARATOR_PRESETS, COLOR_SYMBOLS
from ..config_manager import ConfigManager
from ..i18n import tr

class StyleView(Adw.PreferencesPage):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self._updating = False

        self._build_color_group()
        self._build_separator_group()
        self._build_palette_group()

        self.config_manager.add_change_listener(self._sync_from_config)
        self._sync_from_config()

    def _build_color_group(self):
        self.color_group = Adw.PreferencesGroup(
            title=tr("style_colors_group"),
            description=tr("style_colors_desc")
        )

        color_labels = [name for _, name in COLOR_NAMES]
        self._color_keys = [code for code, _ in COLOR_NAMES]

        # Keys Color
        self.keys_combo = Adw.ComboRow(
            title=tr("style_keys_color"),
            subtitle=tr("style_keys_color_sub"),
            model=Gtk.StringList.new(color_labels)
        )
        self.keys_combo.connect("notify::selected", self._on_key_color_changed)
        self.color_group.add(self.keys_combo)

        # Title Color
        self.title_combo = Adw.ComboRow(
            title=tr("style_title_color"),
            subtitle=tr("style_title_color_sub"),
            model=Gtk.StringList.new(color_labels)
        )
        self.title_combo.connect("notify::selected", self._on_title_color_changed)
        self.color_group.add(self.title_combo)

        # Output Color
        self.output_combo = Adw.ComboRow(
            title=tr("style_output_color"),
            subtitle=tr("style_output_color_sub"),
            model=Gtk.StringList.new(color_labels)
        )
        self.output_combo.connect("notify::selected", self._on_output_color_changed)
        self.color_group.add(self.output_combo)

        # Separator Color
        self.sep_color_combo = Adw.ComboRow(
            title=tr("style_sep_color"),
            subtitle=tr("style_sep_color_sub"),
            model=Gtk.StringList.new(color_labels)
        )
        self.sep_color_combo.connect("notify::selected", self._on_sep_color_changed)
        self.color_group.add(self.sep_color_combo)

        self.add(self.color_group)

    def _build_separator_group(self):
        self.sep_group = Adw.PreferencesGroup(
            title=tr("style_sep_group"),
            description=tr("style_sep_desc")
        )

        sep_labels = [name for _, name in SEPARATOR_PRESETS] + ["Custom Delimiter..."]
        self._sep_values = [code for code, _ in SEPARATOR_PRESETS]

        self.sep_combo = Adw.ComboRow(
            title=tr("style_sep_preset"),
            model=Gtk.StringList.new(sep_labels)
        )
        self.sep_combo.connect("notify::selected", self._on_sep_preset_changed)
        self.sep_group.add(self.sep_combo)

        self.custom_sep_entry = Adw.EntryRow(title=tr("style_custom_sep"))
        self.custom_sep_entry.connect("changed", self._on_custom_sep_changed)
        self.sep_group.add(self.custom_sep_entry)

        self.add(self.sep_group)

    def _build_palette_group(self):
        self.palette_group = Adw.PreferencesGroup(
            title=tr("style_palette_group"),
            description=tr("style_palette_desc")
        )

        symbol_labels = [name for _, name in COLOR_SYMBOLS]
        self._symbol_values = [code for code, _ in COLOR_SYMBOLS]

        self.symbol_combo = Adw.ComboRow(
            title=tr("style_palette_symbol"),
            model=Gtk.StringList.new(symbol_labels)
        )
        self.symbol_combo.connect("notify::selected", self._on_symbol_changed)
        self.palette_group.add(self.symbol_combo)

        self.add(self.palette_group)

    def retranslate(self):
        self.color_group.set_title(tr("style_colors_group"))
        self.color_group.set_description(tr("style_colors_desc"))
        self.keys_combo.set_title(tr("style_keys_color"))
        self.keys_combo.set_subtitle(tr("style_keys_color_sub"))
        self.title_combo.set_title(tr("style_title_color"))
        self.title_combo.set_subtitle(tr("style_title_color_sub"))
        self.output_combo.set_title(tr("style_output_color"))
        self.output_combo.set_subtitle(tr("style_output_color_sub"))
        self.sep_color_combo.set_title(tr("style_sep_color"))
        self.sep_color_combo.set_subtitle(tr("style_sep_color_sub"))

        self.sep_group.set_title(tr("style_sep_group"))
        self.sep_group.set_description(tr("style_sep_desc"))
        self.sep_combo.set_title(tr("style_sep_preset"))
        self.custom_sep_entry.set_title(tr("style_custom_sep"))

        self.palette_group.set_title(tr("style_palette_group"))
        self.palette_group.set_description(tr("style_palette_desc"))
        self.symbol_combo.set_title(tr("style_palette_symbol"))

    def _sync_from_config(self):
        if self._updating:
            return
        self._updating = True

        # Colors
        curr_keys_color = self.config_manager.get_color("keys")
        if curr_keys_color in self._color_keys:
            self.keys_combo.set_selected(self._color_keys.index(curr_keys_color))
        else:
            self.keys_combo.set_selected(0)

        curr_title_color = self.config_manager.get_color("title")
        if curr_title_color in self._color_keys:
            self.title_combo.set_selected(self._color_keys.index(curr_title_color))
        else:
            self.title_combo.set_selected(0)

        curr_output_color = self.config_manager.get_color("output")
        if curr_output_color in self._color_keys:
            self.output_combo.set_selected(self._color_keys.index(curr_output_color))
        else:
            self.output_combo.set_selected(0)

        curr_sep_color = self.config_manager.get_color("separator")
        if curr_sep_color in self._color_keys:
            self.sep_color_combo.set_selected(self._color_keys.index(curr_sep_color))
        else:
            self.sep_color_combo.set_selected(0)

        # Separator
        curr_sep = self.config_manager.get_separator()
        if curr_sep in self._sep_values:
            idx = self._sep_values.index(curr_sep)
            self.sep_combo.set_selected(idx)
            self.custom_sep_entry.set_visible(False)
        else:
            # Custom
            self.sep_combo.set_selected(len(self._sep_values))
            self.custom_sep_entry.set_text(curr_sep)
            self.custom_sep_entry.set_visible(True)

        # Palette symbol
        curr_symbol = "block"
        for mod in self.config_manager.get_modules():
            if isinstance(mod, dict) and mod.get("type") == "colors":
                curr_symbol = mod.get("symbol", "block")
                break
        if curr_symbol in self._symbol_values:
            self.symbol_combo.set_selected(self._symbol_values.index(curr_symbol))

        self._updating = False

    def _on_key_color_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if 0 <= idx < len(self._color_keys):
            self.config_manager.set_color("keys", self._color_keys[idx])

    def _on_title_color_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if 0 <= idx < len(self._color_keys):
            self.config_manager.set_color("title", self._color_keys[idx])

    def _on_output_color_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if 0 <= idx < len(self._color_keys):
            self.config_manager.set_color("output", self._color_keys[idx])

    def _on_sep_color_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if 0 <= idx < len(self._color_keys):
            self.config_manager.set_color("separator", self._color_keys[idx])

    def _on_sep_preset_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if idx < len(self._sep_values):
            self.custom_sep_entry.set_visible(False)
            self.config_manager.set_separator(self._sep_values[idx])
        else:
            self.custom_sep_entry.set_visible(True)

    def _on_custom_sep_changed(self, entry):
        if self._updating or not entry.get_visible():
            return
        self.config_manager.set_separator(entry.get_text())

    def _on_symbol_changed(self, combo, _param):
        if self._updating:
            return
        idx = combo.get_selected()
        if 0 <= idx < len(self._symbol_values):
            sym = self._symbol_values[idx]
            modules = list(self.config_manager.get_modules())
            updated = False
            for i, m in enumerate(modules):
                if m == "colors":
                    modules[i] = {"type": "colors", "symbol": sym}
                    updated = True
                    break
                elif isinstance(m, dict) and m.get("type") == "colors":
                    m["symbol"] = sym
                    updated = True
                    break
            if updated:
                self.config_manager.set_modules(modules)
