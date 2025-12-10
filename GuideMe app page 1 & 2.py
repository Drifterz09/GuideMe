import customtkinter as ctk

# ============================================
# DESTINATION DATA
# ============================================
DESTINATION_SUGGESTIONS = {
    "Beach": ["Goa", "Kovalam", "Pondicherry", "Varkala"],
    "City": ["Bangalore", "Mumbai", "Delhi", "Hyderabad"],
    "Mountains": ["Manali", "Ooty", "Munnar", "Darjeeling"],
    "International": ["Dubai", "Singapore", "Paris", "Maldives"]
}

TRIP_DURATIONS = ["1–3 Days", "4–7 Days", "1–2 Weeks", "1+ Month"]


# ============================================
# TRIP PAGE (After Login)
# ============================================
class TripPage:
    def __init__(self, root, username):
        self.root = root
        self.root.title("GuideMe - Plan Your Trip")
        self.root.geometry("420x600")
        self.root.configure(bg="#F5F7FA")

        self.username = username

        # GREETING
        self.greet = ctk.CTkLabel(
            root,
            text=f"Hey {self.username}, let's plan your trip! ✈️",
            text_color="black",
            font=("Arial Rounded MT Bold", 18)
        )
        self.greet.pack(pady=(25, 20))

        # TRIP TYPE
        ctk.CTkLabel(
            root, text="Select Trip Type:", text_color="black", font=("Arial", 12)
        ).pack(pady=(5, 2))

        self.trip_type = ctk.CTkComboBox(
            root,
            values=list(DESTINATION_SUGGESTIONS.keys()),
            width=240,
            height=38,
            corner_radius=12,
            command=self.show_suggestions
        )
        self.trip_type.pack(pady=10)

        # SUGGESTIONS FRAME
        self.suggestion_frame = ctk.CTkFrame(root, fg_color="#F5F7FA")
        self.suggestion_frame.pack(pady=5)

        # CUSTOM DESTINATION
        ctk.CTkLabel(
            root, text="Or type your own destination:", text_color="black"
        ).pack(pady=(10, 5))

        self.dest_entry = ctk.CTkEntry(
            root, placeholder_text="Enter destination...",
            width=260, height=40, corner_radius=12
        )
        self.dest_entry.pack(pady=5)

        # DURATION DROPDOWN
        ctk.CTkLabel(
            root, text="Trip Duration:", text_color="black", font=("Arial", 12)
        ).pack(pady=(15, 2))

        self.duration_box = ctk.CTkComboBox(
            root, values=TRIP_DURATIONS, width=240, height=38, corner_radius=12
        )
        self.duration_box.pack(pady=10)

        # GENERATE BUTTON
        self.generate_btn = ctk.CTkButton(
            root,
            text="Generate Checklist",
            fg_color="#00D1C4",
            hover_color="#00B8A9",
            text_color="white",
            width=240,
            height=42,
            corner_radius=20,
            command=self.generate_checklist
        )
        self.generate_btn.pack(pady=25)

    # SHOW SUGGESTED DESTINATIONS
    def show_suggestions(self, choice):
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        destinations = DESTINATION_SUGGESTIONS.get(choice, [])

        for dest in destinations:
            btn = ctk.CTkButton(
                self.suggestion_frame,
                text=dest,
                fg_color="white",
                text_color="black",
                border_width=1,
                border_color="#00B8A9",
                hover_color="#E6FFFF",
                width=100,
                height=28,
                corner_radius=20,
                command=lambda d=dest: self.dest_entry.insert(0, d)
            )
            btn.pack(side="left", padx=5, pady=5)

    # GENERATE CHECKLIST
    def generate_checklist(self):
        print("Destination:", self.dest_entry.get())
        print("Duration:", self.duration_box.get())


# ============================================
# LOGIN PAGE
# ============================================
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("GuideMe Login")
        self.root.geometry("420x600")
        self.root.configure(bg="#F5F7FA")

        # ---------- CARD ----------
        self.card = ctk.CTkFrame(
            root,
            corner_radius=20,
            fg_color="white",
            width=330,
            height=450
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # ---------- TITLE FRAME ----------
        title_frame = ctk.CTkFrame(self.card, fg_color="white")
        title_frame.pack(pady=(25, 0))

        ctk.CTkLabel(
            title_frame,
            text="Guide",
            text_color="black",
            font=("Arial Rounded MT Bold", 28)
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Me",
            text_color="#00AFAF",
            font=("Arial Rounded MT Bold", 28)
        ).pack(side="left")

        ctk.CTkLabel(
            self.card,
            text="Your Smart Travel Assistant",
            text_color="gray",
            font=("Arial", 12)
        ).pack(pady=(0, 20))

        # ---------- USERNAME ----------
        self.username = ctk.CTkEntry(
            self.card,
            placeholder_text="Username",
            corner_radius=18,
            height=45,
            width=250
        )
        self.username.pack(pady=10)

        # ---------- PASSWORD ----------
        self.password = ctk.CTkEntry(
            self.card,
            placeholder_text="Password",
            corner_radius=18,
            height=45,
            width=250,
            show="*"
        )
        self.password.pack(pady=10)

        # ---------- OTP BUTTON ----------
        ctk.CTkButton(
            self.card,
            text="Login with OTP",
            fg_color="white",
            border_color="#00AFAF",
            border_width=2,
            text_color="#00AFAF",
            hover_color="#E6FFFF",
            width=200,
            height=35,
            corner_radius=15
        ).pack(pady=10)

        # ---------- LOGIN BUTTON ----------
        login_btn = ctk.CTkButton(
            self.card,
            text="Login",
            fg_color="#00D1C4",
            hover_color="#00B8A9",
            text_color="white",
            width=220,
            height=42,
            corner_radius=20,
            command=self.open_trip_page
        )
        login_btn.pack(pady=10)

        # ---------- CREATE ACCOUNT ----------
        new_acc = ctk.CTkLabel(
            self.card,
            text="Create New Account",
            text_color="#FF7B7B",
            font=("Arial", 11, "underline"),
            cursor="hand2"
        )
        new_acc.pack(pady=(15, 10))

    # SWITCH TO TRIP PAGE
    def open_trip_page(self):
        username_value = self.username.get() or "Traveler"

        # destroy login window
        self.root.destroy()

        # open trip page
        new_root = ctk.CTk()
        TripPage(new_root, username_value)
        new_root.mainloop()


# ============================================
# RUN APP
# ============================================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
LoginPage(root)
root.mainloop()
