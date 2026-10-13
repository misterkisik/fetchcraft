"""
FetchCraft First Run Language Selection Dialog
Modeled after CleanArch initial setup.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from typing import Callable, Optional
from ..i18n import SUPPORTED_LANGUAGES, tr, set_language, get_current_language

LANG_INFO = [
    ("ru", "🇷🇺  Русский", "Русский интерфейс программы"),
    ("en", "🇬🇧  English", "English user interface"),
    ("es", "🇪🇸  Español", "Interfaz en español"),
    ("fr", "🇫🇷  Français", "Interface en français"),
]

class FirstRunLanguageDialog(Adw.Window):
    def __init__(self, parent_window: Gtk.Window, on_completed: Optional[Callable[[str], None]] = None):
        super().__init__(transient_for=parent_window, modal=True)
        self.on_completed = on_completed
        self.set_title("FetchCraft")
        self.set_default_size(440, 520)
        self.set_resizable(False)
        self.set_destroy_with_parent(True)

        self.selected_lang = get_current_language()
        if self.selected_lang not in SUPPORTED_LANGUAGES:
            self.selected_lang = "ru"

        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        # HeaderBar without extra close buttons
        header_bar = Adw.HeaderBar()
        header_bar.set_show_start_title_buttons(False)
        header_bar.set_show_end_title_buttons(False)
        toolbar_view.add_top_bar(header_bar)

        # Scrolled content
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content.set_margin_start(24)
        content.set_margin_end(24)
        content.set_margin_top(20)
        content.set_margin_bottom(24)

        # App / Locale icon
        icon = Gtk.Image.new_from_icon_name("preferences-desktop-locale-symbolic")
        icon.set_pixel_size(56)
        icon.add_css_class("accent")
        content.append(icon)

        # Title
        self.title_label = Gtk.Label(label=tr("welcome_title"))
        self.title_label.add_css_class("title-2")
        self.title_label.set_wrap(True)
        self.title_label.set_justify(Gtk.Justification.CENTER)
        content.append(self.title_label)

        # Subtitle
        self.desc_label = Gtk.Label(label=tr("welcome_subtitle"))
        self.desc_label.add_css_class("body")
        self.desc_label.add_css_class("dim-label")
        self.desc_label.set_wrap(True)
        self.desc_label.set_justify(Gtk.Justification.CENTER)
        content.append(self.desc_label)

        # Language selection group
        group = Adw.PreferencesGroup()
        self.radio_buttons = {}
        first_radio = None

        for code, name, desc in LANG_INFO:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(desc)

            radio = Gtk.CheckButton()
            if first_radio is None:
                first_radio = radio
            else:
                radio.set_group(first_radio)

            if code == self.selected_lang:
                radio.set_active(True)

            radio.connect("toggled", self._on_radio_toggled, code)
            row.add_prefix(radio)
            row.set_activatable_widget(radio)
            self.radio_buttons[code] = radio
            group.add(row)

        content.append(group)

        # Continue button
        self.btn_continue = Gtk.Button(label=tr("welcome_continue"))
        self.btn_continue.add_css_class("suggested-action")
        self.btn_continue.add_css_class("pill")
        self.btn_continue.set_size_request(200, 48)
        self.btn_continue.set_halign(Gtk.Align.CENTER)
        self.btn_continue.set_margin_top(8)
        self.btn_continue.connect("clicked", self._on_continue_clicked)
        content.append(self.btn_continue)

        scroll.set_child(content)
        toolbar_view.set_content(scroll)

    def _on_radio_toggled(self, button, code: str):
        if button.get_active():
            self.selected_lang = code
            set_language(code, first_run_done=False)
            self._update_ui_strings()

    def _update_ui_strings(self):
        self.title_label.set_label(tr("welcome_title"))
        self.desc_label.set_label(tr("welcome_subtitle"))
        self.btn_continue.set_label(tr("welcome_continue"))

    def _on_continue_clicked(self, _button):
        set_language(self.selected_lang, first_run_done=True)
        if self.on_completed:
            self.on_completed(self.selected_lang)
        self.close()
