import json

def load_theme():
    with open("theme_config.json", "r") as f:
        data = json.load(f)
    theme_name = data.get("theme", "Dark")

    themes = {
        "Dark": {
            "bg": "#0D1117",
            "fg": "#C9D1D9",
            "accent": "#58A6FF",
            "button_bg": "#1F6FEB",
            "font_color": "#C9D1D9"
        },
        "Light": {
            "bg": "#FFFFFF",
            "fg": "#000000",
            "accent": "#0078D4",
            "button_bg": "#E0E0E0",
            "font_color": "#000000"  # Black text for Light theme
        },
        "Blue": {
            "bg": "#0F1B4C",
            "fg": "#E0E0E0",
            "accent": "#58A6FF",
            "button_bg": "#27496D",
            "font_color": "#E0E0E0"
        }
    }

    return themes[theme_name]
