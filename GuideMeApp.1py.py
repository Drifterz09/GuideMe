
# GuideMeApp - Single merged file with progressive reveal
# Requires: customtkinter (pip install customtkinter)
# Save as: GuideMeApp.py

import customtkinter as ctk
from tkinter import messagebox
import json
import os
import math
import random
import time

# ---------------- CONFIG / PALETTE ----------------
PALETTE = {
    "bg": "#F4F6F6",
    "card": "#FFFFFF",
    "accent": "#97009F",
    "accent_dark": "#97009F",
    "muted": "#9DA3A6",
    "title_black": "#111111",
    "link": "#FF6A6A",
    "panel": "#F2F2F2",
}

USER_FILE = "users.json"
HISTORY_FILE = "trip_history.json"

# ---------------- HELPERS ----------------
def load_json_safe(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)
        return default.copy()
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default.copy()

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

CITY_COORDS = {
    "goa": (15.4909, 73.8278),
    "mumbai": (19.075984, 72.877656),
    "delhi": (28.704059, 77.102490),
    "manali": (32.2432, 77.1892),
    "bangalore": (12.971599, 77.594566),
    "hyderabad": (17.385044, 78.486671),
    "kochi": (9.931233, 76.267303),
    "ooty": (11.4064, 76.6932),
    "munnar": (10.0889, 77.0595),
    "darjeeling": (27.0360, 88.2627),
    "paris": (48.8566, 2.3522),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "kovalam": (8.4125, 76.9780),
    "pondicherry": (11.9416, 79.8083),
    "varkala": (8.7376, 76.7153),
}

def haversine_km(a, b):
    # a and b should be (lat, lon)
    if not a or not b:
        return 0.0
    R = 6371.0
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    aa = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(aa), math.sqrt(1-aa))
    return R * c

def estimate_travel_time_km(distance_km, transport):
    speed = {"Flight": 800, "Train": 80, "Bus": 60, "Car": 60}
    s = speed.get(transport, 60)
    hours = distance_km / s
    if transport == "Train":
        hours *= 1.15
    if transport == "Bus":
        hours *= 1.2
    return hours

# ---------------- DATA ----------------
DESTINATION_SUGGESTIONS = {
    "Beach": ["Goa", "Kovalam", "Varkala", "Pondicherry"],
    "City": ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Kochi"],
    "Mountains": ["Manali", "Munnar", "Ooty", "Darjeeling"],
    "International": ["Dubai", "Singapore", "Paris", "Maldives"]
}

HOTELS_BY_LOCATION = {
    "goa": ["Taj Exotica Resort", "The Leela Goa", "Park Hyatt Goa"],
    "bangalore": ["The Ritz-Carlton Bangalore", "Taj MG Road", "JW Marriott"],
    "mumbai": ["Taj Mahal Palace", "The Oberoi", "Trident Nariman Point"],
    "delhi": ["The Imperial", "Taj Palace", "ITC Maurya"],
    "manali": ["Solang Valley Resort", "Apple Country Resort"],
    "munnar": ["Tea County", "Amber Dale Munnar"],
    "ooty": ["Savoy Ooty", "Sterling Ooty"],
    "darjeeling": ["The Elgin", "Mayfair Darjeeling"],
    "kovalam": ["The Leela Kovalam", "Turtle On The Beach"],
    "pondicherry": ["Promenade Hotel", "Le Dupleix"],
    "varkala": ["Gateway Varkala", "Clafouti Beach Resort"],
    "hyderabad": ["ITC Kohenur", "Taj Deccan"],
    "kochi": ["Le Meridien Kochi", "Grand Hyatt Kochi"],
    "dubai": ["Atlantis The Palm", "Burj Al Arab"],
    "singapore": ["Marina Bay Sands", "Pan Pacific"],
    "paris": ["Le Meurice", "Hotel Napoleon"],
    "maldives": ["Soneva Fushi", "Anantara Veli"]
}

