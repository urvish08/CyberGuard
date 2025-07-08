# settings.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os


class SettingsPage:
    def __init__(self, root, parent_frame, controller=None):
        self.root = root
        self.parent_frame = parent_frame
        self.controller = controller
        self.settings_file = "settings_config.json"
        self.theme_file = "theme_config.json"
        self.themes = {
            "Dark": {
                "bg": "#0D1117",
                "fg": "#C9D1D9",
                "accent": "#58A6FF",
                "button_bg": "#1F6FEB"
            },
            "Light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "accent": "#0078D4",
                "button_bg": "#E0E0E0"
            },
            "Blue": {
                "bg": "#0F1B4C",
                "fg": "#E0E0E0",
                "accent": "#58A6FF",
                "button_bg": "#27496D"
            }
        }
        self.settings_data = {
            "sound_alerts": True,
            "auto_save_logs": True,
            "scan_timeout": 30,
            "theme": "Dark"
        }
        self.load_settings()
        self.apply_theme()
        self.create_settings_ui()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                self.settings_data = json.load(f)

    def save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings_data, f, indent=4)

    def save_theme_globally(self):
        with open(self.theme_file, "w") as f:
            json.dump({"theme": self.settings_data["theme"]}, f)

    def apply_theme(self):
        theme = self.themes[self.settings_data["theme"]]
        self.bg_color = theme["bg"]
        self.fg_color = theme["fg"]
        self.accent_color = theme["accent"]
        self.button_color = theme["button_bg"]

    def clear_frame(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_settings_ui(self):
        self.clear_frame()
        settings_frame = tk.Frame(self.parent_frame, bg=self.bg_color)
        settings_frame.pack(fill="both", expand=True)

        # Header
        tk.Label(settings_frame, text="⚙️ Settings", font=("Segoe UI", 20, "bold"),
                 fg=self.accent_color, bg=self.bg_color).pack(pady=10)

        form_frame = tk.Frame(settings_frame, bg=self.bg_color)
        form_frame.pack(pady=10)

        # Theme selection
        tk.Label(form_frame, text="Theme:", font=("Segoe UI", 13, "bold"),
                 fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.theme_var = tk.StringVar(value=self.settings_data["theme"])
        theme_menu = ttk.Combobox(form_frame, textvariable=self.theme_var, values=list(self.themes.keys()),
                                  state="readonly", width=30)
        theme_menu.grid(row=0, column=1, padx=10, pady=5)

        # Sound Alerts
        self.sound_var = tk.BooleanVar(value=self.settings_data["sound_alerts"])
        tk.Checkbutton(form_frame, text="Enable Sound Alerts", variable=self.sound_var,
                       font=("Segoe UI", 12), bg=self.bg_color, fg=self.fg_color,
                       selectcolor=self.bg_color, activebackground=self.bg_color).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Auto Save Logs
        self.logs_var = tk.BooleanVar(value=self.settings_data["auto_save_logs"])
        tk.Checkbutton(form_frame, text="Auto-save Scan Logs", variable=self.logs_var,
                       font=("Segoe UI", 12), bg=self.bg_color, fg=self.fg_color,
                       selectcolor=self.bg_color, activebackground=self.bg_color).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Scan timeout
        tk.Label(form_frame, text="Scan Timeout (seconds):", font=("Segoe UI", 13),
                 fg=self.fg_color, bg=self.bg_color).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.timeout_entry = ttk.Entry(form_frame, width=33)
        self.timeout_entry.insert(0, self.settings_data["scan_timeout"])
        self.timeout_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(settings_frame, bg=self.bg_color)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="💾 Save Settings", command=self.save_all).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="♻️ Reset to Default", command=self.reset_defaults).grid(row=0, column=1, padx=10)

        # Info area
        info_frame = tk.LabelFrame(settings_frame, text="ℹ️ About", font=("Segoe UI", 12, "bold"),
                                   bg=self.bg_color, fg=self.fg_color, labelanchor="n", bd=2)
        info_frame.pack(padx=20, pady=10, fill="x")
        tk.Label(info_frame, text="CyberGuard - Web Security Scanner", font=("Segoe UI", 11),
                 bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=10, pady=2)
        tk.Label(info_frame, text="Version: 1.0.0", font=("Segoe UI", 11),
                 bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=10, pady=2)
        tk.Label(info_frame, text="License: MIT Open Source", font=("Segoe UI", 11),
                 bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=10, pady=2)

        # Home Button
        if self.controller:
            ttk.Button(settings_frame, text="🏠 Back to Home", command=lambda: self.controller.show_frame("home")).pack(pady=10)

    def save_all(self):
        try:
            timeout_val = int(self.timeout_entry.get())
            self.settings_data.update({
                "theme": self.theme_var.get(),
                "sound_alerts": self.sound_var.get(),
                "auto_save_logs": self.logs_var.get(),
                "scan_timeout": timeout_val
            })
            self.save_settings()
            self.save_theme_globally()
            messagebox.showinfo("Settings", "Settings saved successfully! Restart tool to apply theme everywhere.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for timeout.")

    def reset_defaults(self):
        confirm = messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings?")
        if confirm:
            self.settings_data = {
                "sound_alerts": True,
                "auto_save_logs": True,
                "scan_timeout": 30,
                "theme": "Dark"
            }
            self.save_settings()
            self.save_theme_globally()
            self.create_settings_ui()
            messagebox.showinfo("Reset", "Settings have been reset to default.")


# This class is integrated in the main home.py controller using: settings.SettingsPage(...)
