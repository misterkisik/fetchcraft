"""
FetchCraft Main Application Window
Modern Libadwaita interface with live split-view terminal and fastfetch customization tabs.
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

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app: Adw.Application):
        super().__init__(application=app)
        self.set_title("FetchCraft")
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

    def _build_header(self, root_box: Gtk.Box):
        header = Adw.HeaderBar()

        # ViewSwitcher for Center
        self.stack = Adw.ViewStack()
        switcher = Adw.ViewSwitcher(stack=self.stack)
        switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        header.set_title_widget(switcher)

        # Terminal Run Button (Left)
        run_btn = Gtk.Button.new_from_icon_name("utilities-terminal-symbolic")
        run_btn.set_tooltip_text("Test Fastfetch in External Terminal")
        run_btn.connect("clicked", self._on_run_in_terminal)
        header.pack_start(run_btn)

        # Apply Button (Right)
        apply_btn = Gtk.Button(label="Apply")
        apply_btn.set_icon_name("emblem-ok-symbolic")
        apply_btn.add_css_class("suggested-action")
        apply_btn.set_tooltip_text("Save and apply to ~/.config/fastfetch/config.jsonc")
        apply_btn.connect("clicked", self._on_apply_clicked)
        header.pack_end(apply_btn)

        # Menu Button (Right)
        menu_btn = Gtk.MenuButton()
        menu_btn.set_icon_name("open-menu-symbolic")
        menu_btn.set_tooltip_text("Options")

        menu = Gio.Menu()
        menu.append("Copy config.jsonc", "win.copy_config")
        menu.append("Export to File…", "win.export_config")
        menu.append("Reload from Disk", "win.reload_config")
        menu.append("About FetchCraft", "win.about")
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)

        self._setup_window_actions()

        root_box.append(header)

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

        # Action: About
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_show_about)
        self.add_action(about_action)

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
        page1 = self.stack.add_titled_with_icon(self.modules_view, "modules", "Modules", "view-list-symbolic")

        # 2. Style
        self.style_view = StyleView(self.config_manager)
        page2 = self.stack.add_titled_with_icon(self.style_view, "style", "Style", "color-select-symbolic")

        # 3. Logo
        self.logo_view = LogoView(self.config_manager)
        page3 = self.stack.add_titled_with_icon(self.logo_view, "logo", "Logo", "image-x-generic-symbolic")

        # 4. Presets
        self.presets_view = PresetsView(self.config_manager)
        page4 = self.stack.add_titled_with_icon(self.presets_view, "presets", "Presets", "emblem-favorite-symbolic")

        left_box.append(self.stack)
        paned.set_start_child(left_box)

        # Right: Live Terminal Preview
        self.preview_panel = PreviewPanel(self.config_manager)
        paned.set_end_child(self.preview_panel)

        root_box.append(paned)

    def show_toast(self, text: str):
        toast = Adw.Toast.new(text)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)

    def _on_apply_clicked(self, _btn):
        path = self.config_manager.save_to_system()
        self.show_toast(f"Configuration applied to {path} 🚀")

    def _on_copy_config(self, _action, _param):
        json_str = self.config_manager.to_jsonc_string()
        clipboard = self.get_display().get_clipboard()
        clipboard.set(json_str)
        self.show_toast("Configuration copied to clipboard!")

    def _on_export_config(self, _action, _param):
        dialog = Gtk.FileDialog()
        dialog.set_title("Export Fastfetch Configuration")
        dialog.set_initial_name("config.jsonc")

        def on_save_finish(_dialog, result):
            try:
                gfile = dialog.save_finish(result)
                if gfile:
                    dest = gfile.get_path()
                    self.config_manager.export_to_file(dest)
                    self.show_toast(f"Exported to {os.path.basename(dest)}!")
            except Exception as e:
                print(f"[FetchCraft] Export cancelled or failed: {e}")

        dialog.save(self, None, on_save_finish)

    def _on_reload_config(self):
        self.config_manager.load()
        self.show_toast("Reloaded configuration from disk.")

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
            self.show_toast("Spawned Fastfetch terminal test window!")
        else:
            self.show_toast("No external terminal emulator found.")

    def _on_show_about(self, _action, _param):
        about = Adw.AboutDialog()
        about.set_application_name("FetchCraft")
        about.set_application_icon("org.cleanarch.FetchCraft")
        about.set_developer_name("misterkisik")
        about.set_version("1.0.0")
        about.set_comments("Visual GUI Configurator and Live Terminal Designer for Fastfetch")
        about.set_website("https://github.com/misterkisik/fetchcraft")
        about.set_issue_url("https://github.com/misterkisik/fetchcraft/issues")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.present(self)