# ---------------- APP CORE ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class GuideMeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GuideMe — Travel App")
        self.geometry("420x720")
        self.minsize(380, 520)
        self.configure(fg_color=PALETTE["bg"])

        # persistent data
        self.users = load_json_safe(USER_FILE, {})
        self.history = load_json_safe(HISTORY_FILE, {})

        self.active_frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, page_class, **kwargs):
        # destroy and create next frame
        if self.active_frame is not None:
            self.active_frame.destroy()
        self.active_frame = page_class(self, **kwargs)
        # pack the CTkFrame (or CTk derived frame)
        try:
            self.active_frame.pack(expand=True, fill="both")
        except Exception:
            pass

    def save_users(self):
        save_json(USER_FILE, self.users)

    def save_history(self):
        save_json(HISTORY_FILE, self.history)

# ---------------- BIG MESSAGE POPUP ----------------
def big_message(title, message, color=PALETTE["accent"]):
    mb = ctk.CTkToplevel()
    mb.title(title)
    mb.geometry("420x220")
    mb.grab_set()
    mb.configure(fg_color=PALETTE["card"])

    ctk.CTkLabel(mb, text=title, font=("Helvetica", 20, "bold"), text_color=color).pack(pady=12)
    ctk.CTkLabel(mb, text=message, font=("Helvetica", 13), wraplength=380, justify="center").pack(pady=6)
    ctk.CTkButton(mb, text="OK", width=140, fg_color=color, command=mb.destroy).pack(pady=14)

# ---------------- LOGIN PAGE ----------------
class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=PALETTE["bg"])
        self.master = master  # GuideMeApp instance

        # top spacing
        top_space = ctk.CTkFrame(self, fg_color="transparent", height=60)
        top_space.pack(fill="x")

        title = ctk.CTkLabel(self, text="GuideMe", font=("Poppins", 34, "bold"),
                             text_color=PALETTE["title_black"])
        title.pack(pady=(2, 6))

        subtitle = ctk.CTkLabel(self, text="Your Smart Travel Assistant",
                                font=("Helvetica", 12), text_color=PALETTE["muted"])
        subtitle.pack(pady=(0, 16))

        # white card
        card = ctk.CTkFrame(self, fg_color=PALETTE["card"], corner_radius=20,
                            width=360, height=430)
        card.place(relx=0.5, rely=0.45, anchor="center")

        # logo
        logo_frame = ctk.CTkFrame(card, fg_color="transparent")
        logo_frame.pack(pady=(18, 2))

        ctk.CTkLabel(logo_frame, text="Guide", font=("Poppins", 26, "bold"),
                     text_color=PALETTE["title_black"]).pack(side="left")
        ctk.CTkLabel(logo_frame, text="Me", font=("Poppins", 26, "bold"),
                     text_color=PALETTE["accent"]).pack(side="left")

        ctk.CTkLabel(card, text=" ", font=("Helvetica", 8)).pack()

        # entries
        self.username = ctk.CTkEntry(card, placeholder_text="Username",
                                     width=300, height=42, corner_radius=18)
        self.username.pack(pady=(10,6))

        self.password = ctk.CTkEntry(card, placeholder_text="Password",
                                     width=300, height=42, corner_radius=18, show="*")
        self.password.pack(pady=(0,8))

        # OTP button
        self.otp_btn = ctk.CTkButton(
            card, text="Login with OTP", width=250, height=40,
            fg_color=PALETTE["card"], text_color=PALETTE["accent"],
            border_width=2, border_color=PALETTE["accent"],
            hover_color="#E8FFFB",
            command=self.otp_flow
        )
        self.otp_btn.pack(pady=(6,10))

        # Login button
        self.login_btn = ctk.CTkButton(
            card, text="Login", width=280, height=48,
            fg_color=PALETTE["accent"], hover_color=PALETTE["accent_dark"],
            text_color="white", corner_radius=24,
            command=self.do_login
        )
        self.login_btn.pack(pady=(6,10))

        # Create account
        create_btn = ctk.CTkButton(
            card, text="Create New Account", fg_color="transparent",
            text_color=PALETTE["link"], hover_color="#FFF2F2",
            corner_radius=8, command=self.open_signup
        )
        create_btn.pack(pady=(6,12))

        ctk.CTkLabel(self, text="Tip: create an account to save trip history",
                     font=("Helvetica", 10), text_color=PALETTE["muted"])\
            .pack(side="bottom", pady=10)

    # OTP flow (demo)
    def otp_flow(self):
        otp = random.randint(100000, 999999)
        self._last_otp = str(otp)

        big_message("OTP sent",
                    f"Your OTP is: {otp}\n(Shown for demo — normally SMS)")

        otp_win = ctk.CTkToplevel()
        otp_win.title("Enter OTP")
        otp_win.geometry("360x160")
        otp_win.grab_set()

        ctk.CTkLabel(otp_win, text="Enter OTP", font=("Helvetica", 14)).pack(pady=(12,6))
        otp_entry = ctk.CTkEntry(otp_win, placeholder_text="6-digit OTP", width=240)
        otp_entry.pack(pady=6)

        def verify():
            if otp_entry.get().strip() == getattr(self, "_last_otp", ""):
                otp_win.destroy()
                username = self.username.get().strip() or f"guest_{int(time.time())%10000}"
                if username not in self.master.users:
                    self.master.users[username] = ""
                    self.master.save_users()
                self.master.switch_frame(TripPage, username=username)
            else:
                messagebox.showerror("Invalid OTP", "OTP did not match")

        ctk.CTkButton(otp_win, text="Verify", width=160,
                      fg_color=PALETTE["accent"], command=verify).pack(pady=10)

    # Standard login
    def do_login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Missing", "Please enter username and password")
            return

        if user in self.master.users and self.master.users[user] == pwd:
            self.master.switch_frame(TripPage, username=user)
        else:
            messagebox.showerror("Invalid", "Username or password incorrect")

    def open_signup(self):
        SignupModal(self.master)

