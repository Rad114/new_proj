import tkinter as tk
from tkinter import messagebox
import math
import random

from database import login_user


# ============================================================
# COLORS
# ============================================================

BG = "#0F1420"
WALL = "#202735"
CARD = "#1B2130"
INPUT = "#252D3D"

WHITE = "#FFFFFF"
GRAY = "#AAB2C0"

PURPLE = "#6C63E8"
PURPLE_HOVER = "#7A72F5"

PAINT = [
    "#FF4D6D",
    "#FFD166",
    "#06D6A0",
    "#4D96FF",
    "#9B5DE5",
    "#FF7B00"
]


# ============================================================
# LOGIN WINDOW
# ============================================================

class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("AI SQL Studio")

        self.root.geometry("1200x750")

        self.root.minsize(900, 650)

        self.root.configure(bg=BG)

        self.canvas = None

        self.frame = 0

        # Start animation
        self.start_animation()


    # ========================================================
    # START ANIMATION
    # ========================================================

    def start_animation(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(
            self.root,
            bg=WALL,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.frame = 0

        self.draw_background()

        self.animate()


    # ========================================================
    # BACKGROUND
    # ========================================================

    def draw_background(self):

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        if w < 500:
            w = 1200

        if h < 400:
            h = 750

        # Wall
        self.canvas.create_rectangle(
            0,
            0,
            w,
            h,
            fill=WALL,
            outline=""
        )

        # Vertical wall lines
        for x in range(0, w, 150):

            self.canvas.create_line(
                x,
                0,
                x,
                h,
                fill="#252D3B",
                width=1
            )

        # Horizontal wall lines
        for y in range(0, h, 100):

            self.canvas.create_line(
                0,
                y,
                w,
                y,
                fill="#252D3B",
                width=1
            )

        # Floor
        self.canvas.create_rectangle(
            0,
            h - 90,
            w,
            h,
            fill="#151A25",
            outline=""
        )

        # Title
        self.canvas.create_text(
            w // 2,
            65,
            text="AI SQL STUDIO",
            font=("Segoe UI", 28, "bold"),
            fill=WHITE
        )

        self.canvas.create_text(
            w // 2,
            105,
            text="INTELLIGENCE • DATABASE • SQL",
            font=("Segoe UI", 10),
            fill=GRAY
        )


    # ========================================================
    # DRAW BOY
    # ========================================================

    def draw_boy(self, x, y, arm_angle):

        self.canvas.delete("boy")

        # Shadow
        self.canvas.create_oval(
            x - 65,
            y + 75,
            x + 65,
            y + 95,
            fill="#11151D",
            outline="",
            tags="boy"
        )

        # Left leg
        self.canvas.create_line(
            x - 12,
            y + 10,
            x - 35,
            y + 80,
            fill="#171717",
            width=14,
            capstyle=tk.ROUND,
            tags="boy"
        )

        # Right leg
        self.canvas.create_line(
            x + 12,
            y + 10,
            x + 40,
            y + 80,
            fill="#171717",
            width=14,
            capstyle=tk.ROUND,
            tags="boy"
        )

        # Shoes
        self.canvas.create_oval(
            x - 52,
            y + 72,
            x - 20,
            y + 88,
            fill="#080808",
            outline="",
            tags="boy"
        )

        self.canvas.create_oval(
            x + 25,
            y + 72,
            x + 57,
            y + 88,
            fill="#080808",
            outline="",
            tags="boy"
        )

        # Body
        self.canvas.create_polygon(
            x - 32,
            y - 80,
            x + 32,
            y - 80,
            x + 40,
            y + 15,
            x - 40,
            y + 15,
            fill="#4D96FF",
            outline="",
            tags="boy"
        )

        # Neck
        self.canvas.create_rectangle(
            x - 10,
            y - 92,
            x + 10,
            y - 75,
            fill="#F2C7A5",
            outline="",
            tags="boy"
        )

        # Head
        self.canvas.create_oval(
            x - 27,
            y - 145,
            x + 27,
            y - 92,
            fill="#F2C7A5",
            outline="",
            tags="boy"
        )

        # Hair
        self.canvas.create_arc(
            x - 28,
            y - 150,
            x + 28,
            y - 92,
            start=0,
            extent=180,
            fill="#151515",
            outline="",
            tags="boy"
        )

        # Back arm
        self.canvas.create_line(
            x - 25,
            y - 65,
            x - 70,
            y - 15,
            fill="#F2C7A5",
            width=12,
            capstyle=tk.ROUND,
            tags="boy"
        )

        # Throwing arm
        arm_length = 85

        hand_x = (
            x +
            math.cos(math.radians(arm_angle))
            * arm_length
        )

        hand_y = (
            y - 65 +
            math.sin(math.radians(arm_angle))
            * arm_length
        )

        self.canvas.create_line(
            x + 25,
            y - 65,
            hand_x,
            hand_y,
            fill="#F2C7A5",
            width=13,
            capstyle=tk.ROUND,
            tags="boy"
        )

        # Hand
        self.canvas.create_oval(
            hand_x - 8,
            hand_y - 8,
            hand_x + 8,
            hand_y + 8,
            fill="#F2C7A5",
            outline="",
            tags="boy"
        )

        return hand_x, hand_y


    # ========================================================
    # PAINT BALL
    # ========================================================

    def create_paint_ball(self, x, y):

        color = PAINT[
            self.frame % len(PAINT)
        ]

        # Main paint
        self.canvas.create_oval(
            x - 16,
            y - 16,
            x + 16,
            y + 16,
            fill=color,
            outline="",
            tags="paint"
        )

        # Paint drops
        for i in range(3):

            dx = random.randint(-30, -10)
            dy = random.randint(-15, 15)

            r = random.randint(3, 7)

            self.canvas.create_oval(
                x + dx - r,
                y + dy - r,
                x + dx + r,
                y + dy + r,
                fill=color,
                outline="",
                tags="paint"
            )


    # ========================================================
    # PAINT SPLASH
    # ========================================================

    def create_splash(self, x, y, radius):

        self.canvas.delete("splash")

        # Main center
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=PAINT[0],
            outline="",
            tags="splash"
        )

        # Colored splash circles
        for i in range(6):

            angle = i * 60

            distance = radius * 0.65

            px = (
                x +
                math.cos(math.radians(angle))
                * distance
            )

            py = (
                y +
                math.sin(math.radians(angle))
                * distance
            )

            r = max(
                5,
                radius * 0.45
            )

            self.canvas.create_oval(
                px - r,
                py - r,
                px + r,
                py + r,
                fill=PAINT[i],
                outline="",
                tags="splash"
            )

        # Splash drops
        for i in range(14):

            angle = (
                i * (360 / 14)
            )

            distance = radius * 1.7

            px = (
                x +
                math.cos(math.radians(angle))
                * distance
            )

            py = (
                y +
                math.sin(math.radians(angle))
                * distance
            )

            r = max(
                4,
                radius * 0.08
            )

            self.canvas.create_oval(
                px - r,
                py - r,
                px + r,
                py + r,
                fill=PAINT[
                    i % len(PAINT)
                ],
                outline="",
                tags="splash"
            )


    # ========================================================
    # MAIN ANIMATION
    # ========================================================

    def animate(self):

        self.canvas.delete("boy")
        self.canvas.delete("paint")

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        if w < 500:
            w = 1200

        if h < 400:
            h = 750


        # ====================================================
        # PHASE 1
        # BOY ENTERS
        # ====================================================

        if self.frame < 35:

            progress = self.frame / 35

            boy_x = (
                -80 +
                progress * 410
            )

            self.draw_boy(
                boy_x,
                h - 170,
                215
            )


        # ====================================================
        # PHASE 2
        # PREPARE THROW
        # ====================================================

        elif self.frame < 55:

            boy_x = 330

            progress = (
                self.frame - 35
            ) / 20

            arm_angle = (
                215 -
                progress * 75
            )

            self.draw_boy(
                boy_x,
                h - 170,
                arm_angle
            )


        # ====================================================
        # PHASE 3
        # THROW
        # ====================================================

        elif self.frame < 80:

            boy_x = 330

            progress = (
                self.frame - 55
            ) / 25

            arm_angle = (
                140 -
                progress * 100
            )

            hand_x, hand_y = self.draw_boy(
                boy_x,
                h - 170,
                arm_angle
            )

            paint_x = (
                hand_x +
                progress * 170
            )

            paint_y = (
                hand_y -
                progress * 35
            )

            self.create_paint_ball(
                paint_x,
                paint_y
            )


        # ====================================================
        # PHASE 4
        # PAINT FLIES
        # ====================================================

        elif self.frame < 120:

            self.draw_boy(
                330,
                h - 170,
                40
            )

            progress = (
                self.frame - 80
            ) / 40

            start_x = 500

            end_x = w - 220

            start_y = h - 315

            end_y = h // 2

            paint_x = (
                start_x +
                (end_x - start_x)
                * progress
            )

            paint_y = (
                start_y +
                (end_y - start_y)
                * progress -
                math.sin(progress * math.pi)
                * 70
            )

            self.create_paint_ball(
                paint_x,
                paint_y
            )


        # ====================================================
        # PHASE 5
        # IMPACT
        # ====================================================

        elif self.frame < 145:

            progress = (
                self.frame - 120
            ) / 25

            radius = (
                20 +
                progress * 190
            )

            self.create_splash(
                w - 220,
                h // 2,
                radius
            )


        # ====================================================
        # PHASE 6
        # SCREEN SPLASH
        # ====================================================

        elif self.frame < 170:

            progress = (
                self.frame - 145
            ) / 25

            radius = (
                210 +
                progress * 900
            )

            self.create_splash(
                w - 220,
                h // 2,
                radius
            )


        # ====================================================
        # FINISH
        # ====================================================

        else:

            self.show_login()

            return


        # Faster animation
        self.frame += 1

        self.root.after(
            12,
            self.animate
        )


    # ========================================================
    # SHOW LOGIN
    # ========================================================

    def show_login(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_login_ui()


    # ========================================================
    # LOGIN UI
    # ========================================================

    def create_login_ui(self):

        main = tk.Frame(
            self.root,
            bg=BG
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
            width=520
        )

        left.pack(
            side="left",
            fill="both"
        )

        left.pack_propagate(False)


        canvas = tk.Canvas(
            left,
            bg="#171D2B",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )


        paint_positions = [
            (100, 150, 50),
            (180, 240, 30),
            (300, 130, 65),
            (390, 270, 40),
            (230, 370, 55),
            (420, 430, 28)
        ]


        for i, (x, y, r) in enumerate(
            paint_positions
        ):

            canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill=PAINT[i],
                outline=""
            )


        canvas.create_text(
            260,
            500,
            text="AI SQL STUDIO",
            font=("Segoe UI", 28, "bold"),
            fill=WHITE
        )

        canvas.create_text(
            260,
            540,
            text="Ask. Generate. Analyze.",
            font=("Segoe UI", 11),
            fill=GRAY
        )


        # ====================================================
        # RIGHT SIDE
        # ====================================================

        right = tk.Frame(
            main,
            bg=BG
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )


        # ====================================================
        # LOGIN CARD
        # ====================================================

        card = tk.Frame(
            right,
            bg=CARD,
            width=440,
            height=480
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)


        # Heading

        tk.Label(
            card,
            text="Welcome Back",
            font=("Segoe UI", 27, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(
            pady=(45, 5)
        )


        tk.Label(
            card,
            text="Sign in to continue to AI SQL Studio",
            font=("Segoe UI", 10),
            bg=CARD,
            fg=GRAY
        ).pack(
            pady=(0, 30)
        )


        # ====================================================
        # EMAIL
        # ====================================================

        tk.Label(
            card,
            text="Email Address",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=45
        )


        self.email_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=INPUT,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            bd=0
        )

        self.email_entry.pack(
            fill="x",
            padx=45,
            pady=(7, 18),
            ipady=11
        )


        # ====================================================
        # PASSWORD
        # ====================================================

        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=45
        )


        self.password_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=INPUT,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            bd=0,
            show="●"
        )

        self.password_entry.pack(
            fill="x",
            padx=45,
            pady=(7, 25),
            ipady=11
        )


        # ====================================================
        # SIGN IN BUTTON
        # ====================================================

        tk.Button(
            card,
            text="Sign In",
            font=("Segoe UI", 11, "bold"),
            bg=PURPLE,
            fg=WHITE,
            activebackground=PURPLE_HOVER,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.login
        ).pack(
            fill="x",
            padx=45,
            ipady=10
        )


        # ====================================================
        # REGISTER LINK
        # ====================================================

        bottom = tk.Frame(
            card,
            bg=CARD
        )

        bottom.pack(
            pady=25
        )


        tk.Label(
            bottom,
            text="Don't have an account?",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=GRAY
        ).pack(
            side="left"
        )


        tk.Button(
            bottom,
            text=" Register",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=PURPLE,
            activebackground=CARD,
            activeforeground=PURPLE_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.open_register
        ).pack(
            side="left"
        )


        self.email_entry.focus_set()


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        email = self.email_entry.get().strip()

        password = self.password_entry.get()


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not email:

            messagebox.showwarning(
                "Missing Email",
                "Please enter your email."
            )

            self.email_entry.focus_set()

            return


        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter your password."
            )

            self.password_entry.focus_set()

            return


        # ----------------------------------------------------
        # DATABASE LOGIN
        # ----------------------------------------------------

        try:

            success, user = login_user(
                email,
                password
            )


            if success:

                user_id = user[0]
                user_name = user[1]
                user_email = user[2]


                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome, {user_name}!"
                )


                # ====================================================
                # IMPORTANT DASHBOARD CONNECTION
                # ====================================================
                #
                # Your dashboard.py contains:
                #
                # class Dashboard:
                #     def __init__(self, root, username="User"):
                #
                # It does NOT contain start_dashboard().
                #
                # Therefore we keep the same root window and create
                # Dashboard directly.
                # ====================================================

                for widget in self.root.winfo_children():

                    widget.destroy()


                from dashboard import Dashboard


                Dashboard(
                    self.root,
                    user_name
                )


            else:

                messagebox.showerror(
                    "Login Failed",
                    "Incorrect email or password."
                )


        except Exception as error:

            messagebox.showerror(
                "Login Error",
                str(error)
            )


    # ========================================================
    # OPEN REGISTER
    # ========================================================

    def open_register(self):

        self.root.destroy()

        import register

        register.start_register()


# ============================================================
# START LOGIN
# ============================================================

def start_login():

    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    start_login()