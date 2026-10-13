"""
FetchCraft Internationalization (i18n) Module
Supported languages: ru (Русский), en (English), es (Español), fr (Français).
"""

import os
import json
from typing import Dict, Any, Callable, List

CONFIG_DIR = os.path.expanduser("~/.config/fetchcraft")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ru": "Русский",
    "en": "English",
    "es": "Español",
    "fr": "Français"
}

_current_lang = "ru"
_listeners: List[Callable[[], None]] = []

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Application & Header
    'app_title': {
        'ru': 'FetchCraft',
        'en': 'FetchCraft',
        'es': 'FetchCraft',
        'fr': 'FetchCraft'
    },
    'app_subtitle': {
        'ru': 'Визуальный конфигуратор и живой дизайнер Fastfetch',
        'en': 'Fastfetch Visual GUI Designer & Configurator',
        'es': 'Diseñador visual y configurador de Fastfetch',
        'fr': 'Concepteur visuel et configurateur de Fastfetch'
    },
    'tab_modules': {
        'ru': 'Модули',
        'en': 'Modules',
        'es': 'Módulos',
        'fr': 'Modules'
    },
    'tab_style': {
        'ru': 'Стили и цвета',
        'en': 'Style &amp; Colors',
        'es': 'Estilo y colores',
        'fr': 'Style et couleurs'
    },
    'tab_logo': {
        'ru': 'Логотипы и арт',
        'en': 'Logo &amp; Art',
        'es': 'Logotipo y arte',
        'fr': 'Logo et art'
    },
    'tab_presets': {
        'ru': 'Пресеты',
        'en': 'Presets',
        'es': 'Preajustes',
        'fr': 'Préréglages'
    },

    # HeaderBar buttons
    'btn_apply': {
        'ru': 'Применить',
        'en': 'Apply',
        'es': 'Aplicar',
        'fr': 'Appliquer'
    },
    'btn_apply_tooltip': {
        'ru': 'Сохранить и применить в ~/.config/fastfetch/config.jsonc',
        'en': 'Save and apply to ~/.config/fastfetch/config.jsonc',
        'es': 'Guardar y aplicar en ~/.config/fastfetch/config.jsonc',
        'fr': 'Enregistrer et appliquer dans ~/.config/fastfetch/config.jsonc'
    },
    'btn_terminal_tooltip': {
        'ru': 'Тест Fastfetch в системном терминале',
        'en': 'Test Fastfetch in External Terminal',
        'es': 'Probar Fastfetch en terminal externo',
        'fr': 'Tester Fastfetch dans le terminal externe'
    },

    # Menu items
    'menu_copy_config': {
        'ru': 'Копировать config.jsonc',
        'en': 'Copy config.jsonc',
        'es': 'Copiar config.jsonc',
        'fr': 'Copier config.jsonc'
    },
    'menu_export': {
        'ru': 'Экспорт в файл…',
        'en': 'Export to File…',
        'es': 'Exportar a archivo…',
        'fr': 'Exporter vers un fichier…'
    },
    'menu_reload': {
        'ru': 'Перезагрузить с диска',
        'en': 'Reload from Disk',
        'es': 'Recargar desde el disco',
        'fr': 'Recharger depuis le disque'
    },
    'menu_language': {
        'ru': 'Язык (Language)',
        'en': 'Language',
        'es': 'Idioma',
        'fr': 'Langue'
    },
    'menu_about': {
        'ru': 'О программе',
        'en': 'About FetchCraft',
        'es': 'Acerca de FetchCraft',
        'fr': 'À propos de FetchCraft'
    },
    'menu_options_tooltip': {
        'ru': 'Параметры и меню',
        'en': 'Options',
        'es': 'Opciones',
        'fr': 'Options'
    },

    # About Dialog
    'about_comments': {
        'ru': 'Интерактивный графический конфигуратор и живой дизайнер Fastfetch для Arch Linux и Linux.',
        'en': 'Interactive visual GUI configurator and live terminal designer for Fastfetch on Arch Linux & Linux.',
        'es': 'Configurador gráfico interactivo y diseñador en vivo para Fastfetch en Arch Linux y Linux.',
        'fr': 'Configurateur graphique interactif et concepteur en direct pour Fastfetch sous Arch Linux et Linux.'
    },

    # Welcome / First Run Dialog
    'welcome_title': {
        'ru': 'Добро пожаловать в FetchCraft!',
        'en': 'Welcome to FetchCraft!',
        'es': '¡Bienvenido a FetchCraft!',
        'fr': 'Bienvenue dans FetchCraft !'
    },
    'welcome_subtitle': {
        'ru': 'Выберите язык интерфейса для комфортной работы с программой:',
        'en': 'Select your preferred interface language to continue:',
        'es': 'Seleccione su idioma preferido para continuar:',
        'fr': "Sélectionnez votre langue d'interface préférée pour continuer :"
    },
    'welcome_continue': {
        'ru': 'Продолжить',
        'en': 'Continue',
        'es': 'Continuar',
        'fr': 'Continuer'
    },

    # Toasts
    'toast_config_applied': {
        'ru': 'Конфигурация успешно применена к {path} 🚀',
        'en': 'Configuration applied to {path} 🚀',
        'es': '¡Configuración aplicada en {path}! 🚀',
        'fr': 'Configuration appliquée à {path} ! 🚀'
    },
    'toast_copied_config': {
        'ru': 'Конфигурация скопирована в буфер обмена!',
        'en': 'Configuration copied to clipboard!',
        'es': '¡Configuración copiada al portapapeles!',
        'fr': 'Configuration copiée dans le presse-papiers !'
    },
    'toast_copied_terminal': {
        'ru': 'Вывод терминала скопирован в буфер обмена!',
        'en': 'Copied terminal output to clipboard!',
        'es': '¡Salida del terminal copiada al portapapeles!',
        'fr': 'Sortie du terminal copiée dans le presse-papiers !'
    },
    'toast_exported': {
        'ru': 'Конфигурация экспортирована в {name}!',
        'en': 'Exported configuration to {name}!',
        'es': '¡Configuración exportada a {name}!',
        'fr': 'Configuration exportée vers {name} !'
    },
    'toast_reloaded': {
        'ru': 'Конфигурация перезагружена с диска.',
        'en': 'Reloaded configuration from disk.',
        'es': 'Configuración recargada desde el disco.',
        'fr': 'Configuration rechargée depuis le disque.'
    },
    'toast_preset_loaded': {
        'ru': 'Загружен пресет «{name}»!',
        'en': "Loaded '{name}' preset!",
        'es': "¡Preajuste '{name}' cargado!",
        'fr': "Préréglage « {name} » chargé !"
    },
    'toast_backup_restored': {
        'ru': 'Конфигурация восстановлена из резервной копии!',
        'en': 'Configuration restored from backup!',
        'es': '¡Configuración restaurada desde la copia de seguridad!',
        'fr': 'Configuration restaurée depuis la sauvegarde !'
    },
    'toast_lang_changed': {
        'ru': 'Язык интерфейса изменён',
        'en': 'Interface language updated',
        'es': 'Idioma de la interfaz actualizado',
        'fr': "Langue de l'interface mise à jour"
    },
    'toast_terminal_spawned': {
        'ru': 'Запущено окно тестирования Fastfetch!',
        'en': 'Spawned Fastfetch terminal test window!',
        'es': '¡Ventana de prueba de Fastfetch iniciada!',
        'fr': 'Fenêtre de test Fastfetch lancée !'
    },
    'toast_terminal_not_found': {
        'ru': 'Не найден подходящий эмулятор терминала.',
        'en': 'No external terminal emulator found.',
        'es': 'No se encontró ningún emulador de terminal.',
        'fr': 'Aucun émulateur de terminal trouvé.'
    },

    # Live Preview Panel
    'preview_heading': {
        'ru': 'Живое превью Fastfetch',
        'en': 'Live Fastfetch Preview',
        'es': 'Vista previa en vivo de Fastfetch',
        'fr': 'Aperçu en direct de Fastfetch'
    },
    'preview_zoom_out_tip': {
        'ru': 'Уменьшить шрифт терминала',
        'en': 'Decrease terminal font size',
        'es': 'Disminuir tamaño de fuente',
        'fr': 'Diminuer la taille de la police'
    },
    'preview_zoom_in_tip': {
        'ru': 'Увеличить шрифт терминала',
        'en': 'Increase terminal font size',
        'es': 'Aumentar tamaño de fuente',
        'fr': 'Augmenter la taille de la police'
    },
    'preview_copy_tip': {
        'ru': 'Скопировать вывод терминала',
        'en': 'Copy output to clipboard',
        'es': 'Copiar salida al portapapeles',
        'fr': 'Copier la sortie dans le presse-papiers'
    },
    'preview_refresh_tip': {
        'ru': 'Обновить превью',
        'en': 'Refresh preview',
        'es': 'Actualizar vista previa',
        'fr': "Actualiser l'aperçu"
    },

    # Modules View
    'modules_group_title': {
        'ru': 'Активные модули',
        'en': 'Active Modules',
        'es': 'Módulos activos',
        'fr': 'Modules actifs'
    },
    'modules_group_desc': {
        'ru': 'Изменяйте порядок, настраивайте подписи и форматы вывода в терминале.',
        'en': 'Reorder, configure, or remove modules to display in terminal output.',
        'es': 'Reordene, configure o elimine módulos para la salida del terminal.',
        'fr': 'Réorganisez, configurez ou supprimez les modules à afficher.'
    },
    'modules_add_btn': {
        'ru': 'Добавить модуль',
        'en': 'Add Module',
        'es': 'Añadir módulo',
        'fr': 'Ajouter un module'
    },
    'modules_move_up': {
        'ru': 'Вверх',
        'en': 'Move Up',
        'es': 'Mover arriba',
        'fr': 'Monter'
    },
    'modules_move_down': {
        'ru': 'Вниз',
        'en': 'Move Down',
        'es': 'Mover abajo',
        'fr': 'Descendre'
    },
    'modules_edit_tip': {
        'ru': 'Редактировать ключ / формат',
        'en': 'Edit Module Key / Format',
        'es': 'Editar clave / formato',
        'fr': 'Modifier clé / format'
    },
    'modules_remove_tip': {
        'ru': 'Удалить модуль',
        'en': 'Remove Module',
        'es': 'Eliminar módulo',
        'fr': 'Supprimer le module'
    },
    'modules_dialog_title': {
        'ru': 'Добавить модуль Fastfetch',
        'en': 'Add Fastfetch Module',
        'es': 'Añadir módulo de Fastfetch',
        'fr': 'Ajouter un module Fastfetch'
    },
    'modules_search_placeholder': {
        'ru': 'Поиск модулей (cpu, ram, gpu, ip, disk)...',
        'en': 'Search modules (e.g. cpu, ram, gpu, ip, disk)...',
        'es': 'Buscar módulos (cpu, ram, gpu, ip, disk)...',
        'fr': 'Rechercher des modules (cpu, ram, gpu, ip, disk)...'
    },
    'modules_edit_dialog_title': {
        'ru': 'Свойства модуля',
        'en': 'Edit Module',
        'es': 'Propiedades del módulo',
        'fr': 'Propriétés du module'
    },
    'modules_edit_type': {
        'ru': 'Тип модуля',
        'en': 'Module Type',
        'es': 'Tipo de módulo',
        'fr': 'Type de module'
    },
    'modules_edit_key': {
        'ru': 'Своя подпись / Ключ',
        'en': 'Custom Key / Label',
        'es': 'Clave / Etiqueta personalizada',
        'fr': 'Clé / Étiquette personnalisée'
    },
    'modules_edit_format': {
        'ru': 'Строка формата (необязательно)',
        'en': 'Format String (Optional)',
        'es': 'Cadena de formato (Opcional)',
        'fr': 'Chaîne de format (Facultatif)'
    },
    'btn_cancel': {
        'ru': 'Отмена',
        'en': 'Cancel',
        'es': 'Cancelar',
        'fr': 'Annuler'
    },
    'btn_save': {
        'ru': 'Сохранить',
        'en': 'Save',
        'es': 'Guardar',
        'fr': 'Enregistrer'
    },

    # Style View
    'style_colors_group': {
        'ru': 'Цвета и подсветка',
        'en': 'Colors &amp; Highlighting',
        'es': 'Colores y resaltado',
        'fr': 'Couleurs et mise en valeur'
    },
    'style_colors_desc': {
        'ru': 'Настройка ANSI-акцентов для названий, заголовка и выводимых значений.',
        'en': 'Customize ANSI color accents for keys, title, and output text.',
        'es': 'Personalice los colores ANSI para claves, título y texto.',
        'fr': 'Personnalisez les couleurs ANSI pour les clés, le titre et le texte.'
    },
    'style_keys_color': {
        'ru': 'Цвет ключей',
        'en': 'Keys Color',
        'es': 'Color de las claves',
        'fr': 'Couleur des clés'
    },
    'style_keys_color_sub': {
        'ru': 'Цвет названий модулей слева',
        'en': 'Color of module names on the left',
        'es': 'Color de los nombres de módulos a la izquierda',
        'fr': 'Couleur des noms de modules à gauche'
    },
    'style_title_color': {
        'ru': 'Цвет заголовка',
        'en': 'Title Color',
        'es': 'Color del título',
        'fr': 'Couleur du titre'
    },
    'style_title_color_sub': {
        'ru': 'Цвет строки user@hostname',
        'en': 'Color of user@hostname header',
        'es': 'Color del encabezado usuario@equipo',
        'fr': "Couleur de l'en-tête utilisateur@machine"
    },
    'style_output_color': {
        'ru': 'Цвет значений',
        'en': 'Output Values Color',
        'es': 'Color de los valores',
        'fr': 'Couleur des valeurs'
    },
    'style_output_color_sub': {
        'ru': 'Цвет определённых системных данных',
        'en': 'Color of detected system information values',
        'es': 'Color de la información detectada del sistema',
        'fr': 'Couleur des informations système détectées'
    },
    'style_sep_color': {
        'ru': 'Цвет разделителя',
        'en': 'Separator Color',
        'es': 'Color del separador',
        'fr': 'Couleur du séparateur'
    },
    'style_sep_color_sub': {
        'ru': 'Цвет знака между ключом и значением',
        'en': 'Color of the delimiter between keys and values',
        'es': 'Color del delimitador entre claves и valores',
        'fr': 'Couleur du délimiteur entre clés et valeurs'
    },
    'style_sep_group': {
        'ru': 'Разделитель и символы',
        'en': 'Separator &amp; Delimiters',
        'es': 'Separador y delimitadores',
        'fr': 'Séparateur et délimiteurs'
    },
    'style_sep_desc': {
        'ru': 'Символ, разделяющий название параметра и его значение.',
        'en': 'Character printed between module label and value.',
        'es': 'Carácter impreso entre la etiqueta del módulo y su valor.',
        'fr': 'Caractère affiché entre le nom du module et sa valeur.'
    },
    'style_sep_preset': {
        'ru': 'Пресет разделителя',
        'en': 'Separator Preset',
        'es': 'Preajuste de separador',
        'fr': 'Préréglage de séparateur'
    },
    'style_custom_sep': {
        'ru': 'Свой символ разделителя',
        'en': 'Custom Separator String',
        'es': 'Separador personalizado',
        'fr': 'Chaîne de séparateur personnalisée'
    },
    'style_palette_group': {
        'ru': 'Блоки палитры цветов',
        'en': 'Color Palette Blocks',
        'es': 'Bloques de paleta de colores',
        'fr': 'Blocs de palette de couleurs'
    },
    'style_palette_desc': {
        'ru': 'Форма символов для нижней 16-цветовой тестовой полосы.',
        'en': 'Symbol style for the 16-color test bar at the bottom.',
        'es': 'Estilo de símbolo para la barra de prueba de 16 colores.',
        'fr': 'Style de symbole pour la barre de test de 16 couleurs.'
    },
    'style_palette_symbol': {
        'ru': 'Символ полосы палитры',
        'en': 'Palette Block Symbol',
        'es': 'Símbolo del bloque de paleta',
        'fr': 'Symbole du bloc de palette'
    },

    # Logo View
    'logo_source_group': {
        'ru': 'Логотип и оформление',
        'en': 'Logo Source &amp; Artwork',
        'es': 'Logotipo y arte',
        'fr': 'Source du logo et illustration'
    },
    'logo_source_desc': {
        'ru': 'Выбор ASCII-арта дистрибутива или собственного изображения.',
        'en': 'Select which distribution ASCII art or custom image to display.',
        'es': 'Seleccione el arte ASCII de distribución o imagen personalizada.',
        'fr': 'Sélectionnez le logo ASCII de la distribution ou une image.'
    },
    'logo_distro': {
        'ru': 'Логотип дистрибутива',
        'en': 'Distribution Logo',
        'es': 'Logotipo de distribución',
        'fr': 'Logo de la distribution'
    },
    'logo_custom_name': {
        'ru': 'Встроенное имя дистрибутива',
        'en': 'Built-in Distro Name',
        'es': 'Nombre de distribución integrada',
        'fr': 'Nom de distribution intégrée'
    },
    'logo_file_path': {
        'ru': 'Путь к файлу логотипа',
        'en': 'Logo File Path',
        'es': 'Ruta del archivo de logotipo',
        'fr': 'Chemin du fichier de logo'
    },
    'logo_browse_tip': {
        'ru': 'Выбрать файл логотипа...',
        'en': 'Browse Logo File...',
        'es': 'Examinar archivo de logotipo...',
        'fr': 'Parcourir le fichier de logo...'
    },
    'logo_layout_group': {
        'ru': 'Отступы и рендеринг',
        'en': 'Logo Spacing &amp; Rendering',
        'es': 'Espaciado y renderizado',
        'fr': 'Espacement et rendu'
    },
    'logo_layout_desc': {
        'ru': 'Настройка расстояния между логотипом и списком данных.',
        'en': 'Fine-tune character padding between the logo and system metrics.',
        'es': 'Ajuste el espaciado en caracteres entre el logotipo y los datos.',
        'fr': "Ajustez l'espacement entre le logo et les informations."
    },
    'logo_padding_right': {
        'ru': 'Отступ справа',
        'en': 'Right Padding',
        'es': 'Espaciado derecho',
        'fr': 'Espacement droit'
    },
    'logo_padding_right_sub': {
        'ru': 'Количество колонок между логотипом и текстом',
        'en': 'Number of empty columns between logo and text',
        'es': 'Número de columnas vacías entre logotipo y texto',
        'fr': 'Nombre de colonnes vides entre logo et texte'
    },
    'logo_render_type': {
        'ru': 'Тип вывода логотипа',
        'en': 'Logo Render Type',
        'es': 'Tipo de renderizado del logotipo',
        'fr': 'Type de rendu du logo'
    },

    # Presets View
    'presets_curated_group': {
        'ru': 'Готовые пресеты FetchCraft',
        'en': 'Curated FetchCraft Presets',
        'es': 'Preajustes seleccionados',
        'fr': 'Préréglages sélectionnés'
    },
    'presets_curated_desc': {
        'ru': 'Элегантные темы оформления для Arch Linux, минималистичных рабочих столов и терминалов.',
        'en': 'Polished themes ready for Arch Linux desktops, minimal rices, and terminals.',
        'es': 'Temas pulidos listos para escritorios Arch Linux y terminales.',
        'fr': 'Thèmes soignés prêts pour Arch Linux et les terminaux.'
    },
    'presets_load_btn': {
        'ru': 'Загрузить пресет',
        'en': 'Load Preset',
        'es': 'Cargar preajuste',
        'fr': 'Charger le préréglage'
    },
    'presets_system_group': {
        'ru': 'Системные пресеты Fastfetch',
        'en': 'Fastfetch System Presets',
        'es': 'Preajustes del sistema',
        'fr': 'Préréglages système'
    },
    'presets_system_desc': {
        'ru': 'Официальные пресеты, установленные в /usr/share/fastfetch/presets/.',
        'en': 'Official presets installed on your system in /usr/share/fastfetch/presets/.',
        'es': 'Preajustes oficiales instalados en /usr/share/fastfetch/presets/.',
        'fr': 'Préréglages officiels installés dans /usr/share/fastfetch/presets/.'
    },
    'presets_backup_group': {
        'ru': 'Резервная копия конфигурации',
        'en': 'Configuration Backup',
        'es': 'Copia de seguridad',
        'fr': 'Sauvegarde de configuration'
    },
    'presets_backup_desc': {
        'ru': 'FetchCraft автоматически сохраняет резервную копию при каждом применении настроек.',
        'en': 'FetchCraft automatically creates a backup whenever you apply changes.',
        'es': 'FetchCraft crea una copia de seguridad automáticamente al aplicar cambios.',
        'fr': 'FetchCraft crée automatiquement une sauvegarde lors de chaque application.'
    },
    'presets_restore_row': {
        'ru': 'Восстановить предыдущую копию',
        'en': 'Restore Previous Backup',
        'es': 'Restaurar copia anterior',
        'fr': 'Restaurer la sauvegarde précédente'
    },
    'presets_restore_sub': {
        'ru': 'Откатить ~/.config/fastfetch/config.jsonc к файлу config.jsonc.bak',
        'en': 'Revert ~/.config/fastfetch/config.jsonc to config.jsonc.bak',
        'es': 'Revertir ~/.config/fastfetch/config.jsonc a config.jsonc.bak',
        'fr': 'Restaurer ~/.config/fastfetch/config.jsonc depuis config.jsonc.bak'
    },
    'presets_restore_btn': {
        'ru': 'Восстановить бэкап',
        'en': 'Restore Backup',
        'es': 'Restaurar copia',
        'fr': 'Restaurer la sauvegarde'
    },
}