# ---------------- SIGNUP MODAL ----------------
class SignupModal(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.title("Create Account")
        self.geometry("420x420")
        self.configure(fg_color=PALETTE["bg"])
        self.grab_set()

        frame = ctk.CTkFrame(self, fg_color=PALETTE["card"],
                             corner_radius=16, width=360, height=360)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Create New Account",
                     font=("Poppins", 18, "bold")).pack(pady=(18,8))

        self.u_entry = ctk.CTkEntry(frame, placeholder_text="Choose username", width=300)
        self.u_entry.pack(pady=8)

        self.p_entry = ctk.CTkEntry(frame, placeholder_text="Choose password",
                                    width=300, show="*")
        self.p_entry.pack(pady=8)

        ctk.CTkButton(frame, text="Sign Up", width=220,
                      fg_color=PALETTE["accent"],
                      command=self.create_account).pack(pady=12)

        ctk.CTkButton(frame, text="Cancel", width=220,
                      fg_color="transparent", text_color=PALETTE["muted"],
                      command=self.destroy).pack()

    def create_account(self):
        u = self.u_entry.get().strip()
        p = self.p_entry.get().strip()

        if not u or not p:
            messagebox.showwarning("Missing", "Fill both fields")
            return

        if u in self.master.users:
            messagebox.showerror("Exists", "Username already exists")
            return

        self.master.users[u] = p
        self.master.save_users()

        messagebox.showinfo("Created", "Account created successfully!")
        self.destroy()

