import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import hashlib
from datetime import datetime, timedelta
import os

class TheMoviesCo:
    def __init__(self, master):
        self.master = master
        self.master.title("The Movies Co.")
        self.master.geometry("520x400")  # Adjusted height to include seat category
        self.master.configure(bg="#F0F0F0")
        
        # Initialize movie details including seats and price
        self.movie_details = {
            "Godzilla x Kong: The New Empire": {
                "INOX: Nehru Place": {"seats": 240, "price": 280},
                "INOX: Janak Place": {"seats": 220, "price": 290},
                "INOX: Insignia At Epicuria, Nehru Place": {"seats": 220, "price": 320},
                "Fun Cinemas: TDI Mall, Moti Nagar": {"seats": 380, "price": 400}},
            
            "Bade Miyan Chote Miyan": {
                "INOX: Nehru Place": {"seats": 240, "price": 230}, 
                "INOX: Janak Place": {"seats": 220, "price": 240}, 
                "INOX: Insignia At Epicuria, Nehru Place": {"seats": 220, "price": 240}, 
                "Fun Cinemas: TDI Mall, Moti Nagar": {"seats": 380, "price": 260}, 
                "Cinepolis: Cross River Mall, Shahdara": {"seats": 240, "price": 300}, 
                "Cinepolis: Janak Cinema, New Delhi": {"seats": 220, "price": 240}},

            "Maidaan": {
                "INOX: Nehru Place": {"seats": 240, "price": 290}, 
                "INOX: Janak Place": {"seats": 220, "price": 310}, 
                "Cinepolis: Janak Cinema, New Delhi": {"seats": 220, "price": 380}, 
                "INOX: Insignia At Epicuria, Nehru Place": {"seats": 220, "price": 430}, 
                "Fun Cinemas: TDI Mall, Moti Nagar": {"seats": 380, "price": 280}, 
                "Cinepolis: Cross River Mall, Shahdara": {"seats": 220, "price": 250}},
            
            "Crew": {
                "INOX: Nehru Place": {"seats": 240, "price": 240}, 
                "INOX: Janak Place": {"seats": 220, "price": 230}, 
                "INOX: Insignia At Epicuria, Nehru Place": {"seats": 220, "price": 410}, 
                "Fun Cinemas: TDI Mall, Moti Nagar": {"seats": 380, "price": 280}},

            "Shaitaan": {
                "INOX: Nehru Place": {"seats": 240, "price": 200}, 
                "INOX: Insignia At Epicuria, Nehru Place": {"seats": 220, "price": 240}, 
                "INOX: Janak Place": {"seats": 220, "price": 230}, 
                "Cinepolis: Janak Cinema, New Delhi": {"seats": 220, "price": 240}, 
                "Cinepolis: Cross River Mall, Shahdara": {"seats": 220, "price": 260}},
            
            "Kung Fu Panda 4": {
                "INOX: Nehru Place": {"seats": 240, "price": 240}, 
                "Fun Cinemas: TDI Mall, Moti Nagar": {"seats": 380, "price": 230}, 
                "INOX: Janak Place": {"seats": 220, "price": 410}, 
                "INOX: Insignia At Epicuria, Nehru Place":{"seats": 220, "price": 190}, 
                "Cinepolis: Janak Cinema, New Delhi": {"seats": 220, "price": 340}},

            "Civil War": {
                "INOX: Nehru Place": {"seats": 240, "price": 310}, 
                "INOX: Insignia At Epicuria, Nehru Place": {"seats": 220, "price": 250}, 
                "INOX: Janak Place": {"seats": 220, "price": 320}, 
                "Fun Cinemas: TDI Mall, Moti Nagar": {"seats": 380, "price": 280}, 
                "Cinepolis: Janak Cinema, New Delhi": {"seats": 220, "price": 260}}
        }

        # Load user details from file
        try:
            with open("user_details.json", "r") as file:
                self.user_details = json.load(file)
        except FileNotFoundError:
            self.user_details = {}

        # Load booking history from file
        try:
            with open("booking_history.json", "r") as file:
                self.booking_history = json.load(file)
        except FileNotFoundError:
            self.booking_history = {}

        # Initialize login_frame attribute
        self.login_frame = None

        # Create login frame
        self.login_frame = tk.Frame(master, bg="#F0F0F0")
        self.login_frame.pack(pady=20)

        # Username and Password Labels and Entry Widgets
        self.label_username = tk.Label(self.login_frame, text="Username:", bg="#F0F0F0", font=("Arial", 12))
        self.label_username.grid(row=0, column=0, pady=5, padx=10, sticky=tk.E)
        self.entry_username = tk.Entry(self.login_frame, font=("Arial", 12))
        self.entry_username.grid(row=0, column=1, pady=5, padx=10)

        self.label_password = tk.Label(self.login_frame, text="Password:", bg="#F0F0F0", font=("Arial", 12))
        self.label_password.grid(row=1, column=0, pady=5, padx=10, sticky=tk.E)
        self.entry_password = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.entry_password.grid(row=1, column=1, pady=5, padx=10)

        # Login Button
        self.button_login = tk.Button(self.login_frame, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)

        # Signup Button
        self.button_signup = tk.Button(self.login_frame, text="Sign Up", command=self.signup, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.button_signup.grid(row=3, column=0, columnspan=2, pady=5)

        # Create booking frame
        self.booking_frame = tk.Frame(master, bg="#F0F0F0")

        # Initialize username variable
        self.username = None
        
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username in self.user_details:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if self.user_details[username] == hashed_password:
                self.username = username  # Store the username
                self.login_frame.destroy()

                # Show booking frame
                self.booking_frame.pack(pady=20)

                # Movie selection label
                self.label_movie = tk.Label(self.booking_frame, text="Select Movie:", bg="#F0F0F0", font=("Arial", 12))
                self.label_movie.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

                # Movie selection dropdown
                self.movie_var = tk.StringVar()
                self.movie_dropdown = ttk.Combobox(self.booking_frame, textvariable=self.movie_var, font=("Arial", 12), width=25)
                self.movie_dropdown['values'] = list(self.movie_details.keys())
                self.movie_dropdown.grid(row=0, column=1, padx=10, pady=5)
                self.movie_dropdown.bind("<<ComboboxSelected>>", self.show_theaters)

                # Theater selection label
                self.label_theater = tk.Label(self.booking_frame, text="Select Theater:", bg="#F0F0F0", font=("Arial", 12))
                self.label_theater.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

                # Theater selection dropdown
                self.theater_var = tk.StringVar()
                self.theater_dropdown = ttk.Combobox(self.booking_frame, textvariable=self.theater_var, font=("Arial", 12), width=25)
                self.theater_dropdown.grid(row=1, column=1, padx=10, pady=5)

                # Date selection label
                self.label_date = tk.Label(self.booking_frame, text="Select Date:", bg="#F0F0F0", font=("Arial", 12))
                self.label_date.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

                # Date selection dropdown
                self.date_var = tk.StringVar()
                self.date_dropdown = ttk.Combobox(self.booking_frame, textvariable=self.date_var, font=("Arial", 12), width=25)
                self.date_dropdown.grid(row=2, column=1, padx=10, pady=5)
                self.populate_dates()

                # Seat category label
                self.label_seat_category = tk.Label(self.booking_frame, text="Seat Category:", bg="#F0F0F0", font=("Arial", 12))
                self.label_seat_category.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

                # Seat category dropdown
                self.seat_category_var = tk.StringVar()
                self.seat_category_dropdown = ttk.Combobox(self.booking_frame, textvariable=self.seat_category_var, font=("Arial", 12), width=25)
                self.seat_category_dropdown['values'] = ["Regular", "Premium", "Recliner"]
                self.seat_category_dropdown.grid(row=3, column=1, padx=10, pady=5)

                # Number of tickets label
                self.label_tickets = tk.Label(self.booking_frame, text="Number of Tickets:", bg="#F0F0F0", font=("Arial", 12))
                self.label_tickets.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

                # Number of tickets entry
                self.entry_tickets = tk.Entry(self.booking_frame, font=("Arial", 12))
                self.entry_tickets.grid(row=4, column=1, padx=10, pady=5)

                # Book button
                self.button_book = tk.Button(self.booking_frame, text="Book", command=self.book_tickets, bg="#4CAF50", fg="white", font=("Arial", 12))
                self.button_book.grid(row=5, column=0, columnspan=2, pady=10)

                # Booking history button
                self.button_history = tk.Button(self.booking_frame, text="Booking History", command=self.show_booking_history, bg="#4CAF50", fg="white", font=("Arial", 12))
                self.button_history.grid(row=6, column=0, columnspan=2, pady=5)
            else:
                messagebox.showerror("Login Error", "Invalid username or password")
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def signup(self):
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("400x300")
        signup_window.configure(bg="#F0F0F0")

        label_new_username = tk.Label(signup_window, text="New Username:", bg="#F0F0F0", font=("Arial", 12))
        label_new_username.pack(pady=10)
        entry_new_username = tk.Entry(signup_window, font=("Arial", 12))
        entry_new_username.pack(pady=5)

        label_new_password = tk.Label(signup_window, text="New Password:", bg="#F0F0F0", font=("Arial", 12))
        label_new_password.pack(pady=10)
        entry_new_password = tk.Entry(signup_window, show="*", font=("Arial", 12))
        entry_new_password.pack(pady=5)

        def create_account():
            new_username = entry_new_username.get()
            new_password = entry_new_password.get()
            if new_username and new_password:
                if new_username not in self.user_details:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    self.user_details[new_username] = hashed_password
                    with open("user_details.json", "w") as file:
                        json.dump(self.user_details, file)
                    messagebox.showinfo("Success", "Account created successfully!")
                    signup_window.destroy()
                else:
                    messagebox.showerror("Error", "Username already exists")
            else:
                messagebox.showerror("Error", "Please enter both username and password")

        button_create_account = tk.Button(signup_window, text="Create Account", command=create_account, bg="#4CAF50", fg="white", font=("Arial", 12))
        button_create_account.pack(pady=20)

    def show_theaters(self, event):
        selected_movie = self.movie_var.get()
        if selected_movie:
            theaters = list(self.movie_details[selected_movie].keys())
            self.theater_dropdown['values'] = theaters

    def populate_dates(self):
        today = datetime.today()
        dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        self.date_dropdown['values'] = dates

    def book_tickets(self):
        selected_movie = self.movie_var.get()
        selected_theater = self.theater_var.get()
        selected_date = self.date_var.get()
        selected_seat_category = self.seat_category_var.get()
        num_tickets = self.entry_tickets.get()

        if not (selected_movie and selected_theater and selected_date and selected_seat_category and num_tickets):
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            num_tickets = int(num_tickets)
        except ValueError:
            messagebox.showerror("Error", "Number of tickets must be an integer")
            return

        available_seats = self.movie_details[selected_movie][selected_theater]["seats"]
        base_price_per_ticket = self.movie_details[selected_movie][selected_theater]["price"]

        # Adjust price based on seat category
        seat_category_multiplier = {
            "Regular": 1.0,
            "Premium": 2.0,
            "Recliner": 3.0
        }
        price_per_ticket = base_price_per_ticket * seat_category_multiplier[selected_seat_category]

        if num_tickets > available_seats:
            messagebox.showerror("Error", f"Only {available_seats} seats available")
            return

        total_cost = num_tickets * price_per_ticket
        gst = total_cost * 0.18
        total_cost_with_gst = total_cost + gst

        self.movie_details[selected_movie][selected_theater]["seats"] -= num_tickets

        if self.username not in self.booking_history:
            self.booking_history[self.username] = []

        self.booking_history[self.username].append({
            "movie": selected_movie,
            "theater": selected_theater,
            "date": selected_date,
            "seat_category": selected_seat_category,
            "num_tickets": num_tickets,
            "price_per_ticket": round(price_per_ticket, 2),
            "total_cost": round(total_cost, 2),
            "gst": round(gst, 2),
            "total_cost_with_gst": round(total_cost_with_gst, 2)
        })

        # Save booking history to file
        with open("booking_history.json", "w") as file:
            json.dump(self.booking_history, file)

        bill_details = f"""
        Movie: {selected_movie}
        Theater: {selected_theater}
        Date: {selected_date}
        Seat Category: {selected_seat_category}
        Number of Tickets: {num_tickets}
        Price per Ticket: ₹{price_per_ticket:.2f}
        Total Cost (before GST): ₹{total_cost:.2f}
        GST (18%): ₹{gst:.2f}
        Total Cost (including GST): ₹{total_cost_with_gst:.2f}
        """

        messagebox.showinfo("Booking Confirmation", f"Tickets booked successfully!\n\n{bill_details}")

    def show_booking_history(self):
        if self.username not in self.booking_history or not self.booking_history[self.username]:
            messagebox.showinfo("Booking History", "No booking history found")
            return

        history_window = tk.Toplevel(self.master)
        history_window.title("Booking History")
        history_window.geometry("500x400")
        history_window.configure(bg="#F0F0F0")

        text_history = tk.Text(history_window, font=("Arial", 12))
        text_history.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        for booking in self.booking_history[self.username]:
            booking_details = f"""
            Movie: {booking['movie']}
            Theater: {booking['theater']}
            Date: {booking['date']}
            Seat Category: {booking['seat_category']}
            Number of Tickets: {booking['num_tickets']}
            Price per Ticket: ₹{booking['price_per_ticket']:.2f}
            Total Cost (before GST): ₹{booking['total_cost']:.2f}
            GST (18%): ₹{booking['gst']:.2f}
            Total Cost (including GST): ₹{booking['total_cost_with_gst']:.2f}
            """
            text_history.insert(tk.END, booking_details + "\n" + "-"*40 + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TheMoviesCo(root)
    root.mainloop()
