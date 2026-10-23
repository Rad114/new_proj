# ============================================================
# REGISTER.PY
# AI SQL STUDIO
# ============================================================

import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

import urllib.request
from io import BytesIO

from database import register_user


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
CARD_COLOR = "#1C2433"
INPUT_COLOR = "#252D3D"

ACCENT_COLOR = "#6C63E8"
ACCENT_HOVER = "#7A72F5"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#AAB2C0"


# ============================================================
# IMAGE URL
# ============================================================

IMAGE_URL = (
    "https://encrypted-tbn0.gstatic.com/"
    "images?q=tbn%3AANd9GcRSivwrICcSPdmoXDHxGlPvX9g9oI3nRuZvmvCOlbN_ig"
    "&s=10"
)


# ============================================================
# REGISTER WINDOW
# ============================================================

class RegisterWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI SQL Studio - Register"
        )

        self.root.geometry(
            "1200x750"
        )

        self.root.minsize(
            900,
            650
        )

        self.root.configure(
            bg=BG_COLOR
        )

        self.create_ui()


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        # ====================================================
        # MAIN CONTAINER
        # ====================================================

        main = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        main.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # LEFT SIDE
        # ====================================================

        left = tk.Frame(
            main,
            bg="#171D2B",
            width=500
        )

        left.pack(
            side="left",
            fill="both"
        )

        left.pack_propagate(False)


        # ====================================================
        # LEFT CANVAS
        # ====================================================

        canvas = tk.Canvas(
            left,
            bg="#171D2B",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # PROJECT TITLE
        # ====================================================

        canvas.create_text(
            250,
            55,
            text="AI SQL STUDIO",
            font=("Segoe UI", 28, "bold"),
            fill=TEXT_COLOR
        )


        # ====================================================
        # ACCENT LINE
        # ====================================================

        canvas.create_line(
            165,
            82,
            335,
            82,
            fill=ACCENT_COLOR,
            width=3
        )


        # ====================================================
        # PROJECT SUBTITLE
        # ====================================================

        canvas.create_text(
            250,
            105,
            text="Smart SQL • Simple Answers",
            font=("Segoe UI", 10, "italic"),
            fill=SECONDARY_TEXT
        )


        # ====================================================
        # IMAGE FROM URL
        # ====================================================

        try:

            print("Loading SQL Agent image...")

            request = urllib.request.Request(
                IMAGE_URL,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=15
            ) as response:

                image_data = response.read()


            # =================================================
            # OPEN IMAGE
            # =================================================

            original_image = Image.open(
                BytesIO(image_data)
            ).convert("RGBA")


            # =================================================
            # IMAGE SIZE
            # =================================================

            max_width = 430
            max_height = 500

            img_width, img_height = original_image.size


            # =================================================
            # MAINTAIN ASPECT RATIO
            # =================================================

            ratio = min(
                max_width / img_width,
                max_height / img_height
            )


            new_width = int(
                img_width * ratio
            )

            new_height = int(
                img_height * ratio
            )


            # =================================================
            # RESIZE
            # =================================================

            resized_image = original_image.resize(
                (
                    new_width,
                    new_height
                ),
                Image.Resampling.LANCZOS
            )


            # =================================================
            # TKINTER IMAGE
            # =================================================

            self.register_image = ImageTk.PhotoImage(
                resized_image
            )


            # =================================================
            # DISPLAY IMAGE
            # =================================================

            canvas.create_image(
                250,
                350,
                image=self.register_image,
                anchor="center"
            )


            print(
                "SQL Agent image loaded successfully."
            )


        except Exception as error:

            print(
                "Image loading error:",
                error
            )

            # =================================================
            # FALLBACK GRAPHIC
            # =================================================

            canvas.create_oval(
                150,
                220,
                350,
                420,
                fill="#252D3D",
                outline=ACCENT_COLOR,
                width=3
            )

            canvas.create_text(
                250,
                300,
                text="SQL",
                font=("Segoe UI", 40, "bold"),
                fill=ACCENT_COLOR
            )

            canvas.create_text(
                250,
                355,
                text="AGENT",
                font=("Segoe UI", 18, "bold"),
                fill=TEXT_COLOR
            )

            canvas.create_text(
                250,
                400,
                text="Image could not be loaded",
                font=("Segoe UI", 9),
                fill=SECONDARY_TEXT
            )


        # ====================================================
        # LEFT BOTTOM TEXT
        # ====================================================

        canvas.create_text(
            250,
            650,
            text="Create • Query • Analyze",
            font=("Segoe UI", 12, "bold"),
            fill=TEXT_COLOR
        )


        canvas.create_text(
            250,
            680,
            text="Your intelligent SQL workspace",
            font=("Segoe UI", 9),
            fill=SECONDARY_TEXT
        )


        # ====================================================
        # RIGHT SIDE
        # ====================================================

        right = tk.Frame(
            main,
            bg=BG_COLOR
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )


        # ====================================================
        # REGISTER CARD
        # ====================================================

        card = tk.Frame(
            right,
            bg=CARD_COLOR,
            width=500,
            height=600
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)


        # ====================================================
        # HEADING
        # ====================================================

        heading = tk.Label(
            card,
            text="Create Account",
            font=("Segoe UI", 26, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        heading.pack(
            pady=(30, 5)
        )


        # ====================================================
        # SUBTITLE
        # ====================================================

        subtitle = tk.Label(
            card,
            text="Join AI SQL Studio",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        subtitle.pack(
            pady=(0, 25)
        )


        # ====================================================
        # FULL NAME
        # ====================================================

        name_label = tk.Label(
            card,
            text="Full Name",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        name_label.pack(
            anchor="w",
            padx=50
        )


        self.name_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            bd=0
        )

        self.name_entry.pack(
            fill="x",
            padx=50,
            pady=(6, 15),
            ipady=10
        )


        # ====================================================
        # EMAIL
        # ====================================================

        email_label = tk.Label(
            card,
            text="Email Address",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        email_label.pack(
            anchor="w",
            padx=50
        )


        self.email_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            bd=0
        )

        self.email_entry.pack(
            fill="x",
            padx=50,
            pady=(6, 15),
            ipady=10
        )


        # ====================================================
        # PASSWORD
        # ====================================================

        password_label = tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        password_label.pack(
            anchor="w",
            padx=50
        )


        self.password_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            bd=0,
            show="●"
        )

        self.password_entry.pack(
            fill="x",
            padx=50,
            pady=(6, 20),
            ipady=10
        )


        # ====================================================
        # CREATE ACCOUNT BUTTON
        # ====================================================

        register_button = tk.Button(
            card,
            text="Create Account",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.register
        )

        register_button.pack(
            fill="x",
            padx=50,
            ipady=10
        )


        # ====================================================
        # SIGN IN SECTION
        # ====================================================

        signin_frame = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        signin_frame.pack(
            pady=(25, 5)
        )


        signin_text = tk.Label(
            signin_frame,
            text="Already have an account?",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        signin_text.pack(
            side="left"
        )


        signin_button = tk.Button(
            signin_frame,
            text=" Sign In",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR,
            activebackground=CARD_COLOR,
            activeforeground=ACCENT_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.open_login
        )

        signin_button.pack(
            side="left"
        )


        # ====================================================
        # FOCUS
        # ====================================================

        self.name_entry.focus_set()


    # ========================================================
    # REGISTER FUNCTION
    # ========================================================

    def register(self):

        name = self.name_entry.get().strip()

        email = self.email_entry.get().strip()

        password = self.password_entry.get()


        # ====================================================
        # NAME VALIDATION
        # ====================================================

        if not name:

            messagebox.showwarning(
                "Missing Name",
                "Please enter your full name."
            )

            return


        # ====================================================
        # EMAIL VALIDATION
        # ====================================================

        if not email:

            messagebox.showwarning(
                "Missing Email",
                "Please enter your email address."
            )

            return


        # ====================================================
        # PASSWORD VALIDATION
        # ====================================================

        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please create a password."
            )

            return


        # ====================================================
        # PASSWORD LENGTH
        # ====================================================

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )

            return


        # ====================================================
        # DATABASE
        # ====================================================

        try:

            success, message = register_user(
                name,
                email,
                password
            )


            # =================================================
            # SUCCESS
            # =================================================

            if success:

                messagebox.showinfo(
                    "Registration Successful",
                    "Your account has been created successfully.\n\n"
                    "You can now Sign In."
                )

                self.open_login()


            # =================================================
            # FAILED
            # =================================================

            else:

                messagebox.showerror(
                    "Registration Failed",
                    message
                )


        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )


    # ========================================================
    # OPEN LOGIN
    # ========================================================

    def open_login(self):

        self.root.destroy()

        import login

        login.start_login()


# ============================================================
# START REGISTER
# ============================================================

def start_register():

    root = tk.Tk()

    RegisterWindow(
        root
    )

    root.mainloop()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    start_register() 