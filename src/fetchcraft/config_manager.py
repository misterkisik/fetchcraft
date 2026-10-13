"""
FetchCraft Config Manager
Handles reading, writing, updating and serializing Fastfetch JSONC configuration.
"""

import copy
import json
import os
import re
import shutil
import tempfile
from typing import Any, Callable, Dict, List, Optional
from .models import BUILTIN_PRESETS

FASTFETCH_CONFIG_DIR = os.path.expanduser("~/.config/fastfetch")
FASTFETCH_CONFIG_PATH = os.path.join(FASTFETCH_CONFIG_DIR, "config.jsonc")
FASTFETCH_BACKUP_PATH = os.path.join(FASTFETCH_CONFIG_DIR, "config.jsonc.bak")

def strip_jsonc(text: str) -> str:
    """Safely strips C-style comments and trailing commas from JSONC while preserving strings."""
    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return ""
        return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|"(?:\\.|[^"\\])*"',
        re.DOTALL | re.MULTILINE
    )
    clean = re.sub(pattern, replacer, text)
    clean = re.sub(r',\s*([}\]])', r'\1', clean)
    return clean

class ConfigManager:
    def __init__(self):
        self._listeners: List[Callable[[], None]] = []
        self._config: Dict[str, Any] = {}
        self._temp_preview_file: Optional[str] = None
        self.load()

    def add_change_listener(self, callback: Callable[[], None]):
        """Register a callback that fires when configuration changes."""
        self._listeners.append(callback)

    def _notify_change(self):
        for listener in self._listeners:
            try:
                listener()
            except Exception as e:
                print(f"[FetchCraft] Error in change listener: {e}")

    def load(self):
        """Loads from ~/.config/fastfetch/config.jsonc or falls back to Arch Modern preset."""
        if os.path.exists(FASTFETCH_CONFIG_PATH):
            try:
                with open(FASTFETCH_CONFIG_PATH, "r", encoding="utf-8") as f:
                    content = f.read()
                clean = strip_jsonc(content)
                self._config = json.loads(clean)
                self._ensure_structure()
                self._notify_change()
                return
            except Exception as e:
                print(f"[FetchCraft] Failed to parse {FASTFETCH_CONFIG_PATH}: {e}. Using default preset.")

        # Default fallback
        self.apply_preset("arch_modern")

    def _ensure_structure(self):
        """Ensures standard top-level keys exist."""
        if "$schema" not in self._config:
            self._config["$schema"] = "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json"
        if "display" not in self._config or not isinstance(self._config["display"], dict):
            self._config["display"] = {}
        if "logo" not in self._config or not isinstance(self._config["logo"], dict):
            self._config["logo"] = {}
        if "modules" not in self._config or not isinstance(self._config["modules"], list):
            self._config["modules"] = []

    def get_config(self) -> Dict[str, Any]:
        return self._config

    def set_config(self, new_config: Dict[str, Any]):
        self._config = copy.deepcopy(new_config)
        self._ensure_structure()
        self._notify_change()

    def apply_preset(self, preset_key: str):
        """Applies a built-in preset or system preset."""
        if preset_key in BUILTIN_PRESETS:
            self._config = copy.deepcopy(BUILTIN_PRESETS[preset_key]["config"])
            self._ensure_structure()
            self._notify_change()

    def apply_preset_from_dict(self, preset_dict: Dict[str, Any]):
        """Applies a preset loaded from external file or dictionary."""
        self._config = copy.deepcopy(preset_dict)
        self._ensure_structure()
        self._notify_change()

    # --- Display Settings ---

    def get_separator(self) -> str:
        return self._config.get("display", {}).get("separator", ": ")

    def set_separator(self, separator: str):
        if "display" not in self._config:
            self._config["display"] = {}
        self._config["display"]["separator"] = separator
        self._notify_change()

    def get_color(self, element: str) -> str:
        """Element can be: keys, title, output, separator"""
        color_dict = self._config.get("display", {}).get("color", {})
        if isinstance(color_dict, dict):
            return color_dict.get(element, "default")
        return "default"

    def set_color(self, element: str, color_name: str):
        """Sets color for keys, title, output, or separator."""
        if "display" not in self._config:
            self._config["display"] = {}
        if "color" not in self._config["display"] or not isinstance(self._config["display"]["color"], dict):
            self._config["display"]["color"] = {}
        
        if color_name == "default":
            self._config["display"]["color"].pop(element, None)
            if not self._config["display"]["color"]:
                self._config["display"].pop("color", None)
        else:
            self._config["display"]["color"][element] = color_name
        self._notify_change()

    # --- Logo Settings ---

    def get_logo_source(self) -> str:
        return self._config.get("logo", {}).get("source", "auto")

    def set_logo_source(self, source: str):
        if "logo" not in self._config:
            self._config["logo"] = {}
        self._config["logo"]["source"] = source
        self._notify_change()

    def get_logo_type(self) -> str:
        return self._config.get("logo", {}).get("type", "auto")

    def set_logo_type(self, logo_type: str):
        if "logo" not in self._config:
            self._config["logo"] = {}
        if logo_type == "auto":
            self._config["logo"].pop("type", None)
        else:
            self._config["logo"]["type"] = logo_type
        self._notify_change()

    def get_logo_padding_right(self) -> int:
        return self._config.get("logo", {}).get("padding", {}).get("right", 1)

    def set_logo_padding_right(self, padding: int):
        if "logo" not in self._config:
            self._config["logo"] = {}
        if "padding" not in self._config["logo"] or not isinstance(self._config["logo"]["padding"], dict):
            self._config["logo"]["padding"] = {}
        self._config["logo"]["padding"]["right"] = padding
        self._notify_change()

    # --- Module Settings ---

    def get_modules(self) -> List[Any]:
        return self._config.get("modules", [])

    def set_modules(self, modules: List[Any]):
        self._config["modules"] = copy.deepcopy(modules)
        self._notify_change()

    def add_module(self, module_item: Any, index: Optional[int] = None):
        if "modules" not in self._config:
            self._config["modules"] = []
        if index is None or index >= len(self._config["modules"]):
            self._config["modules"].append(module_item)
        else:
            self._config["modules"].insert(index, module_item)
        self._notify_change()

    def remove_module(self, index: int):
        modules = self._config.get("modules", [])
        if 0 <= index < len(modules):
            modules.pop(index)
            self._notify_change()

    def move_module_up(self, index: int) -> bool:
        modules = self._config.get("modules", [])
        if 0 < index < len(modules):
            modules[index - 1], modules[index] = modules[index], modules[index - 1]
            self._notify_change()
            return True
        return False

    def move_module_down(self, index: int) -> bool:
        modules = self._config.get("modules", [])
        if 0 <= index < len(modules) - 1:
            modules[index + 1], modules[index] = modules[index], modules[index + 1]
            self._notify_change()
            return True
        return False

    def update_module(self, index: int, new_item: Any):
        modules = self._config.get("modules", [])
        if 0 <= index < len(modules):
            modules[index] = new_item
            self._notify_change()

    # --- Temp Preview File & Export ---

    def write_temp_preview(self) -> str:
        """Writes current configuration to a temporary JSONC file for fastfetch execution."""
        if not self._temp_preview_file or not os.path.exists(self._temp_preview_file):
            tmp = tempfile.NamedTemporaryFile("w", suffix=".jsonc", delete=False)
            self._temp_preview_file = tmp.name
            tmp.close()

        with open(self._temp_preview_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=4, ensure_ascii=False)
            f.write("\n")

        return self._temp_preview_file

    def to_jsonc_string(self) -> str:
        """Generates formatted JSONC with helpful header comment."""
        header = (
            "// Fastfetch Configuration\n"
            "// Generated with FetchCraft (https://github.com/misterkisik/fetchcraft)\n\n"
        )
        body = json.dumps(self._config, indent=4, ensure_ascii=False)
        return header + body + "\n"

    def save_to_system(self) -> str:
        """
        Saves current configuration to ~/.config/fastfetch/config.jsonc.
        Creates backup of previous file to config.jsonc.bak.
        Returns message of action taken.
        """
        os.makedirs(FASTFETCH_CONFIG_DIR, exist_ok=True)
        if os.path.exists(FASTFETCH_CONFIG_PATH):
            shutil.copy2(FASTFETCH_CONFIG_PATH, FASTFETCH_BACKUP_PATH)

        with open(FASTFETCH_CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(self.to_jsonc_string())

        return FASTFETCH_CONFIG_PATH

    def has_backup(self) -> bool:
        return os.path.exists(FASTFETCH_BACKUP_PATH)

    def restore_backup(self) -> bool:
        if self.has_backup():
            shutil.copy2(FASTFETCH_BACKUP_PATH, FASTFETCH_CONFIG_PATH)
            self.load()
            return True
        return False

    def export_to_file(self, target_path: str):
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(self.to_jsonc_string())
