import customtkinter as ctk
from tkinter import messagebox
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- USERS FILE ----------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- DESTINATIONS ----------------
DESTINATION_SUGGESTIONS = {
    "Beach": ["Goa", "Kovalam", "Pondicherry", "Varkala"],
    "City": ["Bangalore", "Mumbai", "Delhi", "Hyderabad"],
    "Mountains": ["Manali", "Ooty", "Munnar", "Darjeeling"],
    "International": ["Dubai", "Singapore", "Paris", "Maldives"]
}

TRIP_DURATIONS = ["1–3 Days", "4–7 Days", "1–2 Weeks", "1+ Month"]

# ---------------- OFFLINE HOTEL DATABASE ----------------
HOTELS_BY_LOCATION = {
    # Beach
    "goa": ["Taj Exotica Resort", "The Leela Goa", "Park Hyatt Goa", "ITC Grand Goa"],
    "kovalam": ["The Leela Kovalam", "Turtle On The Beach", "UDS Hotel"],
    "pondicherry": ["Promenade Hotel", "Le Dupleix", "Accord Puducherry"],
    "varkala": ["Gateway Varkala", "Clafouti Beach Resort", "Hindustan Beach Retreat"],

    # Cities
    "mumbai": ["Taj Mahal Palace", "The Oberoi", "Trident Nariman Point"],
    "bangalore": ["The Ritz-Carlton", "Taj MG Road", "JW Marriott"],
    "delhi": ["The Imperial", "Taj Palace", "ITC Maurya"],
    "hyderabad": ["ITC Kohenur", "Taj Deccan", "Novotel HICC"],

    # Mountains
    "manali": ["Solang Valley Resort", "Apple Country Resort", "Johnson Lodge"],
    "ooty": ["Savoy Ooty", "Hotel Gem Park", "Sterling Ooty"],
    "munnar": ["Tea County", "Amber Dale Munnar", "Windermere Estate"],
    "darjeeling": ["The Elgin", "Mayfair Darjeeling", "Cedar Inn"],

    # International
    "dubai": ["Atlantis The Palm", "Burj Al Arab", "Rove Downtown"],
    "singapore": ["Marina Bay Sands", "Pan Pacific", "V Hotel Lavender"],
    "paris": ["Le Meurice", "Hotel Napoleon", "Shangri-La Paris"],
    "maldives": ["Soneva Fushi", "Sun Siyam Iru Fushi", "Adaaran Prestige"]
}

# ---------------- APP ----------------
class GuideMeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GuideMe — Travel App")
        self.geometry("500x700")
        self.users = load_users()
        self.active_frame = None
        self.configure(fg_color="#E0F7FA")

        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class, **kwargs):
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = frame_class(self, **kwargs)
        self.active_frame.pack(expand=True, fill="both")

# ---------------- LOGIN ----------------
class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#B2EBF2")
        ctk.CTkLabel(self, text="GuideMe", font=("Blackadder ITC", 36, "bold"), text_color="#0D47A1").pack(pady=25)

        self.username = ctk.CTkEntry(self, placeholder_text="Username", width=280, height=40)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=280, height=40)
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Login", width=220, fg_color="#00796B", hover_color="#004D40",
                       text_color="white", command=self.login).pack(pady=10)

        ctk.CTkButton(self, text="Create Account", width=220, fg_color="#FFA000", hover_color="#FF6F00",
                       text_color="white", command=lambda: master.switch_frame(SignupPage)).pack(pady=5)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in self.master.users and self.master.users[user] == pwd:
            messagebox.showinfo("Success", f"Welcome {user}!")
            self.master.switch_frame(TripPage, username=user)
        else:
            messagebox.showerror("Error", "Invalid username or password")

