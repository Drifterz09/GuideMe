import tkinter as tk
from tkinter import BOTH, Canvas

# GitHub Copilot

root = tk.Tk()
root.title("Dashboard Demo")
root.state('zoomed')  # full screen

header_height = 120
canvas = Canvas(root, height=header_height, highlightthickness=0)
canvas.pack(fill="x")

# placeholder for toggle window id so draw_header can reference it before creation
toggle_window = None

# draw header rectangle and reposition the toggle on resize
def draw_header(event=None):
    w = event.width if event else root.winfo_width()
    canvas.delete("bg")
    canvas.create_rectangle(0, 0, w, header_height, outline="", fill=current_colors["header"], tags="bg")
    if toggle_window:
        # place toggle near the right edge
        canvas.coords(toggle_window, w - 20, 40)

canvas.bind("<Configure>", draw_header)

# NAV BUTTONS placed on the canvas
btn_names = ["Home", "Budget", "Profile", "Logout", "Settings", "Help"]
x_place = 40
buttons = []
for name in btn_names:
    b = tk.Button(canvas, text=name, bd=0, padx=20, pady=5)
    buttons.append(b)
    canvas.create_window(x_place, 40, window=b, anchor="nw")
    x_place += 120

# MAIN CONTENT FRAME
main_frame = tk.Frame(root)
main_frame.pack(fill=BOTH, expand=True)

title = tk.Label(main_frame, text="Welcome to our app, GuideMe!", font=("Segoe UI", 28))
title.pack(pady=30)

desc = tk.Label(main_frame, text="Get Started", font=("Segoe UI", 14))
desc.pack()

# Theme definitions
dark_colors = {
    "root_bg": "#0f0f0f",
    "header": "#1f1f1f",
    "main_bg": "#0f0f0f",
    "text": "#eaeaea",
    "muted": "#bdbdbd",
    "nav_bg": "#262626",
    "nav_fg": "#eaeaea",
    "btn_active_bg": "#333333",
    "toggle_bg": "#2b2b2b",
    "toggle_fg": "#eaeaea"
}

light_colors = {
    "root_bg": "#fafafa",
    "header": "#e9e9e9",  # neutral light header (purple removed)
    "main_bg": "#fafafa",
    "text": "#1a1a1a",
    "muted": "#555555",
    "nav_bg": "#ffffff",
    "nav_fg": "#1a1a1a",
    "btn_active_bg": "#e6e6e6",
    "toggle_bg": "#f0f0f0",
    "toggle_fg": "#1a1a1a"
}

# start in dark mode
is_dark = True
current_colors = dark_colors.copy()

def apply_theme():
    global current_colors
    current_colors = dark_colors.copy() if is_dark else light_colors.copy()

    root.configure(bg=current_colors["root_bg"])
    canvas.configure(bg=current_colors["header"])
    # redraw header rectangle with new color
    draw_header()

    main_frame.config(bg=current_colors["main_bg"])
    title.config(bg=current_colors["main_bg"], fg=current_colors["text"])
    desc.config(bg=current_colors["main_bg"], fg=current_colors["muted"])

    for b in buttons:
        b.config(
            bg=current_colors["nav_bg"],
            fg=current_colors["nav_fg"],
            activebackground=current_colors["btn_active_bg"],
            activeforeground=current_colors["nav_fg"],
            relief="flat"
        )

    toggle_btn.config(
        bg=current_colors["toggle_bg"],
        fg=current_colors["toggle_fg"],
        activebackground=current_colors["btn_active_bg"],
        activeforeground=current_colors["toggle_fg"]
    )

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    toggle_btn.config(text="Light" if is_dark else "Dark")
    apply_theme()

# create a toggle button on the header (will be positioned by draw_header)
toggle_btn = tk.Button(canvas, text="Light" if is_dark else "Dark", bd=0, padx=12, pady=6, command=toggle_theme)
toggle_window = canvas.create_window(0, 40, window=toggle_btn, anchor="ne")

# initial theme apply and initial draw
apply_theme()

root.mainloop()