# ---------------- TRIP PAGE ----------------
class TripPage(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master, fg_color=PALETTE["bg"])
        self.master = master
        self.username = username

        self.transport = None
        self.distance_km = 0
        self.travel_hours = 0

        # CHECKLIST BASED ON TRIP TYPE
        self.CHECKLISTS = {
            "Beach": [
                "Sunscreen", "Beach Towel", "Swimwear", "Sunglasses",
                "Flip Flops", "Water Bottle", "Camera"
            ],
            "Mountains": [
                "Winter Jacket", "Trekking Shoes", "Woolen Gloves",
                "Thermal Wear", "Portable Charger", "Torch", "Medicines"
            ],
            "City": [
                "Comfortable Shoes", "Power Bank", "Wallet / ID",
                "Public Transport Card", "Phone Charger"
            ],
            "International": [
                "Passport", "Visa Documents", "Currency",
                "Universal Adapter", "Travel Insurance", "Copies of IDs"
            ]
        }

        # SPECIAL DESTINATION ADD-ONS
        self.DEST_CHECKLIST = {
            "goa": ["Beach Hat", "Aloe Vera Gel"],
            "paris": ["Travel Guidebook", "Translator App"],
            "dubai": ["Light Clothing", "Respectful Dress for Mosques"],
            "manali": ["Snow Boots", "Muffler"],
            "munnar": ["Raincoat", "Warm Socks"]
        }

        # ------- MAIN LAYOUT --------
        ctk.CTkLabel(self, text=f"Welcome {username} ✨",
                     font=("Poppins", 22, "bold"),
                     text_color=PALETTE["title_black"]).pack(pady=10)

        self.tabview = ctk.CTkTabview(self, width=380, height=640)
        self.tabview.pack(pady=10)

        # TABS (Only Plan Trip enabled first)
        self.plan_tab = self.tabview.add("Plan Trip")
        self.hotels_tab = self.tabview.add("Hotels")
        self.budget_tab = self.tabview.add("Budget")
        self.history_tab = self.tabview.add("Trip History")
        self.checklist_tab = self.tabview.add("Checklist")

        # Disable all except Plan Trip
        for tab in [self.hotels_tab, self.budget_tab, self.history_tab, self.checklist_tab]:
            tab._state = "disabled"

        # Build UI sections
        self.build_plan_trip()
        self.build_hotels_tab()
        self.build_budget_tab()
        self.build_history_tab()
        self.build_checklist_tab()

        # Logout button
        ctk.CTkButton(self, text="Logout", width=120,
                      fg_color="#FF3B30",
                      command=self.logout).pack(pady=8)

    # PLAN TRIP TAB
    def build_plan_trip(self):
        tab = self.plan_tab

        ctk.CTkLabel(tab, text="Start Location").pack(pady=5)
        self.start_entry = ctk.CTkEntry(tab, width=300)
        self.start_entry.pack()

        ctk.CTkLabel(tab, text="Trip Type").pack(pady=5)
        self.trip_type = ctk.CTkComboBox(tab, width=300,
                                         values=list(DESTINATION_SUGGESTIONS.keys()),
                                         command=lambda x: (self.show_suggestions(x), self.check_ready()))
        self.trip_type.pack()

        ctk.CTkLabel(tab, text="Destination").pack(pady=5)
        self.dest_entry = ctk.CTkEntry(tab, width=300)
        self.dest_entry.pack()

        self.suggest_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.suggest_frame.pack(pady=5)

        ctk.CTkLabel(tab, text="Transport").pack(pady=5)

        self.transport_buttons = {}
        trans_frame = ctk.CTkFrame(tab)
        trans_frame.pack()

        for t in ["Flight", "Train", "Bus", "Car"]:
            btn = ctk.CTkButton(trans_frame, text=t, width=70,
                                fg_color="#E9F8F6", text_color=PALETTE["muted"],
                                hover_color="#D6F3EE",
                                command=lambda tt=t: (self.select_transport(tt), self.check_ready()))
            btn.pack(side="left", padx=4)
            self.transport_buttons[t] = btn

        # =====================================================
        # HIDDEN / ADVANCED SECTION (appears after basic fields filled)
        # =====================================================
        self.advanced_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.advanced_frame.pack(pady=10)
        self.advanced_frame.pack_forget()   # hide initially

        # INFO LABEL inside advanced_frame
        self.info_label = ctk.CTkLabel(self.advanced_frame, text="Distance: -- km\nTime: --")
        self.info_label.pack(pady=10)

        # Generate Button (inside advanced_frame)
        self.generate_btn = ctk.CTkButton(
            self.advanced_frame,
            text="Generate Packages",
            fg_color=PALETTE["accent"],
            command=self.generate_packages
        )
        self.generate_btn.pack(pady=10)

        # Bind update checker
        self.start_entry.bind("<KeyRelease>", self.check_ready)
        self.dest_entry.bind("<KeyRelease>", self.check_ready)

    # HOTELS TAB
    def build_hotels_tab(self):
        tab = self.hotels_tab
        ctk.CTkLabel(tab, text="Suggested Hotels",
                     font=("Poppins", 16, "bold")).pack(pady=10)

        # CTkTextbox exists in recent customtkinter releases; fallback to simple CTkLabel if missing
        try:
            self.hotel_box = ctk.CTkTextbox(tab, width=330, height=400)
            self.hotel_box.pack(pady=10)
            self.hotel_box.configure(state="disabled")
        except Exception:
            self.hotel_box = ctk.CTkLabel(tab, text="", width=330, height=20, anchor="nw")
            self.hotel_box.pack(pady=10)

    # BUDGET TAB
    def build_budget_tab(self):
        tab = self.budget_tab
        ctk.CTkLabel(tab, text="Estimated Packages",
                     font=("Poppins", 16, "bold")).pack(pady=10)

        self.budget_label = ctk.CTkLabel(tab, text="", font=("Helvetica", 14))
        self.budget_label.pack(pady=10)

    # HISTORY TAB
    def build_history_tab(self):
        tab = self.history_tab
        ctk.CTkLabel(tab, text="Past Trips",
                     font=("Poppins", 16, "bold")).pack(pady=10)

        try:
            self.history_box = ctk.CTkTextbox(tab, width=330, height=400)
            self.history_box.pack(pady=10)
            self.history_box.configure(state="disabled")
        except Exception:
            self.history_box = ctk.CTkLabel(tab, text="", width=330, height=20, anchor="nw")
            self.history_box.pack(pady=10)

    # CHECKLIST TAB
    def build_checklist_tab(self):
        tab = self.checklist_tab
        ctk.CTkLabel(tab, text="Trip Checklist",
                     font=("Poppins", 16, "bold")).pack(pady=10)

        try:
            self.checklist_box = ctk.CTkTextbox(tab, width=330, height=400)
            self.checklist_box.pack(pady=10)
            self.checklist_box.configure(state="disabled")
        except Exception:
            self.checklist_box = ctk.CTkLabel(tab, text="", width=330, height=20, anchor="nw")
            self.checklist_box.pack(pady=10)

    # SUGGESTIONS
    def show_suggestions(self, trip_type):
        for w in self.suggest_frame.winfo_children():
            w.destroy()

        for d in DESTINATION_SUGGESTIONS.get(trip_type, []):
            ctk.CTkButton(self.suggest_frame, text=d, width=80,
                          fg_color="#E6F9F6",
                          command=lambda x=d: (self.dest_entry.delete(0, "end"), self.dest_entry.insert(0, x))
                          ).pack(side="left", padx=4)

    # TRANSPORT SELECT
    def select_transport(self, t):
        self.transport = t
        for x, b in self.transport_buttons.items():
            if x == t:
                b.configure(fg_color=PALETTE["accent"], text_color="white")
            else:
                b.configure(fg_color="#E9F8F6", text_color=PALETTE["muted"])

    # CHECK READY - show advanced_frame only when basic fields filled
    def check_ready(self, *args):
        start_ok = bool(self.start_entry.get().strip())
        dest_ok = bool(self.dest_entry.get().strip())
        type_ok = bool(self.trip_type.get().strip())
        trans_ok = bool(self.transport)

        if start_ok and dest_ok and type_ok and trans_ok:
            # show advanced frame
            try:
                self.advanced_frame.pack(pady=10)
            except Exception:
                pass
        else:
            # hide advanced frame
            try:
                self.advanced_frame.pack_forget()
            except Exception:
                pass

    # ROUTE CALC
    def compute_route(self):
        start = self.start_entry.get().lower().strip()
        dest = self.dest_entry.get().lower().strip()

        a = CITY_COORDS.get(start)
        b = CITY_COORDS.get(dest)

        # if both coords present use haversine, else random plausible distance
        if a and b:
            self.distance_km = round(haversine_km(a, b), 1)
        else:
            self.distance_km = random.randint(80, 600)
        self.travel_hours = estimate_travel_time_km(self.distance_km, self.transport or "Car")

        self.info_label.configure(
            text=f"Distance: {self.distance_km} km\\nTime: {int(self.travel_hours)}h {int((self.travel_hours % 1) * 60)}m"
        )

    # GENERATE PACKAGES
    def generate_packages(self):
        if not self.start_entry.get().strip() or not self.dest_entry.get().strip() or not self.transport:
            messagebox.showerror("Missing", "Please fill all fields")
            return

        self.compute_route()

        base = max(500, int(self.distance_km * 10))
        mult = {"Flight": 1.6, "Train": 1.0, "Bus": 0.8, "Car": 0.9}.get(self.transport, 1)

        eco = int(base * 0.9 * mult)
        std = int(base * 1.4 * mult)
        prem = int(base * 2.0 * mult)

        self.budget_label.configure(
            text=f"Economy: ₹{eco:,}\\nStandard: ₹{std:,}\\nPremium: ₹{prem:,}"
        )

        # HOTELS
        dest = self.dest_entry.get().lower().strip()
        hotels = HOTELS_BY_LOCATION.get(dest, ["Taj Hotel", "Treebo", "Lemon Tree"])

        try:
            self.hotel_box.configure(state="normal")
            self.hotel_box.delete("1.0", "end")
            for h in hotels:
                self.hotel_box.insert("end", f"• {h}\\n")
            self.hotel_box.configure(state="disabled")
        except Exception:
            # fallback label update
            try:
                self.hotel_box.configure(text="\\n".join(f"• {h}" for h in hotels))
            except Exception:
                pass

        # CHECKLIST
        ttype = self.trip_type.get()
        base_list = self.CHECKLISTS.get(ttype, [])
        extra = self.DEST_CHECKLIST.get(dest, [])

        final_list = base_list + extra

        try:
            self.checklist_box.configure(state="normal")
            self.checklist_box.delete("1.0", "end")
            for item in final_list:
                self.checklist_box.insert("end", f"✔ {item}\\n")
            self.checklist_box.configure(state="disabled")
        except Exception:
            try:
                self.checklist_box.configure(text="\\n".join(f"✔ {i}" for i in final_list))
            except Exception:
                pass

        # HISTORY
        rec = {
            "destination": self.dest_entry.get(),
            "trip_type": ttype,
            "transport": self.transport,
            "distance_km": self.distance_km,
            "time": self.travel_hours
        }

        user_hist = self.master.history.get(self.username, [])
        user_hist.append(rec)
        self.master.history[self.username] = user_hist
        self.master.save_history()

        try:
            self.history_box.configure(state="normal")
            self.history_box.delete("1.0", "end")
            for r in user_hist:
                self.history_box.insert("end", f"{r['destination']} — {r['trip_type']} — {r['transport']}\\n")
            self.history_box.configure(state="disabled")
        except Exception:
            try:
                self.history_box.configure(text="\\n".join(f"{r['destination']} — {r['trip_type']} — {r['transport']}" for r in user_hist))
            except Exception:
                pass

        # UNLOCK other tabs
        for tab in [self.hotels_tab, self.budget_tab, self.history_tab, self.checklist_tab]:
            tab._state = ""

    # LOGOUT
    def logout(self):
        self.master.switch_frame(LoginPage)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = GuideMeApp()
    app.mainloop()