# ---------------- SIGNUP ----------------
class SignupPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#B2EBF2")
        ctk.CTkLabel(self, text="Create Account", font=("Blackadder ITC", 32), text_color="#0D47A1").pack(pady=25)

        self.username = ctk.CTkEntry(self, placeholder_text="Choose Username", width=280)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Choose Password", show="*", width=280)
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Sign Up", width=220, fg_color="#00796B", hover_color="#004D40",
                       text_color="white", command=self.signup).pack(pady=10)

        ctk.CTkButton(self, text="Back to Login", width=220, fg_color="#FFA000", hover_color="#FF6F00",
                       text_color="white", command=lambda: master.switch_frame(LoginPage)).pack(pady=5)

    def signup(self):
        user = self.username.get()
        pwd = self.password.get()

        if not user or not pwd:
            messagebox.showwarning("Error", "Please fill all fields")
            return

        if user in self.master.users:
            messagebox.showerror("Error", "Username already taken")
            return

        self.master.users[user] = pwd
        save_users(self.master.users)

        messagebox.showinfo("Success", "Account created!")
        self.master.switch_frame(LoginPage)

# ---------------- TRIP PAGE ----------------
class TripPage(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master, fg_color="#F5F7FA")
        self.master = master
        self.username = username

        ctk.CTkLabel(self, text=f"Welcome {username} ✨", font=("Segoe UI", 26, "bold"),
                     text_color="#0D47A1").pack(pady=20)

        self.tabs = ctk.CTkTabview(self, width=420, height=520)
        self.tabs.pack(pady=10)

        self.tab_plan = self.tabs.add("Plan Trip")
        self.tab_hotels = self.tabs.add("Hotels & Rest")
        self.tab_checklist = self.tabs.add("Checklist")
        self.tab_budget = self.tabs.add("Budget Manager")

        self.build_plan_tab()
        self.build_hotel_tab()
        self.build_checklist_tab()
        self.build_budget_tab()

    # ---------------- PLAN TAB ----------------
    def build_plan_tab(self):
        ctk.CTkLabel(self.tab_plan, text="Trip Type").pack(pady=5)
        self.trip_type = ctk.CTkComboBox(self.tab_plan, values=list(DESTINATION_SUGGESTIONS.keys()), width=250)
        self.trip_type.pack()

        ctk.CTkLabel(self.tab_plan, text="Destination").pack(pady=5)
        self.dest_entry = ctk.CTkEntry(self.tab_plan, width=250)
        self.dest_entry.pack()

        ctk.CTkLabel(self.tab_plan, text="Trip Duration").pack(pady=5)
        self.duration_box = ctk.CTkComboBox(self.tab_plan, values=TRIP_DURATIONS, width=250)
        self.duration_box.pack()

        ctk.CTkLabel(self.tab_plan, text="Budget (₹)").pack(pady=5)
        self.budget_entry = ctk.CTkEntry(self.tab_plan, width=250)
        self.budget_entry.pack()

        ctk.CTkButton(self.tab_plan, text="Save Trip", fg_color="#00BFA5", width=200,
                      command=self.save_trip).pack(pady=20)

    def save_trip(self):
        self.destination = self.dest_entry.get().strip()
        self.duration = self.duration_box.get()
        self.budget = self.budget_entry.get()

        self.update_hotels_based_on_destination()

        messagebox.showinfo("Saved", "Trip details saved successfully!")

    # ---------------- HOTEL TAB ----------------
    def build_hotel_tab(self):
        ctk.CTkLabel(self.tab_hotels, text="Recommended Hotels",
                     font=("Segoe UI", 18, "bold")).pack(pady=10)

        self.hotel_list = ctk.CTkTextbox(self.tab_hotels, width=360, height=350)
        self.hotel_list.pack(pady=10)

    def update_hotels_based_on_destination(self):
        place = self.dest_entry.get().strip().lower()

        hotels = HOTELS_BY_LOCATION.get(place, [
            "Taj Hotel",
            "Lemon Tree",
            "Treebo",
            "OYO Premium"
        ])

        self.hotel_list.delete("1.0", "end")

        self.hotel_list.insert("end", f"🏨 Hotels in {self.dest_entry.get()}:\n\n")
        for h in hotels:
            self.hotel_list.insert("end", f"• {h}\n")

        self.hotel_list.insert("end", "\n🛑 Rest Areas:\n➡ Highway Dhaba\n➡ Fuel + Rest Lounge\n➡ Food Junction")

    # ---------------- CHECKLIST TAB ----------------
    def build_checklist_tab(self):
        ctk.CTkLabel(self.tab_checklist, text="Smart Packing Checklist",
                     font=("Segoe UI", 18, "bold")).pack(pady=10)

        frame = ctk.CTkScrollableFrame(self.tab_checklist, width=360, height=350)
        frame.pack(pady=10)

        self.check_vars = []
        items = ["Clothes", "Toothbrush", "Phone Charger", "Medications",
                 "Water Bottle", "Power Bank", "Travel Documents"]

        for item in items:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(frame, text=item, variable=var).pack(anchor="w")
            self.check_vars.append((var, item))

        ctk.CTkButton(self.tab_checklist, text="Show Selected",
                      fg_color="#00BFA5", command=self.show_checked).pack(pady=10)

    def show_checked(self):
        selected = [item for var, item in self.check_vars if var.get()]
        messagebox.showinfo("Items", "\n".join(selected) if selected else "No items selected.")

    # ---------------- BUDGET MANAGER TAB ----------------
    def build_budget_tab(self):
        ctk.CTkLabel(self.tab_budget, text="Budget Manager", font=("Segoe UI", 20, "bold"),
                     text_color="#0D47A1").pack(pady=10)

        ctk.CTkLabel(self.tab_budget, text="Enter Total Budget (₹):",
                     text_color="#004D40").pack()

        self.total_budget_entry = ctk.CTkEntry(self.tab_budget, width=200)
        self.total_budget_entry.pack(pady=5)

        ctk.CTkButton(self.tab_budget, text="Set Budget",
                      fg_color="#009688", hover_color="#004D40",
                      command=self.set_budget).pack(pady=10)

        ctk.CTkLabel(self.tab_budget, text="Add Daily Expense (₹):",
                     text_color="#004D40").pack(pady=5)

        self.daily_expense_entry = ctk.CTkEntry(self.tab_budget, width=200)
        self.daily_expense_entry.pack()

        ctk.CTkButton(self.tab_budget, text="Add Expense",
                      fg_color="#FFA000", hover_color="#FF6F00",
                      command=self.add_daily_expense).pack(pady=10)

        self.budget_status_label = ctk.CTkLabel(self.tab_budget, text="",
                                                text_color="#00796B")
        self.budget_status_label.pack(pady=10)

        self.expenses = []
        self.total_budget = 0

        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_budget)
        self.canvas.get_tk_widget().pack(pady=10)

        self.update_budget_graph()

    # ---------------- BUDGET FUNCTIONS ----------------
    def set_budget(self):
        try:
            self.total_budget = float(self.total_budget_entry.get())
            self.budget_status_label.configure(text=f"Total Budget: ₹{self.total_budget}")
        except:
            messagebox.showerror("Error", "Invalid number")

    def add_daily_expense(self):
        try:
            amount = float(self.daily_expense_entry.get())
            self.expenses.append(amount)
            self.daily_expense_entry.delete(0, "end")
            self.update_budget_status()
            self.update_budget_graph()
        except:
            messagebox.showerror("Error", "Invalid amount")

    def update_budget_status(self):
        spent = sum(self.expenses)
        remaining = self.total_budget - spent

        if remaining < 0:
            color = "red"
            warn = "⚠ Budget Exceeded!"
        elif remaining <= self.total_budget * 0.2:
            color = "#FF6F00"
            warn = "⚠ 20% Budget Remaining"
        else:
            color = "#00796B"
            warn = ""

        self.budget_status_label.configure(
            text=f"Spent: ₹{spent:.2f}\nRemaining: ₹{remaining:.2f}\n{warn}",
            text_color=color
        )

    def update_budget_graph(self):
        self.ax.clear()

        if self.expenses:
            self.ax.plot(self.expenses, marker="o", color="#00897B",
                         label="Daily Expenses")

        if self.total_budget > 0:
            self.ax.axhline(self.total_budget, color="#FFA000",
                            linestyle="--", label="Budget Limit")

        self.ax.set_title("Daily Expense Trend", color="#004D40")
        self.ax.set_xlabel("Day", color="#004D40")
        self.ax.set_ylabel("Amount (₹)", color="#004D40")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        self.ax.legend()

        self.canvas.draw()


