# ============================================================
# ACCOUNT.PY
# ============================================================

import tkinter as tk
from tkinter import messagebox
import sqlite3


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


# ============================================================
# ACCOUNT CLASS
# ============================================================

class Account:

    # IMPORTANT:
    # Only parent is required.
    # This matches:
    # Account(self.content)

    def __init__(self, parent):

        self.parent = parent

        self.create_ui()


    # ========================================================
    # MAIN UI
    # ========================================================

    def create_ui(self):

        # ----------------------------------------------------
        # OUTER FRAME
        # ----------------------------------------------------

        outer_frame = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        outer_frame.pack(
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            outer_frame,
            bg=BG_COLOR,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # SCROLLBAR
        # ----------------------------------------------------

        scrollbar = tk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )


        # ----------------------------------------------------
        # INNER FRAME
        # ----------------------------------------------------

        self.inner_frame = tk.Frame(
            self.canvas,
            bg=BG_COLOR
        )


        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.inner_frame,
            anchor="nw"
        )


        # Update scroll region

        self.inner_frame.bind(
            "<Configure>",
            self.update_scroll
        )


        # Resize inner frame

        self.canvas.bind(
            "<Configure>",
            self.resize_inner
        )


        # Mouse wheel

        self.canvas.bind(
            "<Enter>",
            self.enable_mousewheel
        )

        self.canvas.bind(
            "<Leave>",
            self.disable_mousewheel
        )


        # Create account page

        self.create_account_page()


    # ========================================================
    # UPDATE SCROLL
    # ========================================================

    def update_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    # ========================================================
    # RESIZE INNER FRAME
    # ========================================================

    def resize_inner(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    # ========================================================
    # ENABLE MOUSE WHEEL
    # ========================================================

    def enable_mousewheel(self, event):

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mousewheel
        )


    # ========================================================
    # DISABLE MOUSE WHEEL
    # ========================================================

    def disable_mousewheel(self, event):

        self.canvas.unbind_all(
            "<MouseWheel>"
        )


    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # ========================================================
    # ACCOUNT PAGE
    # ========================================================

    def create_account_page(self):

        # ====================================================
        # HEADER
        # ====================================================

        title = tk.Label(
            self.inner_frame,
            text="My Account",
            font=("Segoe UI", 27, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )


        subtitle = tk.Label(
            self.inner_frame,
            text="Manage your account and security settings.",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(0, 25)
        )


        # ====================================================
        # PROFILE CARD
        # ====================================================

        profile_card = tk.Frame(
            self.inner_frame,
            bg=CARD_COLOR
        )

        profile_card.pack(
            fill="x",
            padx=35,
            pady=10
        )


        profile_title = tk.Label(
            profile_card,
            text="Profile",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        profile_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )


        username_label = tk.Label(
            profile_card,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        username_label.pack(
            anchor="w",
            padx=25
        )


        # ----------------------------------------------------
        # Username
        # ----------------------------------------------------

        self.username_entry = tk.Entry(
            profile_card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat"
        )

        self.username_entry.pack(
            fill="x",
            padx=25,
            pady=(7, 25),
            ipady=8
        )


        # ====================================================
        # CHANGE PASSWORD CARD
        # ====================================================

        password_card = tk.Frame(
            self.inner_frame,
            bg=CARD_COLOR
        )

        password_card.pack(
            fill="x",
            padx=35,
            pady=10
        )


        password_title = tk.Label(
            password_card,
            text="Change Password",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        password_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )


        password_subtitle = tk.Label(
            password_card,
            text="Enter your current password and choose a new password.",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        password_subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )


        # ====================================================
        # CURRENT PASSWORD
        # ====================================================

        current_label = tk.Label(
            password_card,
            text="Current Password",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        current_label.pack(
            anchor="w",
            padx=25
        )


        self.current_password = tk.Entry(
            password_card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            show="*"
        )

        self.current_password.pack(
            fill="x",
            padx=25,
            pady=(7, 15),
            ipady=8
        )


        # ====================================================
        # NEW PASSWORD
        # ====================================================

        new_label = tk.Label(
            password_card,
            text="New Password",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        new_label.pack(
            anchor="w",
            padx=25
        )


        self.new_password = tk.Entry(
            password_card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            show="*"
        )

        self.new_password.pack(
            fill="x",
            padx=25,
            pady=(7, 15),
            ipady=8
        )


        # ====================================================
        # CONFIRM PASSWORD
        # ====================================================

        confirm_label = tk.Label(
            password_card,
            text="Confirm New Password",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        confirm_label.pack(
            anchor="w",
            padx=25
        )


        self.confirm_password = tk.Entry(
            password_card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            show="*"
        )

        self.confirm_password.pack(
            fill="x",
            padx=25,
            pady=(7, 20),
            ipady=8
        )


        # ====================================================
        # CHANGE PASSWORD BUTTON
        # ====================================================

        change_button = tk.Button(
            password_card,
            text="Change Password",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground=HOVER_COLOR,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.change_password
        )

        change_button.pack(
            anchor="w",
            padx=25,
            pady=(0, 25),
            ipadx=20,
            ipady=8
        )


        # ====================================================
        # SECURITY CARD
        # ====================================================

        security_card = tk.Frame(
            self.inner_frame,
            bg=CARD_COLOR
        )

        security_card.pack(
            fill="x",
            padx=35,
            pady=10
        )


        security_title = tk.Label(
            security_card,
            text="Security",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        security_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )


        security_text = tk.Label(
            security_card,
            text=(
                "Keep your password secure.\n\n"
                "Use a strong password containing letters, "
                "numbers and special characters."
            ),
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            justify="left"
        )

        security_text.pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )


    # ========================================================
    # CHANGE PASSWORD
    # ========================================================

    def change_password(self):

        current_password = (
            self.current_password
            .get()
            .strip()
        )

        new_password = (
            self.new_password
            .get()
            .strip()
        )

        confirm_password = (
            self.confirm_password
            .get()
            .strip()
        )


        # ====================================================
        # VALIDATION
        # ====================================================

        if current_password == "":

            messagebox.showwarning(
                "Warning",
                "Please enter your current password."
            )

            return


        if new_password == "":

            messagebox.showwarning(
                "Warning",
                "Please enter a new password."
            )

            return


        if confirm_password == "":

            messagebox.showwarning(
                "Warning",
                "Please confirm your new password."
            )

            return


        if len(new_password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )

            return


        if new_password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "New passwords do not match."
            )

            return


        if current_password == new_password:

            messagebox.showwarning(
                "Warning",
                "New password must be different from current password."
            )

            return


        # ====================================================
        # DATABASE
        # ====================================================

        try:

            connection = sqlite3.connect(
                "users.db"
            )

            cursor = connection.cursor()


            # ------------------------------------------------
            # Find user
            # ------------------------------------------------

            username = (
                self.username_entry
                .get()
                .strip()
            )


            if username == "":

                connection.close()

                messagebox.showwarning(
                    "Warning",
                    "Username cannot be empty."
                )

                return


            cursor.execute(
                """
                SELECT password
                FROM users
                WHERE username = ?
                """,
                (username,)
            )


            result = cursor.fetchone()


            if result is None:

                connection.close()

                messagebox.showerror(
                    "Error",
                    "User account was not found."
                )

                return


            stored_password = result[0]


            # ------------------------------------------------
            # Verify current password
            # ------------------------------------------------

            if stored_password != current_password:

                connection.close()

                messagebox.showerror(
                    "Incorrect Password",
                    "Current password is incorrect."
                )

                return


            # ------------------------------------------------
            # Update password
            # ------------------------------------------------

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE username = ?
                """,
                (
                    new_password,
                    username
                )
            )


            connection.commit()

            connection.close()


            # ------------------------------------------------
            # Clear fields
            # ------------------------------------------------

            self.current_password.delete(
                0,
                tk.END
            )

            self.new_password.delete(
                0,
                tk.END
            )

            self.confirm_password.delete(
                0,
                tk.END
            )


            messagebox.showinfo(
                "Success",
                "Password changed successfully."
            )


        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Database error:\n{error}"
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "My Account"
    )

    root.geometry(
        "1100x750"
    )

    root.minsize(
        800,
        600
    )

    root.configure(
        bg=BG_COLOR
    )


    Account(
        root
    )


    root.mainloop()