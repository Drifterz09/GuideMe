import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("GuideMe Login")
app.geometry("420x600")

# ---------- CARD FRAME ----------
card = ctk.CTkFrame(
    app,
    corner_radius=20,
    fg_color="white",
    width=330,
    height=450
)
card.place(relx=0.5, rely=0.5, anchor="center")


# ---------- TWO-COLOR TITLE ----------
title_frame = ctk.CTkFrame(card, fg_color="white")
title_frame.pack(pady=(25, 0))

guide = ctk.CTkLabel(
    title_frame,
    text="Guide",
    text_color="black",
    font=("Arial Rounded MT Bold", 28)
)
guide.pack(side="left")

me = ctk.CTkLabel(
    title_frame,
    text="Me",
    text_color="#00AFAF",
    font=("Arial Rounded MT Bold", 28)
)
me.pack(side="left")

subtitle = ctk.CTkLabel(
    card,
    text="Your Smart Travel Assistant",
    text_color="gray",
    font=("Arial", 12)
)
subtitle.pack(pady=(0, 20))


# ---------- USERNAME FIELD ----------
username = ctk.CTkEntry(
    card,
    placeholder_text="Username",
    corner_radius=18,
    height=45,
    width=250
)
username.pack(pady=10)

# ---------- PASSWORD FIELD ----------
password = ctk.CTkEntry(
    card,
    placeholder_text="Password",
    corner_radius=18,
    height=45,
    width=250,
    show="*"
)
password.pack(pady=10)


# ---------- OTP BUTTON ----------
otp_btn = ctk.CTkButton(
    card,
    text="Login with OTP",
    fg_color="white",
    border_color="#00AFAF",
    border_width=2,
    text_color="#00AFAF",
    hover_color="#E6FFFF",
    width=200,
    height=35,
    corner_radius=15
)
otp_btn.pack(pady=10)

# ---------- LOGIN BUTTON ----------
login_btn = ctk.CTkButton(
    card,
    text="Login",
    fg_color="#00D1C4",
    hover_color="#00B8A9",
    text_color="white",
    width=220,
    height=42,
    corner_radius=20
)
login_btn.pack(pady=10)


# ---------- CLICKABLE "Create New Account" ----------
def create_account():
    print("Create New Account clicked!")

new_acc = ctk.CTkLabel(
    card,
    text="Create New Account",
    text_color="#FF7B7B",
    font=("Arial", 11, "underline"),
    cursor="hand2"
)
new_acc.pack(pady=(15, 10))

new_acc.bind("<Button-1>", lambda e: create_account())


app.mainloop()