# ---------------- RUN APP ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = GuideMeApp()
app.mainloop()
import customtkinter as ctk
from tkinter import messagebox
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- USERS FILE ----------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- DESTINATIONS ----------------
DESTINATION_SUGGESTIONS = {
    "Beach": ["Goa", "Kovalam", "Pondicherry", "Varkala"],
    "City": ["Bangalore", "Mumbai", "Delhi", "Hyderabad"],
    "Mountains": ["Manali", "Ooty", "Munnar", "Darjeeling"],
    "International": ["Dubai", "Singapore", "Paris", "Maldives"]
}

TRIP_DURATIONS = ["1–3 Days", "4–7 Days", "1–2 Weeks", "1+ Month"]

# ---------------- OFFLINE HOTEL DATABASE ----------------
HOTELS_BY_LOCATION = {
    # Beach
    "goa": ["Taj Exotica Resort", "The Leela Goa", "Park Hyatt Goa", "ITC Grand Goa"],
    "kovalam": ["The Leela Kovalam", "Turtle On The Beach", "UDS Hotel"],
    "pondicherry": ["Promenade Hotel", "Le Dupleix", "Accord Puducherry"],
    "varkala": ["Gateway Varkala", "Clafouti Beach Resort", "Hindustan Beach Retreat"],

    # Cities
    "mumbai": ["Taj Mahal Palace", "The Oberoi", "Trident Nariman Point"],
    "bangalore": ["The Ritz-Carlton", "Taj MG Road", "JW Marriott"],
    "delhi": ["The Imperial", "Taj Palace", "ITC Maurya"],
    "hyderabad": ["ITC Kohenur", "Taj Deccan", "Novotel HICC"],

    # Mountains
    "manali": ["Solang Valley Resort", "Apple Country Resort", "Johnson Lodge"],
    "ooty": ["Savoy Ooty", "Hotel Gem Park", "Sterling Ooty"],
    "munnar": ["Tea County", "Amber Dale Munnar", "Windermere Estate"],
    "darjeeling": ["The Elgin", "Mayfair Darjeeling", "Cedar Inn"],

    # International
    "dubai": ["Atlantis The Palm", "Burj Al Arab", "Rove Downtown"],
    "singapore": ["Marina Bay Sands", "Pan Pacific", "V Hotel Lavender"],
    "paris": ["Le Meurice", "Hotel Napoleon", "Shangri-La Paris"],
    "maldives": ["Soneva Fushi", "Sun Siyam Iru Fushi", "Adaaran Prestige"]
}

