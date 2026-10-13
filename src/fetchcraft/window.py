"""
FetchCraft Main Application Window
Modern Libadwaita interface with live split-view terminal and fastfetch customization tabs.
Includes multi-language support (i18n), first-run language selection, and full copyrights.
"""

import os
import shutil
import subprocess
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GLib

from .config_manager import ConfigManager, FASTFETCH_CONFIG_PATH
from .preview_panel import PreviewPanel
from .views.modules_view import ModulesView
from .views.style_view import StyleView
from .views.logo_view import LogoView
from .views.presets_view import PresetsView
from .views.language_dialog import FirstRunLanguageDialog
from .i18n import (
    tr,
    is_first_run,
    set_language,
    get_current_language,
    SUPPORTED_LANGUAGES,
    add_language_change_listener
)

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app: Adw.Application):
        super().__init__(application=app)
        self.set_title(tr("app_title"))
        self.set_default_size(1180, 760)

        self.config_manager = ConfigManager()

        # Toast overlay
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        # Root box
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(root_box)

        # Build HeaderBar
        self._build_header(root_box)

        # Build Main Body (Split View)
        self._build_body(root_box)

        # Retranslate on i18n change
        add_language_change_listener(self.retranslate)

        # Check for first run language prompt
        GLib.idle_add(self._check_first_run)

    def _build_header(self, root_box: Gtk.Box):
        self.header = Adw.HeaderBar()

        # ViewSwitcher for Center
        self.stack = Adw.ViewStack()
        self.switcher = Adw.ViewSwitcher(stack=self.stack)
        self.switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        self.header.set_title_widget(self.switcher)

        # Terminal Run Button (Left)
        self.run_btn = Gtk.Button.new_from_icon_name("utilities-terminal-symbolic")
        self.run_btn.set_tooltip_text(tr("btn_terminal_tooltip"))
        self.run_btn.connect("clicked", self._on_run_in_terminal)
        self.header.pack_start(self.run_btn)

        # Apply Button (Right)
        self.apply_btn = Gtk.Button(label=tr("btn_apply"))
        self.apply_btn.set_icon_name("emblem-ok-symbolic")
        self.apply_btn.add_css_class("suggested-action")
        self.apply_btn.set_tooltip_text(tr("btn_apply_tooltip"))
        self.apply_btn.connect("clicked", self._on_apply_clicked)
        self.header.pack_end(self.apply_btn)

        # Menu Button (Right)
        self.menu_btn = Gtk.MenuButton()
        self.menu_btn.set_icon_name("open-menu-symbolic")
        self.menu_btn.set_tooltip_text(tr("menu_options_tooltip"))
        self.header.pack_end(self.menu_btn)

        self._setup_window_actions()
        self._build_menu()

        root_box.append(self.header)

    def _setup_window_actions(self):
        # Action: Copy config
        copy_action = Gio.SimpleAction.new("copy_config", None)
        copy_action.connect("activate", self._on_copy_config)
        self.add_action(copy_action)

        # Action: Export config
        export_action = Gio.SimpleAction.new("export_config", None)
        export_action.connect("activate", self._on_export_config)
        self.add_action(export_action)

        # Action: Reload config
        reload_action = Gio.SimpleAction.new("reload_config", None)
        reload_action.connect("activate", lambda *_: self._on_reload_config())
        self.add_action(reload_action)

        # Action: Set language
        set_lang_action = Gio.SimpleAction.new("set_lang", GLib.VariantType.new("s"))
        set_lang_action.connect("activate", self._on_set_lang)
        self.add_action(set_lang_action)

        # Action: About
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_show_about)
        self.add_action(about_action)

    def _build_menu(self):
        menu = Gio.Menu()

        # Language Submenu
        lang_menu = Gio.Menu()
        lang_items = [
            ("ru", "🇷🇺 Русский"),
            ("en", "🇬🇧 English"),
            ("es", "🇪🇸 Español"),
            ("fr", "🇫🇷 Français"),
        ]
        curr = get_current_language()
        for code, name in lang_items:
            prefix = "✓ " if code == curr else "    "
            item = Gio.MenuItem.new(f"{prefix}{name}", None)
            item.set_action_and_target_value("win.set_lang", GLib.Variant.new_string(code))
            lang_menu.append_item(item)

        menu.append_submenu(tr("menu_language"), lang_menu)
        menu.append(tr("menu_copy_config"), "win.copy_config")
        menu.append(tr("menu_export"), "win.export_config")
        menu.append(tr("menu_reload"), "win.reload_config")
        menu.append(tr("menu_about"), "win.about")

        self.menu_btn.set_menu_model(menu)

    def _on_set_lang(self, _action, param):
        lang = param.get_string()
        if lang in SUPPORTED_LANGUAGES:
            set_language(lang)
            self.retranslate()
            self.show_toast(tr("toast_lang_changed"))

    def _check_first_run(self):
        if is_first_run():
            dlg = FirstRunLanguageDialog(self, on_completed=self._on_first_run_completed)
            dlg.present()
        return False

    def _on_first_run_completed(self, _lang: str):
        self.retranslate()
        self.show_toast(tr("toast_lang_changed"))

    def _build_body(self, root_box: Gtk.Box):
        # Split Paned: Left = Settings Stack, Right = Terminal Live Preview
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_hexpand(True)
        paned.set_vexpand(True)
        paned.set_position(580)

        # Left: Settings Views
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_box.set_hexpand(True)
        left_box.set_vexpand(True)

        # 1. Modules
        self.modules_view = ModulesView(self.config_manager)
        self.page_modules = self.stack.add_titled_with_icon(
            self.modules_view, "modules", tr("tab_modules"), "view-list-symbolic"
        )

        # 2. Style
        self.style_view = StyleView(self.config_manager)
        self.page_style = self.stack.add_titled_with_icon(
            self.style_view, "style", tr("tab_style"), "color-select-symbolic"
        )

        # 3. Logo
        self.logo_view = LogoView(self.config_manager)
        self.page_logo = self.stack.add_titled_with_icon(
            self.logo_view, "logo", tr("tab_logo"), "image-x-generic-symbolic"
        )

        # 4. Presets
        self.presets_view = PresetsView(self.config_manager)
        self.page_presets = self.stack.add_titled_with_icon(
            self.presets_view, "presets", tr("tab_presets"), "emblem-favorite-symbolic"
        )

        left_box.append(self.stack)
        paned.set_start_child(left_box)

        # Right: Live Terminal Preview
        self.preview_panel = PreviewPanel(self.config_manager)
        paned.set_end_child(self.preview_panel)

        root_box.append(paned)

    def retranslate(self):
        """Dynamically retranslates all window widgets and subviews."""
        self.set_title(tr("app_title"))
        self.apply_btn.set_label(tr("btn_apply"))
        self.apply_btn.set_tooltip_text(tr("btn_apply_tooltip"))
        self.run_btn.set_tooltip_text(tr("btn_terminal_tooltip"))
        self.menu_btn.set_tooltip_text(tr("menu_options_tooltip"))

        if hasattr(self, "page_modules"):
            self.page_modules.set_title(tr("tab_modules"))
        if hasattr(self, "page_style"):
            self.page_style.set_title(tr("tab_style"))
        if hasattr(self, "page_logo"):
            self.page_logo.set_title(tr("tab_logo"))
        if hasattr(self, "page_presets"):
            self.page_presets.set_title(tr("tab_presets"))

        if hasattr(self.modules_view, "retranslate"):
            self.modules_view.retranslate()
        if hasattr(self.style_view, "retranslate"):
            self.style_view.retranslate()
        if hasattr(self.logo_view, "retranslate"):
            self.logo_view.retranslate()
        if hasattr(self.presets_view, "retranslate"):
            self.presets_view.retranslate()
        if hasattr(self.preview_panel, "retranslate"):
            self.preview_panel.retranslate()

        self._build_menu()

    def show_toast(self, text: str):
        toast = Adw.Toast.new(text)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)

    def _on_apply_clicked(self, _btn):
        path = self.config_manager.save_to_system()
        self.show_toast(tr("toast_config_applied", path=path))

    def _on_copy_config(self, _action, _param):
        json_str = self.config_manager.to_jsonc_string()
        clipboard = self.get_display().get_clipboard()
        clipboard.set(json_str)
        self.show_toast(tr("toast_copied_config"))

    def _on_export_config(self, _action, _param):
        dialog = Gtk.FileDialog()
        dialog.set_title(tr("menu_export"))
        dialog.set_initial_name("config.jsonc")

        def on_save_finish(_dialog, result):
            try:
                gfile = dialog.save_finish(result)
                if gfile:
                    dest = gfile.get_path()
                    self.config_manager.export_to_file(dest)
                    self.show_toast(tr("toast_exported", name=os.path.basename(dest)))
            except Exception as e:
                print(f"[FetchCraft] Export cancelled or failed: {e}")

        dialog.save(self, None, on_save_finish)

    def _on_reload_config(self):
        self.config_manager.load()
        self.show_toast(tr("toast_reloaded"))

    def _on_run_in_terminal(self, _btn):
        tmp_config = self.config_manager.write_temp_preview()
        cmd = f"fastfetch -c {tmp_config}; read -p 'Press Enter to close...'"

        terminals = [
            ["kgx", "-e", "bash", "-c", cmd],
            ["ptyxis", "--", "bash", "-c", cmd],
            ["gnome-terminal", "--", "bash", "-c", cmd],
            ["alacritty", "-e", "bash", "-c", cmd],
            ["kitty", "bash", "-c", cmd],
            ["xterm", "-e", f"bash -c \"{cmd}\""],
        ]

        launched = False
        for t in terminals:
            if shutil.which(t[0]):
                try:
                    subprocess.Popen(t)
                    launched = True
                    break
                except Exception:
                    continue

        if launched:
            self.show_toast(tr("toast_terminal_spawned"))
        else:
            self.show_toast(tr("toast_terminal_not_found"))

    def _on_show_about(self, _action, _param):
        if hasattr(Adw, "AboutDialog"):
            about = Adw.AboutDialog()
            about.set_application_name("FetchCraft")
            about.set_application_icon("org.cleanarch.FetchCraft")
            about.set_developer_name("MisterKisik")
            about.set_version("1.0.0")
            about.set_comments(tr("about_comments"))
            about.set_website("https://github.com/misterkisik/fetchcraft")
            about.set_issue_url("https://github.com/misterkisik/fetchcraft/issues")
            about.set_copyright("© 2026 MisterKisik")
            about.set_license_type(Gtk.License.GPL_3_0)
            about.present(self)
        else:
            about = Adw.AboutWindow(transient_for=self)
            about.set_application_name("FetchCraft")
            about.set_application_icon("org.cleanarch.FetchCraft")
            about.set_developer_name("MisterKisik")
            about.set_version("1.0.0")
            about.set_comments(tr("about_comments"))
            about.set_website("https://github.com/misterkisik/fetchcraft")
            about.set_issue_url("https://github.com/misterkisik/fetchcraft/issues")
            about.set_copyright("© 2026 MisterKisik")
            about.set_license_type(Gtk.License.GPL_3_0)
            about.present()
