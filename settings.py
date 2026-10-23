# ============================================================
# SETTINGS.PY
# AI SQL STUDIO - CONTROL CENTER
# ============================================================

import tkinter as tk
from tkinter import messagebox
import sqlite3
import importlib.util
import urllib.request
import json


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
CARD_COLOR = "#1C2433"
INPUT_COLOR = "#252D3D"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#AAB2C0"

ACCENT_COLOR = "#6C63E8"
HOVER_COLOR = "#7A72F5"

SUCCESS_COLOR = "#35D07F"
DANGER_COLOR = "#FF5C6C"
WARNING_COLOR = "#FFD166"


# ============================================================
# SETTINGS
# ============================================================

class Settings:

    def __init__(self, parent):

        self.parent = parent

        self.dark_mode = True
        self.auto_validate = True
        self.confirm_delete = True

        self.notifications = True
        self.compact_results = False
        self.response_style = "Balanced"
        self.auto_refresh = False
        self.read_only = True

        self.create_ui()


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        self.frame = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        self.frame.pack(
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.frame,
            bg=BG_COLOR
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(28, 15)
        )

        tk.Label(
            header,
            text="Control Center",
            font=("Segoe UI", 27, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Configure how AI SQL Studio thinks, looks and protects your data.",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # ----------------------------------------------------
        # MAIN CONTENT
        # ----------------------------------------------------

        main = tk.Frame(
            self.frame,
            bg=BG_COLOR
        )

        main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )


        # ====================================================
        # LEFT SCROLLABLE PANEL
        # ====================================================

        left_container = tk.Frame(
            main,
            bg=BG_COLOR
        )

        left_container.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )


        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------

        left_canvas = tk.Canvas(
            left_container,
            bg=BG_COLOR,
            highlightthickness=0,
            bd=0
        )

        left_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # SCROLLBAR
        # ----------------------------------------------------

        left_scrollbar = tk.Scrollbar(
            left_container,
            orient="vertical",
            command=left_canvas.yview,
            bg=INPUT_COLOR,
            troughcolor=BG_COLOR,
            activebackground=ACCENT_COLOR,
            width=8
        )

        left_scrollbar.pack(
            side="right",
            fill="y"
        )

        left_canvas.configure(
            yscrollcommand=left_scrollbar.set
        )


        # ----------------------------------------------------
        # ACTUAL LEFT CONTENT
        # ----------------------------------------------------

        left = tk.Frame(
            left_canvas,
            bg=BG_COLOR
        )

        left_window = left_canvas.create_window(
            (0, 0),
            window=left,
            anchor="nw"
        )


        # ----------------------------------------------------
        # UPDATE SCROLL REGION
        # ----------------------------------------------------

        def update_scroll_region(event=None):

            left_canvas.configure(
                scrollregion=left_canvas.bbox("all")
            )

        left.bind(
            "<Configure>",
            update_scroll_region
        )


        # ----------------------------------------------------
        # KEEP CONTENT WIDTH EQUAL TO CANVAS
        # ----------------------------------------------------

        def resize_left_content(event):

            left_canvas.itemconfig(
                left_window,
                width=event.width
            )

        left_canvas.bind(
            "<Configure>",
            resize_left_content
        )


        # ----------------------------------------------------
        # MOUSE WHEEL
        # ----------------------------------------------------

        def mousewheel(event):

            left_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        left_canvas.bind_all(
            "<MouseWheel>",
            mousewheel
        )


        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right = tk.Frame(
            main,
            bg=BG_COLOR,
            width=310
        )

        right.pack(
            side="right",
            fill="y",
            padx=(12, 0)
        )

        right.pack_propagate(False)


        # ====================================================
        # CREATE CARDS
        # ====================================================

        self.create_ai_card(left)

        self.create_workspace_card(left)

        self.create_safety_card(left)

        self.create_health_card(right)

        self.create_actions_card(right)


    # ========================================================
    # CARD HELPER
    # ========================================================

    def card_title(self, parent, icon, title, subtitle):

        tk.Label(
            parent,
            text=f"{icon}  {title}",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 2)
        )

        tk.Label(
            parent,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 12)
        )


    # ========================================================
    # AI BRAIN
    # ========================================================

    def create_ai_card(self, parent):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        card.pack(
            fill="x",
            pady=(0, 15)
        )

        self.card_title(
            card,
            "🤖",
            "AI Brain",
            "Control the intelligence behind SQL generation."
        )


        # AI MODEL

        row = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        row.pack(
            fill="x",
            padx=22,
            pady=5
        )

        tk.Label(
            row,
            text="AI Model",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            side="left"
        )

        self.model_var = tk.StringVar(
            value="Default"
        )

        menu = tk.OptionMenu(
            row,
            self.model_var,
            "Default",
            "GPT",
            "Local Model"
        )

        menu.config(
            font=("Segoe UI", 9),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            width=15
        )

        menu["menu"].config(
            bg=INPUT_COLOR,
            fg=TEXT_COLOR
        )

        menu.pack(
            side="right"
        )


        # RESPONSE STYLE

        row2 = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        row2.pack(
            fill="x",
            padx=22,
            pady=(5, 18)
        )

        tk.Label(
            row2,
            text="Response Style",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            side="left"
        )

        self.response_var = tk.StringVar(
            value="Balanced"
        )

        style_menu = tk.OptionMenu(
            row2,
            self.response_var,
            "Fast",
            "Balanced",
            "Detailed"
        )

        style_menu.config(
            font=("Segoe UI", 9),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            width=15
        )

        style_menu["menu"].config(
            bg=INPUT_COLOR,
            fg=TEXT_COLOR
        )

        style_menu.pack(
            side="right"
        )


    # ========================================================
    # WORKSPACE
    # ========================================================

    def create_workspace_card(self, parent):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        card.pack(
            fill="x",
            pady=(0, 15)
        )

        self.card_title(
            card,
            "🎨",
            "Workspace",
            "Choose how your analysis workspace behaves."
        )


        self.dark_var = tk.BooleanVar(
            value=True
        )

        self.notifications_var = tk.BooleanVar(
            value=True
        )

        self.compact_var = tk.BooleanVar(
            value=False
        )

        self.refresh_var = tk.BooleanVar(
            value=False
        )


        self.create_switch(
            card,
            "Dark Mode",
            self.dark_var
        )

        self.create_switch(
            card,
            "Helpful Notifications",
            self.notifications_var
        )

        self.create_switch(
            card,
            "Compact Result Tables",
            self.compact_var
        )

        self.create_switch(
            card,
            "Auto Refresh",
            self.refresh_var,
            bottom=True
        )


    # ========================================================
    # SAFETY
    # ========================================================

    def create_safety_card(self, parent):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        card.pack(
            fill="x",
            pady=(0, 10)
        )

        self.card_title(
            card,
            "🛡",
            "Safety",
            "Extra protection for database operations."
        )


        self.validate_var = tk.BooleanVar(
            value=True
        )

        self.delete_var = tk.BooleanVar(
            value=True
        )

        self.read_only_var = tk.BooleanVar(
            value=True
        )


        self.create_switch(
            card,
            "Automatically Validate SQL",
            self.validate_var
        )

        self.create_switch(
            card,
            "Confirm Before Deleting",
            self.delete_var
        )

        self.create_switch(
            card,
            "Read-Only SQL Protection",
            self.read_only_var,
            bottom=True
        )


    # ========================================================
    # SWITCH
    # ========================================================

    def create_switch(
        self,
        parent,
        text,
        variable,
        bottom=False
    ):

        row = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        row.pack(
            fill="x",
            padx=22,
            pady=(
                3,
                18 if bottom else 5
            )
        )


        tk.Label(
            row,
            text=text,
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left"
        )


        switch = tk.Checkbutton(
            row,
            variable=variable,
            onvalue=True,
            offvalue=False,
            text="ON",
            font=("Segoe UI", 8, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            selectcolor=ACCENT_COLOR,
            indicatoron=False,
            width=6,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        switch.pack(
            side="right"
        )


    # ========================================================
    # WORKSPACE HEALTH
    # ========================================================

    def create_health_card(self, parent):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        card.pack(
            fill="x",
            pady=(0, 15)
        )

        self.card_title(
            card,
            "⚡",
            "Workspace Health",
            "Live component check."
        )


        self.health_percent = tk.StringVar(
            value="READY"
        )


        tk.Label(
            card,
            textvariable=self.health_percent,
            font=("Segoe UI", 24, "bold"),
            bg=CARD_COLOR,
            fg=SUCCESS_COLOR
        ).pack(
            pady=(3, 15)
        )


        self.health_labels = {}


        self.create_health_row(
            card,
            "Python",
            "python"
        )

        self.create_health_row(
            card,
            "SQLite",
            "sqlite3"
        )

        self.create_health_row(
            card,
            "Matplotlib",
            "matplotlib"
        )

        self.create_health_row(
            card,
            "Pandas",
            "pandas"
        )

        self.create_health_row(
            card,
            "Ollama",
            "ollama"
        )


    # ========================================================
    # HEALTH ROW
    # ========================================================

    def create_health_row(
        self,
        parent,
        name,
        key
    ):

        row = tk.Frame(
            parent,
            bg=INPUT_COLOR
        )

        row.pack(
            fill="x",
            padx=18,
            pady=3
        )


        tk.Label(
            row,
            text=name,
            font=("Segoe UI", 9),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=10,
            pady=7
        )


        status = tk.Label(
            row,
            text="●",
            font=("Segoe UI", 10, "bold"),
            bg=INPUT_COLOR,
            fg=SECONDARY_TEXT
        )

        status.pack(
            side="right",
            padx=10
        )


        self.health_labels[key] = status


    # ========================================================
    # ACTIONS
    # ========================================================

    def create_actions_card(self, parent):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        card.pack(
            fill="x"
        )

        self.card_title(
            card,
            "⚙",
            "Quick Actions",
            "Apply or restore your workspace configuration."
        )


        tk.Button(
            card,
            text="⚡  RUN SYSTEM CHECK",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.run_system_check
        ).pack(
            fill="x",
            padx=22,
            pady=6,
            ipady=9
        )


        tk.Button(
            card,
            text="✓  SAVE CONFIGURATION",
            font=("Segoe UI", 9, "bold"),
            bg=SUCCESS_COLOR,
            fg="#101522",
            activebackground=SUCCESS_COLOR,
            activeforeground="#101522",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.save_settings
        ).pack(
            fill="x",
            padx=22,
            pady=6,
            ipady=9
        )


        tk.Button(
            card,
            text="↻  RESET DEFAULTS",
            font=("Segoe UI", 9, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.reset_defaults
        ).pack(
            fill="x",
            padx=22,
            pady=(6, 20),
            ipady=8
        )


    # ========================================================
    # SYSTEM CHECK
    # ========================================================

    def run_system_check(self):

        checks = {}

        checks["python"] = True


        try:

            sqlite3.connect(
                ":memory:"
            ).close()

            checks["sqlite3"] = True

        except Exception:

            checks["sqlite3"] = False


        for package in (
            "matplotlib",
            "pandas"
        ):

            checks[package] = (
                importlib.util.find_spec(package)
                is not None
            )


        checks["ollama"] = self.check_ollama()


        ready_count = 0


        for key, status in checks.items():

            if status:

                ready_count += 1

                self.health_labels[key].config(
                    fg=SUCCESS_COLOR
                )

            else:

                self.health_labels[key].config(
                    fg=DANGER_COLOR
                )


        percentage = int(
            (ready_count / len(checks)) * 100
        )


        if percentage == 100:

            self.health_percent.set(
                "100% READY"
            )

            messagebox.showinfo(
                "System Check",
                "All AI SQL Studio components are ready."
            )

        else:

            self.health_percent.set(
                f"{percentage}% READY"
            )

            messagebox.showwarning(
                "System Check",
                f"Workspace check completed.\n\n"
                f"{ready_count}/{len(checks)} components are ready."
            )


    # ========================================================
    # OLLAMA CHECK
    # ========================================================

    def check_ollama(self):

        try:

            request = urllib.request.Request(
                "http://localhost:11434/api/tags",
                method="GET"
            )


            with urllib.request.urlopen(
                request,
                timeout=1.5
            ) as response:

                return response.status == 200


        except Exception:

            return False


    # ========================================================
    # RESET
    # ========================================================

    def reset_defaults(self):

        self.dark_var.set(True)

        self.validate_var.set(True)

        self.delete_var.set(True)

        self.read_only_var.set(True)


        self.notifications_var.set(True)

        self.compact_var.set(False)

        self.refresh_var.set(False)


        self.model_var.set(
            "Default"
        )

        self.response_var.set(
            "Balanced"
        )


        self.health_percent.set(
            "READY"
        )


        for status in self.health_labels.values():

            status.config(
                fg=SECONDARY_TEXT
            )


        self.dark_mode = True

        self.auto_validate = True

        self.confirm_delete = True

        self.notifications = True

        self.compact_results = False

        self.auto_refresh = False

        self.read_only = True

        self.response_style = "Balanced"


        messagebox.showinfo(
            "Defaults Restored",
            "AI SQL Studio has been restored to its default configuration."
        )


    # ========================================================
    # SAVE
    # ========================================================

    def save_settings(self):

        self.dark_mode = (
            self.dark_var.get()
        )

        self.auto_validate = (
            self.validate_var.get()
        )

        self.confirm_delete = (
            self.delete_var.get()
        )

        self.notifications = (
            self.notifications_var.get()
        )

        self.compact_results = (
            self.compact_var.get()
        )

        self.auto_refresh = (
            self.refresh_var.get()
        )

        self.read_only = (
            self.read_only_var.get()
        )

        self.response_style = (
            self.response_var.get()
        )


        messagebox.showinfo(
            "Configuration Saved",
            "Your AI SQL Studio configuration has been saved for this session."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "AI SQL Studio - Control Center"
    )

    root.geometry(
        "1200x760"
    )

    root.minsize(
        1000,
        680
    )

    root.configure(
        bg=BG_COLOR
    )


    Settings(root)


    root.mainloop()