# ---------------- APP ----------------
class GuideMeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GuideMe — Travel App")
        self.geometry("500x700")
        self.users = load_users()
        self.active_frame = None
        self.configure(fg_color="#E0F7FA")

        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class, **kwargs):
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = frame_class(self, **kwargs)
        self.active_frame.pack(expand=True, fill="both")

# ---------------- LOGIN ----------------
class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#B2EBF2")
        ctk.CTkLabel(self, text="GuideMe", font=("Blackadder ITC", 36, "bold"), text_color="#0D47A1").pack(pady=25)

        self.username = ctk.CTkEntry(self, placeholder_text="Username", width=280, height=40)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=280, height=40)
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Login", width=220, fg_color="#00796B", hover_color="#004D40",
                       text_color="white", command=self.login).pack(pady=10)

        ctk.CTkButton(self, text="Create Account", width=220, fg_color="#FFA000", hover_color="#FF6F00",
                       text_color="white", command=lambda: master.switch_frame(SignupPage)).pack(pady=5)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in self.master.users and self.master.users[user] == pwd:
            messagebox.showinfo("Success", f"Welcome {user}!")
            self.master.switch_frame(TripPage, username=user)
        else:
            messagebox.showerror("Error", "Invalid username or password")

# ---------------- SIGNUP ----------------
class SignupPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#B2EBF2")
        ctk.CTkLabel(self, text="Create Account", font=("Blackadder ITC", 32), text_color="#0D47A1").pack(pady=25)

        self.username = ctk.CTkEntry(self, placeholder_text="Choose Username", width=280)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Choose Password", show="*", width=280)
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Sign Up", width=220, fg_color="#00796B", hover_color="#004D40",
                       text_color="white", command=self.signup).pack(pady=10)

        ctk.CTkButton(self, text="Back to Login", width=220, fg_color="#FFA000", hover_color="#FF6F00",
                       text_color="white", command=lambda: master.switch_frame(LoginPage)).pack(pady=5)

    def signup(self):
        user = self.username.get()
        pwd = self.password.get()

        if not user or not pwd:
            messagebox.showwarning("Error", "Please fill all fields")
            return

        if user in self.master.users:
            messagebox.showerror("Error", "Username already taken")
            return

        self.master.users[user] = pwd
        save_users(self.master.users)

        messagebox.showinfo("Success", "Account created!")
        self.master.switch_frame(LoginPage)

