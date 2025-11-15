import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (id INTEGER PRIMARY KEY, user_id INTEGER, weight REAL, height REAL, bmi REAL, category TEXT, date TEXT, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def add_user(name):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        user_id = c.lastrowid
    except sqlite3.IntegrityError:
        c.execute('SELECT id FROM users WHERE name = ?', (name,))
        user_id = c.fetchone()[0]
    conn.close()
    return user_id

def save_bmi(user_id, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO bmi_records (user_id, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)', (user_id, weight, height, bmi, category, date))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('SELECT date, bmi, category FROM bmi_records WHERE user_id = ? ORDER BY date DESC', (user_id,))
    records = c.fetchall()
    conn.close()
    return records

def get_users():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('SELECT id, name FROM users')
    users = c.fetchall()
    conn.close()
    return users

# BMI calculation
def calculate_bmi(weight, height):
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive.")
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

# GUI class
class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("600x500")

        # User selection
        tk.Label(root, text="Select User:").grid(row=0, column=0, padx=10, pady=10)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(root, textvariable=self.user_var)
        self.user_combo.grid(row=0, column=1, padx=10, pady=10)
        self.load_users()

        tk.Button(root, text="New User", command=self.new_user).grid(row=0, column=2, padx=10, pady=10)

        # Input fields
        tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=10)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=10)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=2, column=1, padx=10, pady=10)

        # Calculate button
        tk.Button(root, text="Calculate BMI", command=self.calculate).grid(row=3, column=0, columnspan=3, pady=20)

        # Result display
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=3, pady=10)

        # History button
        tk.Button(root, text="View History", command=self.view_history).grid(row=5, column=0, pady=10)
        tk.Button(root, text="View Trends", command=self.view_trends).grid(row=5, column=1, pady=10)

    def load_users(self):
        users = get_users()
        self.user_combo['values'] = [name for _, name in users]
        self.user_dict = {name: id for id, name in users}

    def new_user(self):
        name = simpledialog.askstring("New User", "Enter user name:")
        if name:
            add_user(name)
            self.load_users()
            self.user_var.set(name)

    def calculate(self):
        try:
            user_name = self.user_var.get()
            if not user_name:
                messagebox.showerror("Error", "Please select a user.")
                return
            user_id = self.user_dict[user_name]
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi, category = calculate_bmi(weight, height)
            save_bmi(user_id, weight, height, bmi, category)
            self.result_label.config(text=f"BMI: {bmi:.2f} - {category}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Invalid input.")

    def view_history(self):
        user_name = self.user_var.get()
        if not user_name:
            messagebox.showerror("Error", "Please select a user.")
            return
        user_id = self.user_dict[user_name]
        records = get_history(user_id)
        if not records:
            messagebox.showinfo("History", "No records found.")
            return
        history_text = "\n".join([f"{date}: BMI {bmi:.2f} - {category}" for date, bmi, category in records])
        messagebox.showinfo("BMI History", history_text)

    def view_trends(self):
        user_name = self.user_var.get()
        if not user_name:
            messagebox.showerror("Error", "Please select a user.")
            return
        user_id = self.user_dict[user_name]
        records = get_history(user_id)
        if len(records) < 2:
            messagebox.showinfo("Trends", "Not enough data for trends.")
            return
        dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date, _, _ in records[::-1]]
        bmis = [bmi for _, bmi, _ in records[::-1]]
        plt.plot(dates, bmis, marker='o')
        plt.title(f"BMI Trends for {user_name}")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
