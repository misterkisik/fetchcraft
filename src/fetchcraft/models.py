"""
FetchCraft Models and Definitions
Provides module registry, presets, color options, and logos for Fastfetch.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ModuleDefinition:
    id: str
    name: str
    category: str
    icon: str
    description: str
    default_enabled: bool = False
    supports_key: bool = True
    supports_format: bool = True

MODULE_REGISTRY: List[ModuleDefinition] = [
    # System info
    ModuleDefinition("title", "Username &amp; Hostname", "System", "avatar-default-symbolic", "Prints user@hostname title header", default_enabled=True, supports_key=False),
    ModuleDefinition("separator", "Header Separator", "System", "format-text-underline-symbolic", "Line underneath title", default_enabled=True, supports_key=False),
    ModuleDefinition("os", "Operating System", "System", "distributor-logo-symbolic", "OS name, distribution and architecture", default_enabled=True),
    ModuleDefinition("kernel", "Linux Kernel", "System", "system-run-symbolic", "Kernel release and version", default_enabled=True),
    ModuleDefinition("uptime", "Uptime", "System", "alarm-symbolic", "System uptime duration", default_enabled=True),
    ModuleDefinition("packages", "Packages Count", "System", "package-x-generic-symbolic", "Installed packages across pacman, flatpak, etc.", default_enabled=True),
    ModuleDefinition("shell", "Shell", "System", "utilities-terminal-symbolic", "Current shell name and version (bash, zsh, etc.)", default_enabled=True),
    ModuleDefinition("initsystem", "Init System", "System", "system-component-symbolic", "Systemd or alternative init system"),
    ModuleDefinition("processes", "Process Count", "System", "utilities-system-monitor-symbolic", "Total running processes"),
    ModuleDefinition("datetime", "Date &amp; Time", "System", "time-symbolic", "Current local date and time"),
    ModuleDefinition("locale", "System Locale", "System", "preferences-desktop-locale-symbolic", "Current language and charset", default_enabled=False),

    # Desktop & Appearance
    ModuleDefinition("de", "Desktop Environment", "Desktop", "desktop-symbolic", "Current DE (GNOME, KDE, XFCE, etc.)", default_enabled=True),
    ModuleDefinition("wm", "Window Manager", "Desktop", "window-new-symbolic", "Current WM (Mutter, KWin, Hyprland, Sway, etc.)", default_enabled=True),
    ModuleDefinition("wmtheme", "WM Theme", "Desktop", "preferences-desktop-theme-symbolic", "Window manager decoration theme"),
    ModuleDefinition("theme", "GTK/Qt Theme", "Desktop", "preferences-desktop-appearance-symbolic", "GTK / Qt theme name", default_enabled=True),
    ModuleDefinition("icons", "Icon Theme", "Desktop", "preferences-desktop-icons-symbolic", "System icon pack name", default_enabled=True),
    ModuleDefinition("font", "System Font", "Desktop", "preferences-desktop-font-symbolic", "Default interface font", default_enabled=True),
    ModuleDefinition("cursor", "Cursor Theme", "Desktop", "input-mouse-symbolic", "Mouse cursor theme and size"),
    ModuleDefinition("wallpaper", "Wallpaper Path", "Desktop", "preferences-desktop-wallpaper-symbolic", "Path to active desktop background"),
    ModuleDefinition("terminal", "Terminal Emulator", "Desktop", "utilities-terminal-symbolic", "Terminal application name", default_enabled=True),
    ModuleDefinition("terminalfont", "Terminal Font", "Desktop", "font-x-generic-symbolic", "Font and size configured in terminal", default_enabled=True),

    # Hardware
    ModuleDefinition("host", "Computer Model", "Hardware", "computer-symbolic", "Motherboard or PC model (e.g. ThinkPad)", default_enabled=True),
    ModuleDefinition("cpu", "Processor (CPU)", "Hardware", "hardware-cpu-symbolic", "CPU model, core count and clock speed", default_enabled=True),
    ModuleDefinition("gpu", "Graphics (GPU)", "Hardware", "video-display-symbolic", "Dedicated and integrated GPU models", default_enabled=True),
    ModuleDefinition("memory", "Memory (RAM)", "Hardware", "media-flash-symbolic", "Used and total RAM memory", default_enabled=True),
    ModuleDefinition("swap", "Swap Space", "Hardware", "drive-multidisk-symbolic", "Virtual memory usage", default_enabled=True),
    ModuleDefinition("disk", "Disk Storage", "Hardware", "drive-harddisk-symbolic", "Partition usage and file systems", default_enabled=True),
    ModuleDefinition("display", "Monitors &amp; Resolution", "Hardware", "video-display-symbolic", "Connected screens, resolution and refresh rates", default_enabled=True),
    ModuleDefinition("battery", "Battery Status", "Hardware", "battery-good-symbolic", "Battery percentage and health"),
    ModuleDefinition("poweradapter", "Power Adapter", "Hardware", "ac-adapter-symbolic", "Connected power charger wattage"),
    ModuleDefinition("bluetooth", "Bluetooth Devices", "Hardware", "bluetooth-active-symbolic", "Connected Bluetooth peripherals"),
    ModuleDefinition("sound", "Audio Output", "Hardware", "audio-volume-high-symbolic", "Sound cards and active audio devices"),
    ModuleDefinition("gamepad", "Game Controller", "Hardware", "input-gaming-symbolic", "Connected gamepads"),

    # Network & Media
    ModuleDefinition("localip", "Local IP Address", "Network", "network-wired-symbolic", "Local network IPv4/IPv6 address"),
    ModuleDefinition("publicip", "Public IP Address", "Network", "network-workgroup-symbolic", "External public IP address"),
    ModuleDefinition("wifi", "Wi-Fi Network", "Network", "network-wireless-symbolic", "Current connected Wi-Fi SSID"),
    ModuleDefinition("dns", "DNS Server", "Network", "network-server-symbolic", "Configured DNS resolvers"),
    ModuleDefinition("media", "Now Playing Media", "Network", "audio-speakers-symbolic", "Song title and artist from MPRIS"),

    # Formatting & Decorators
    ModuleDefinition("break", "Empty Line Spacer", "Decorations", "insert-space-symbolic", "Blank line separator", default_enabled=True, supports_key=False, supports_format=False),
    ModuleDefinition("colors", "Color Palette Blocks", "Decorations", "color-select-symbolic", "Terminal 16-color test blocks or symbols", default_enabled=True, supports_key=False),
    ModuleDefinition("custom", "Custom Text Line", "Decorations", "text-x-generic-symbolic", "User-defined custom text line", default_enabled=False),
]

POPULAR_LOGOS = [
    ("arch", "Arch Linux (Standard)"),
    ("arch_small", "Arch Linux (Small / Compact)"),
    ("arch2", "Arch Linux (Alt 2)"),
    ("endeavouros", "EndeavourOS"),
    ("manjaro", "Manjaro"),
    ("cachyos", "CachyOS"),
    ("garuda", "Garuda Linux"),
    ("fedora", "Fedora"),
    ("fedora_small", "Fedora (Small)"),
    ("ubuntu", "Ubuntu"),
    ("ubuntu_small", "Ubuntu (Small)"),
    ("debian", "Debian"),
    ("debian_small", "Debian (Small)"),
    ("nixos", "NixOS"),
    ("nixos_small", "NixOS (Small)"),
    ("gentoo", "Gentoo"),
    ("void", "Void Linux"),
    ("alpine", "Alpine Linux"),
    ("opensuse-tumbleweed", "openSUSE Tumbleweed"),
    ("popos", "Pop!_OS"),
    ("linuxmint", "Linux Mint"),
    ("steamos", "SteamOS"),
    ("linux", "Generic Linux Tux"),
    ("linux_small", "Generic Linux Tux (Small)"),
    ("freebsd", "FreeBSD"),
    ("macos", "macOS Apple"),
    ("windows11", "Windows 11"),
    ("none", "None (Disable Logo)"),
]

COLOR_NAMES = [
    ("default", "Default"),
    ("black", "Black"),
    ("red", "Red"),
    ("green", "Green"),
    ("yellow", "Yellow"),
    ("blue", "Blue"),
    ("magenta", "Magenta"),
    ("cyan", "Cyan"),
    ("white", "White"),
    ("bright_black", "Bright Black (Gray)"),
    ("bright_red", "Bright Red"),
    ("bright_green", "Bright Green"),
    ("bright_yellow", "Bright Yellow"),
    ("bright_blue", "Bright Blue"),
    ("bright_magenta", "Bright Magenta"),
    ("bright_cyan", "Bright Cyan"),
    ("bright_white", "Bright White"),
]

SEPARATOR_PRESETS = [
    (": ", "Classic Colon ( : )"),
    (" ➜ ", "Modern Arrow ( ➜ )"),
    (" ➔ ", "Thick Arrow ( ➔ )"),
    ("  ", "Nerd Font Arrow (  )"),
    (" │ ", "Vertical Line ( │ )"),
    (" » ", "Double Chevrons ( » )"),
    (" ~ ", "Tilde ( ~ )"),
    (" - ", "Hyphen ( - )"),
]

COLOR_SYMBOLS = [
    ("block", "Solid Blocks ( █ )"),
    ("circle", "Circles ( ● )"),
    ("diamond", "Diamonds ( ◆ )"),
    ("triangle", "Triangles ( ▲ )"),
    ("star", "Stars ( ★ )"),
]

BUILTIN_PRESETS = {
    "arch_modern": {
        "name": "Arch Modern",
        "desc": "Sleek cyan accents with modern arrow separator and circle palette.",
        "icon": "distributor-logo-archlinux-symbolic",
        "config": {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "source": "arch",
                "padding": {"right": 2}
            },
            "display": {
                "separator": " ➜ ",
                "color": {
                    "keys": "cyan",
                    "title": "bright_blue"
                }
            },
            "modules": [
                "title",
                "separator",
                "os",
                "kernel",
                "uptime",
                "packages",
                "shell",
                "de",
                "wm",
                "theme",
                "icons",
                "terminal",
                "cpu",
                "gpu",
                "memory",
                "disk",
                "break",
                {"type": "colors", "symbol": "circle"}
            ]
        }
    },
    "neofetch_classic": {
        "name": "Neofetch Classic",
        "desc": "Faithful recreation of original Neofetch layout and standard color palette.",
        "icon": "view-grid-symbolic",
        "config": {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "source": "auto"
            },
            "display": {
                "separator": ": ",
                "color": {
                    "keys": "default",
                    "title": "default"
                }
            },
            "modules": [
                "title",
                "separator",
                "os",
                "host",
                {"type": "kernel", "format": "{release}"},
                "uptime",
                {"type": "packages", "combined": True},
                "shell",
                {"type": "display", "compactType": "original", "key": "Resolution"},
                {"type": "de", "key": "DE"},
                {"type": "wm", "key": "WM"},
                "wmtheme",
                "theme",
                "icons",
                "terminal",
                {"type": "terminalfont", "format": "{/name}{-}{/}{name}{?size} {size}{?}"},
                {"type": "cpu", "showPeCoreCount": False},
                {"type": "gpu", "key": "GPU", "format": "{name}"},
                {"type": "memory", "format": "{used} / {total}"},
                "break",
                "colors"
            ]
        }
    },
    "compact_rice": {
        "name": "Compact Rice",
        "desc": "Ultra-clean and narrow layout featuring compact small logo.",
        "icon": "application-x-addon-symbolic",
        "config": {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "source": "arch_small",
                "padding": {"right": 1}
            },
            "display": {
                "separator": " │ ",
                "color": {
                    "keys": "bright_cyan",
                    "title": "magenta"
                }
            },
            "modules": [
                "title",
                "separator",
                "os",
                "kernel",
                "uptime",
                "packages",
                "shell",
                "wm",
                "terminal",
                "cpu",
                "memory",
                "break",
                {"type": "colors", "symbol": "diamond"}
            ]
        }
    },
    "cyberpunk_neon": {
        "name": "Cyberpunk Neon",
        "desc": "Vibrant magenta and bright yellow palette with diamond indicators.",
        "icon": "applications-graphics-symbolic",
        "config": {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "source": "arch",
                "color": {"1": "bright_magenta", "2": "cyan"}
            },
            "display": {
                "separator": " » ",
                "color": {
                    "keys": "bright_magenta",
                    "title": "bright_yellow",
                    "separator": "cyan"
                }
            },
            "modules": [
                "title",
                "separator",
                "os",
                "kernel",
                "uptime",
                "packages",
                "shell",
                "de",
                "wm",
                "terminal",
                "cpu",
                "gpu",
                "memory",
                "disk",
                "localip",
                "media",
                "break",
                {"type": "colors", "symbol": "circle"}
            ]
        }
    },
    "hardware_master": {
        "name": "Hardware Master",
        "desc": "Deep hardware audit: CPU, GPU, RAM, Swap, Disks, Monitors, and Battery.",
        "icon": "drive-harddisk-symbolic",
        "config": {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "source": "auto"
            },
            "display": {
                "separator": " : ",
                "color": {
                    "keys": "green",
                    "title": "bright_green"
                }
            },
            "modules": [
                "title",
                "separator",
                "host",
                "cpu",
                "gpu",
                "memory",
                "swap",
                "disk",
                "display",
                "battery",
                "poweradapter",
                "sound",
                "break",
                "os",
                "kernel",
                "uptime",
                "break",
                {"type": "colors", "symbol": "block"}
            ]
        }
    },
    "minimalist": {
        "name": "Minimalist",
        "desc": "Strictly the essentials. Fast to read, zero clutter.",
        "icon": "format-justify-left-symbolic",
        "config": {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "source": "none"
            },
            "display": {
                "separator": "  ",
                "color": {
                    "keys": "bright_white",
                    "title": "cyan"
                }
            },
            "modules": [
                "title",
                "os",
                "kernel",
                "uptime",
                "packages",
                "shell",
                "memory",
                "break",
                {"type": "colors", "symbol": "circle"}
            ]
        }
    }
}