# ---------------- TRIP PAGE ----------------
class TripPage(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master, fg_color="#F5F7FA")
        self.master = master
        self.username = username

        ctk.CTkLabel(self, text=f"Welcome {username} ✨", font=("Segoe UI", 26, "bold"),
                     text_color="#0D47A1").pack(pady=20)

        self.tabs = ctk.CTkTabview(self, width=420, height=520)
        self.tabs.pack(pady=10)

        self.tab_plan = self.tabs.add("Plan Trip")
        self.tab_hotels = self.tabs.add("Hotels & Rest")
        self.tab_checklist = self.tabs.add("Checklist")
        self.tab_budget = self.tabs.add("Budget Manager")

        self.build_plan_tab()
        self.build_hotel_tab()
        self.build_checklist_tab()
        self.build_budget_tab()

    # ---------------- PLAN TAB ----------------
    def build_plan_tab(self):
        ctk.CTkLabel(self.tab_plan, text="Trip Type").pack(pady=5)
        self.trip_type = ctk.CTkComboBox(self.tab_plan, values=list(DESTINATION_SUGGESTIONS.keys()), width=250)
        self.trip_type.pack()

        ctk.CTkLabel(self.tab_plan, text="Destination").pack(pady=5)
        self.dest_entry = ctk.CTkEntry(self.tab_plan, width=250)
        self.dest_entry.pack()

        ctk.CTkLabel(self.tab_plan, text="Trip Duration").pack(pady=5)
        self.duration_box = ctk.CTkComboBox(self.tab_plan, values=TRIP_DURATIONS, width=250)
        self.duration_box.pack()

        ctk.CTkLabel(self.tab_plan, text="Budget (₹)").pack(pady=5)
        self.budget_entry = ctk.CTkEntry(self.tab_plan, width=250)
        self.budget_entry.pack()

        ctk.CTkButton(self.tab_plan, text="Save Trip", fg_color="#00BFA5", width=200,
                      command=self.save_trip).pack(pady=20)

    def save_trip(self):
        self.destination = self.dest_entry.get().strip()
        self.duration = self.duration_box.get()
        self.budget = self.budget_entry.get()

        self.update_hotels_based_on_destination()

        messagebox.showinfo("Saved", "Trip details saved successfully!")

    # ---------------- HOTEL TAB ----------------
    def build_hotel_tab(self):
        ctk.CTkLabel(self.tab_hotels, text="Recommended Hotels",
                     font=("Segoe UI", 18, "bold")).pack(pady=10)

        self.hotel_list = ctk.CTkTextbox(self.tab_hotels, width=360, height=350)
        self.hotel_list.pack(pady=10)

    def update_hotels_based_on_destination(self):
        place = self.dest_entry.get().strip().lower()

        hotels = HOTELS_BY_LOCATION.get(place, [
            "Taj Hotel",
            "Lemon Tree",
            "Treebo",
            "OYO Premium"
        ])

        self.hotel_list.delete("1.0", "end")

        self.hotel_list.insert("end", f"🏨 Hotels in {self.dest_entry.get()}:\n\n")
        for h in hotels:
            self.hotel_list.insert("end", f"• {h}\n")

        self.hotel_list.insert("end", "\n🛑 Rest Areas:\n➡ Highway Dhaba\n➡ Fuel + Rest Lounge\n➡ Food Junction")

    # ---------------- CHECKLIST TAB ----------------
    def build_checklist_tab(self):
        ctk.CTkLabel(self.tab_checklist, text="Smart Packing Checklist",
                     font=("Segoe UI", 18, "bold")).pack(pady=10)

        frame = ctk.CTkScrollableFrame(self.tab_checklist, width=360, height=350)
        frame.pack(pady=10)

        self.check_vars = []
        items = ["Clothes", "Toothbrush", "Phone Charger", "Medications",
                 "Water Bottle", "Power Bank", "Travel Documents"]

        for item in items:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(frame, text=item, variable=var).pack(anchor="w")
            self.check_vars.append((var, item))

        ctk.CTkButton(self.tab_checklist, text="Show Selected",
                      fg_color="#00BFA5", command=self.show_checked).pack(pady=10)

    def show_checked(self):
        selected = [item for var, item in self.check_vars if var.get()]
        messagebox.showinfo("Items", "\n".join(selected) if selected else "No items selected.")

    # ---------------- BUDGET MANAGER TAB ----------------
    def build_budget_tab(self):
        ctk.CTkLabel(self.tab_budget, text="Budget Manager", font=("Segoe UI", 20, "bold"),
                     text_color="#0D47A1").pack(pady=10)

        ctk.CTkLabel(self.tab_budget, text="Enter Total Budget (₹):",
                     text_color="#004D40").pack()

        self.total_budget_entry = ctk.CTkEntry(self.tab_budget, width=200)
        self.total_budget_entry.pack(pady=5)

        ctk.CTkButton(self.tab_budget, text="Set Budget",
                      fg_color="#009688", hover_color="#004D40",
                      command=self.set_budget).pack(pady=10)

        ctk.CTkLabel(self.tab_budget, text="Add Daily Expense (₹):",
                     text_color="#004D40").pack(pady=5)

        self.daily_expense_entry = ctk.CTkEntry(self.tab_budget, width=200)
        self.daily_expense_entry.pack()

        ctk.CTkButton(self.tab_budget, text="Add Expense",
                      fg_color="#FFA000", hover_color="#FF6F00",
                      command=self.add_daily_expense).pack(pady=10)

        self.budget_status_label = ctk.CTkLabel(self.tab_budget, text="",
                                                text_color="#00796B")
        self.budget_status_label.pack(pady=10)

        self.expenses = []
        self.total_budget = 0

        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_budget)
        self.canvas.get_tk_widget().pack(pady=10)

        self.update_budget_graph()

    # ---------------- BUDGET FUNCTIONS ----------------
    def set_budget(self):
        try:
            self.total_budget = float(self.total_budget_entry.get())
            self.budget_status_label.configure(text=f"Total Budget: ₹{self.total_budget}")
        except:
            messagebox.showerror("Error", "Invalid number")

    def add_daily_expense(self):
        try:
            amount = float(self.daily_expense_entry.get())
            self.expenses.append(amount)
            self.daily_expense_entry.delete(0, "end")
            self.update_budget_status()
            self.update_budget_graph()
        except:
            messagebox.showerror("Error", "Invalid amount")

    def update_budget_status(self):
        spent = sum(self.expenses)
        remaining = self.total_budget - spent

        if remaining < 0:
            color = "red"
            warn = "⚠ Budget Exceeded!"
        elif remaining <= self.total_budget * 0.2:
            color = "#FF6F00"
            warn = "⚠ 20% Budget Remaining"
        else:
            color = "#00796B"
            warn = ""

        self.budget_status_label.configure(
            text=f"Spent: ₹{spent:.2f}\nRemaining: ₹{remaining:.2f}\n{warn}",
            text_color=color
        )

    def update_budget_graph(self):
        self.ax.clear()

        if self.expenses:
            self.ax.plot(self.expenses, marker="o", color="#00897B",
                         label="Daily Expenses")

        if self.total_budget > 0:
            self.ax.axhline(self.total_budget, color="#FFA000",
                            linestyle="--", label="Budget Limit")

        self.ax.set_title("Daily Expense Trend", color="#004D40")
        self.ax.set_xlabel("Day", color="#004D40")
        self.ax.set_ylabel("Amount (₹)", color="#004D40")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        self.ax.legend()

        self.canvas.draw()


# ---------------- RUN APP ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = GuideMeApp()
app.mainloop()
