<div align="center">

# ⚡ FetchCraft

**Interactive Visual GUI Configurator and Live Terminal Designer for Fastfetch**

[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/Platform-Arch%20Linux%20%7C%20Linux-brightgreen.svg)](#)
[![GTK4 & Libadwaita](https://img.shields.io/badge/UI-GTK4%20%2F%20Libadwaita-blue.svg)](#)

*Craft your ultimate terminal system fetch with zero manual JSON guesswork.*

</div>

---

## 🌟 Features

- **📺 Real-Time Terminal Live Preview**: Built directly with `Vte.Terminal` using Catppuccin Mocha colors and true monospace font rendering. Every toggle, separator, and color change renders instantly without leaving the window.
- **🧩 Visual Module Manager**:
  - Reorder, enable, disable, and configure all 76+ Fastfetch modules (CPU, GPU, Memory, Disks, Kernel, Uptime, DE, WM, IP, Media, etc.).
  - Searchable "Add Module" modal with category filters.
  - Customize labels, formatting tokens, and icons per module.
- **🎨 Color & Delimiter Studio**:
  - Customize Key colors, Title colors, Output colors, and Separators.
  - Instant separator presets (` ➜ `, ` : `, ` │ `, ` ➔ `, ` » `) or custom characters.
  - 16-color test bar styling (circles, diamonds, squares, blocks, stars).
- **🐧 Distro Logos & Custom ASCII Art**:
  - Over 500+ built-in ASCII distro logos (Arch, Fedora, Ubuntu, Debian, Gentoo, NixOS, Void, etc.).
  - Support for custom text/ASCII files and images via Chafa / Kitty graphics.
  - Adjust padding and alignment dynamically.
- **🚀 One-Click Presets & System Templates**:
  - Handcrafted curated presets (*Arch Modern*, *Neofetch Classic*, *Compact Rice*, *Cyberpunk Neon*, *Hardware Master*, *Minimalist*).
  - Quick browser for all system presets in `/usr/share/fastfetch/presets/`.
- **🛡️ Safe Backup & Apply**:
  - Applies directly to `~/.config/fastfetch/config.jsonc`.
  - Automatically creates a `.bak` backup file before writing.
  - One-click restore button.
  - Export to custom file or copy JSONC to clipboard.

---

## 📦 Requirements

- **Linux** (Arch Linux, Fedora, Ubuntu, etc.)
- **Python 3.9+**
- `fastfetch` (`pacman -S fastfetch`)
- `gtk4`, `libadwaita`, `vte4` (`pacman -S gtk4 libadwaita vte4 python-gobject`)

---

## 🚀 Running FetchCraft

Run directly from repository:
```bash
./bin/fetchcraft
```

Or install locally with pip:
```bash
pip install -e .
```

---

## 📝 License

FetchCraft is released under the **GNU General Public License v3.0**.
