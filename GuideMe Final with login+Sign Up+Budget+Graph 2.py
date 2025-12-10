from PIL import Image
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG_IMAGE_PATH = "picture 1.png"

# ---------------- DUMMY USER DATABASE ----------------
USERS = {}

# ---------------- REAL DESTINATION DATA ----------------
DESTINATIONS = {
    "Beach": ["Goa", "Varkala", "Pondicherry", "Kovalam"],
    "Mountains": ["Manali", "Ooty", "Munnar", "Coorg"],
    "City": ["Bangalore", "Mumbai", "Delhi", "Hyderabad"],
    "International": ["Dubai", "Singapore", "Paris", "Maldives"]
}

TRANSPORT_COST = {
    "Flight": 5000,
    "Train": 2000,
    "Bus": 1200,
    "Car": 3000
}


# ---------------- MAIN APP ----------------
class GuideMeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GuideMe")
        self.geometry("390x720")
        self.resizable(False, False)

        try:
            self.bg_image = ctk.CTkImage(Image.open(BG_IMAGE_PATH), size=(390, 720))
        except:
            self.bg_image = None

        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.current_frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, page, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = page(self, **kwargs)
        self.current_frame.place(relwidth=1, relheight=1)


# ---------------- LOGIN PAGE ----------------
class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        card = ctk.CTkFrame(self, width=340, height=460, corner_radius=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="GuideMe", font=("Poppins", 26, "bold")).pack(pady=15)

        self.username = ctk.CTkEntry(card, placeholder_text="Username", width=260)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=260)
        self.password.pack(pady=10)

        ctk.CTkButton(card, text="Login", width=260, fg_color="#00BFA5",
                       command=self.login).pack(pady=15)

        ctk.CTkButton(card, text="Create Account", fg_color="transparent",
                       text_color="#FF7043",
                       command=lambda: master.switch_frame(SignupPage)).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in USERS and USERS[user] == pwd:
            self.master.switch_frame(TripPage, username=user)
        else:
            messagebox.showerror("Error", "Invalid Login ❌")


# ---------------- SIGNUP PAGE ----------------
class SignupPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        card = ctk.CTkFrame(self, width=340, height=420, corner_radius=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Create Account", font=("Poppins", 22, "bold")).pack(pady=15)

        self.username = ctk.CTkEntry(card, placeholder_text="New Username", width=260)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(card, placeholder_text="New Password", show="*", width=260)
        self.password.pack(pady=10)

        ctk.CTkButton(card, text="Create",
                      fg_color="#00BFA5", command=self.create).pack(pady=15)

    def create(self):
        user = self.username.get()
        pwd = self.password.get()

        if not user or not pwd:
            messagebox.showerror("Error", "Fill all fields")
            return

        USERS[user] = pwd
        messagebox.showinfo("Success", "Account Created ✅")
        self.master.switch_frame(LoginPage)


# ---------------- TRIP PAGE ----------------
class TripPage(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master, fg_color="transparent")

        self.username = username
        self.selected_transport = None

        card = ctk.CTkFrame(self, width=340, height=620, corner_radius=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=f"Welcome {username} ✨", font=("Poppins", 18, "bold")).pack(pady=10)

        # Trip Type
        self.trip_type = ctk.CTkComboBox(card, values=list(DESTINATIONS.keys()), width=250,
                                          command=self.show_destinations)
        self.trip_type.pack(pady=10)

        # Destination
        self.destination_entry = ctk.CTkEntry(card, placeholder_text="Destination", width=250)
        self.destination_entry.pack(pady=10)

        self.dest_buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.dest_buttons_frame.pack(pady=5)

        # Transport
        ctk.CTkLabel(card, text="Select Transport").pack(pady=10)

        transport_frame = ctk.CTkFrame(card, fg_color="transparent")
        transport_frame.pack(pady=5)

        for t in TRANSPORT_COST:
            ctk.CTkButton(transport_frame, text=t, width=70,
                          command=lambda x=t: self.select_transport(x)).pack(side="left", padx=5)

        # Budget Result
        self.budget_label = ctk.CTkLabel(card, text="")
        self.budget_label.pack(pady=15)

        ctk.CTkButton(card, text="Generate Packages",
                      fg_color="#00BFA5",
                      command=self.generate_budget).pack(pady=10)

        ctk.CTkButton(card, text="Logout", fg_color="red",
                      command=lambda: master.switch_frame(LoginPage)).pack(pady=15)

    def show_destinations(self, choice):
        for w in self.dest_buttons_frame.winfo_children():
            w.destroy()

        for city in DESTINATIONS.get(choice, []):
            ctk.CTkButton(self.dest_buttons_frame,
                          text=city, width=80,
                          command=lambda c=city: self.destination_entry.insert(0, c))\
                .pack(side="left", padx=5)

    def select_transport(self, mode):
        self.selected_transport = mode
        messagebox.showinfo("Selected", f"{mode} Selected ✅")

    def generate_budget(self):
        if not self.destination_entry.get() or not self.selected_transport:
            messagebox.showerror("Error", "Select Destination & Transport")
            return

        base = TRANSPORT_COST[self.selected_transport]

        eco = base + 1500
        standard = base + 3500
        premium = base + 6000

        self.budget_label.configure(
            text=f"Economy: ₹{eco}\nStandard: ₹{standard}\nPremium: ₹{premium}"
        )


# ---------------- RUN APP ----------------
app = GuideMeApp()
app.mainloop()