def load_saved_language() -> str:
    """Loads saved language from ~/.config/fetchcraft/config.json or system locale."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang = data.get("language")
                if lang in SUPPORTED_LANGUAGES:
                    return lang
    except Exception:
        pass

    # Detect by system LANG
    sys_lang = os.environ.get("LANG", "").split(".")[0].split("_")[0].lower()
    if sys_lang in SUPPORTED_LANGUAGES:
        return sys_lang

    return "ru"

def save_language(lang: str, first_run_done: bool = True):
    """Saves language preference to ~/.config/fetchcraft/config.json."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            data = {}
            if os.path.exists(CONFIG_PATH):
                try:
                    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    pass
            data["language"] = lang
            if first_run_done:
                data["first_run_done"] = True
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[FetchCraft] Error saving language config: {e}")

def set_language(lang: str, first_run_done: bool = True):
    """Sets active language and notifies listeners."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang
        save_language(lang, first_run_done=first_run_done)
        for listener in _listeners:
            try:
                listener()
            except Exception as e:
                print(f"[FetchCraft] Error in i18n listener: {e}")

def get_current_language() -> str:
    return _current_lang

def add_language_change_listener(callback: Callable[[], None]):
    _listeners.append(callback)

def is_first_run() -> bool:
    """Checks if first run language dialog should be presented."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return not data.get("first_run_done", False)
    except Exception:
        pass
    return True

def tr(key: str, **kwargs) -> str:
    """Retrieves translated string by key for current language."""
    lang_dict = TRANSLATIONS.get(key)
    if not lang_dict:
        return key

    text = lang_dict.get(_current_lang) or lang_dict.get("en") or lang_dict.get("ru") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

# Initialize on import
_current_lang = load_saved_language()
