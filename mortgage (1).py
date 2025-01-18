
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use("TkAgg")

class MortgageCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mortgage Calculator App")
        self.root.geometry("800x600")

        # Color Schemes
        self.light_mode_colors = {
            'background': '#F7EFE5',
            'primary': '#E2BFD9',
            'accent': '#C8A1E0',
            'text': '#674188'
        }
        self.dark_mode_colors = {
            'background': '#674188',
            'primary': '#C8A1E0',
            'accent': '#E2BFD9',
            'text': '#F7EFE5'
        }
        self.is_dark_mode = False
        self.current_colors = self.light_mode_colors

        # Profile data
        self.profile_data = {
            'name': '',
            'email': '',
            'income': '',
            'expenses': '',
            'credit_score': ''
        }

        # Create main frame
        self.main_frame = tk.Frame(root, bg=self.current_colors['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create menu frame
        self.menu_frame = tk.Frame(self.main_frame, bg=self.current_colors['primary'], width=200)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.current_colors['background'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create pages
        self.create_menu()
        self.create_home_page()
        self.create_calculator_page()
        self.create_reminders_page()
        self.create_profile_page()

        # Show the home page initially
        self.show_home()

    def create_menu(self):
        menu_buttons = [
            ('Home', self.show_home),
            ('Calculator', self.show_calculator),
            ('Reminders', self.show_reminders),
            ('Profile', self.show_profile),
            ('Toggle Dark/Light Mode', self.toggle_mode)
        ]
        for text, command in menu_buttons:
            tk.Button(self.menu_frame, text=text, command=command, bg=self.current_colors['accent'], fg=self.current_colors['text'], font=("Arial", 12, "bold"), relief=tk.RAISED).pack(padx=5, pady=5, fill=tk.X)

    def create_home_page(self):
        self.home_frame = tk.Frame(self.content_frame, bg=self.current_colors['background'])
        tk.Label(self.home_frame, text="Welcome to the Mortgage Calculator App!", font=("Arial", 20, "bold"), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=20)
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    def create_calculator_page(self):
        self.calculator_frame = tk.Frame(self.content_frame, bg=self.current_colors['background'])
        tk.Label(self.calculator_frame, text="Mortgage Calculator", font=("Arial", 18, "bold"), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=10)

        self.home_price_var = tk.StringVar()
        self.down_payment_var = tk.StringVar()
        self.interest_rate_var = tk.StringVar()
        self.property_tax_var = tk.StringVar()

        tk.Label(self.calculator_frame, text="Home Price (₹):", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.calculator_frame, textvariable=self.home_price_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.calculator_frame, text="Down Payment (₹):", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.calculator_frame, textvariable=self.down_payment_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.calculator_frame, text="Interest Rate (%):", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.calculator_frame, textvariable=self.interest_rate_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.calculator_frame, text="Property Tax Rate (%):", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.calculator_frame, textvariable=self.property_tax_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.calculator_frame, text="Loan Program:", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        self.loan_program_var = tk.StringVar(value="Fixed Rate")
        self.loan_program_menu = tk.OptionMenu(self.calculator_frame, self.loan_program_var, "Fixed Rate", "Adjustable Rate")
        self.loan_program_menu.config(font=("Arial", 14), bg=self.current_colors['background'])
        self.loan_program_menu.pack(pady=5)
        self.loan_program_var.trace_add("write", self.on_loan_program_selected)

        tk.Button(self.calculator_frame, text="Calculate Payment", command=self.calculate_payment, bg=self.current_colors['accent'], fg=self.current_colors['text'], font=("Arial", 12, "bold"), relief=tk.RAISED).pack(pady=10)

        self.result_var = tk.StringVar()
        self.result_label = tk.Label(self.calculator_frame, textvariable=self.result_var, font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.result_label.pack(pady=10)

        self.calculator_frame.pack(fill=tk.BOTH, expand=True)

    def create_reminders_page(self):
        self.reminders_frame = tk.Frame(self.content_frame, bg=self.current_colors['background'])
        tk.Label(self.reminders_frame, text="Daily Reminders", font=("Arial", 18, "bold"), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=10)

        self.due_dates_text = tk.Label(self.reminders_frame, font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.due_dates_text.pack(pady=10)

        self.calendar_frame = tk.Frame(self.reminders_frame, bg=self.current_colors['background'])
        self.calendar_frame.pack(pady=10)

        self.chart_frame = tk.Frame(self.reminders_frame, bg=self.current_colors['background'])
        self.chart_frame.pack(pady=10)

        self.reminders_frame.pack(fill=tk.BOTH, expand=True)

    def create_profile_page(self):
        self.profile_frame = tk.Frame(self.content_frame, bg=self.current_colors['background'])

        self.profile_label = tk.Label(self.profile_frame, text="User Profile", font=("Arial", 18, "bold"), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.profile_label.pack(pady=10)

        self.profile_name_label = tk.Label(self.profile_frame, text=f"Name: {self.profile_data['name']}", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.profile_name_label.pack(pady=5)

        self.profile_email_label = tk.Label(self.profile_frame, text=f"Email Address: {self.profile_data['email']}", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.profile_email_label.pack(pady=5)

        self.profile_income_label = tk.Label(self.profile_frame, text=f"Monthly Income (₹): {self.profile_data['income']}", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.profile_income_label.pack(pady=5)

        self.profile_expenses_label = tk.Label(self.profile_frame, text=f"Monthly Expenses (₹): {self.profile_data['expenses']}", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.profile_expenses_label.pack(pady=5)

        self.profile_credit_score_label = tk.Label(self.profile_frame, text=f"Credit Score: {self.profile_data['credit_score']}", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        self.profile_credit_score_label.pack(pady=5)

        tk.Button(self.profile_frame, text="Edit Profile", command=self.edit_profile, bg=self.current_colors['accent'], fg=self.current_colors['text'], font=("Arial", 12, "bold"), relief=tk.RAISED).pack(pady=10)

        self.profile_frame.pack(fill=tk.BOTH, expand=True)

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.current_colors = self.dark_mode_colors if self.is_dark_mode else self.light_mode_colors
        self.update_colors()

    def update_colors(self):
        self.main_frame.config(bg=self.current_colors['background'])
        self.menu_frame.config(bg=self.current_colors['primary'])
        self.content_frame.config(bg=self.current_colors['background'])
        self.home_frame.config(bg=self.current_colors['background'])
        self.calculator_frame.config(bg=self.current_colors['background'])
        self.reminders_frame.config(bg=self.current_colors['background'])
        self.profile_frame.config(bg=self.current_colors['background'])
        self.update_reminders()

    def show_home(self):
        self.clear_content_frame()
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    def show_calculator(self):
        self.clear_content_frame()
        self.calculator_frame.pack(fill=tk.BOTH, expand=True)

    def show_reminders(self):
        self.clear_content_frame()
        self.update_reminders()
        self.reminders_frame.pack(fill=tk.BOTH, expand=True)

    def show_profile(self):
        self.clear_content_frame()
        self.create_profile_page()  # Recreate profile page to update information
        self.profile_frame.pack(fill=tk.BOTH, expand=True)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    def calculate_payment(self):
        try:
            home_price = float(self.home_price_var.get())
            down_payment = float(self.down_payment_var.get())
            interest_rate = float(self.interest_rate_var.get()) / 100 / 12
            property_tax = float(self.property_tax_var.get()) / 100 / 12

            loan_amount = home_price - down_payment
            if self.loan_program_var.get() == "Adjustable Rate":
                year = simpledialog.askinteger("Adjustable Rate", "Enter the number of years:")
                if year is None:
                    return
                num_payments = year * 12
            else:
                num_payments = 30 * 12

            monthly_payment = (loan_amount * interest_rate) / (1 - (1 + interest_rate) ** -num_payments)
            property_tax_payment = (home_price * property_tax) / num_payments
            total_payment = monthly_payment + property_tax_payment

            self.result_var.set(f"Monthly Payment: ₹{total_payment:.2f}")

            self.update_reminders()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    def on_loan_program_selected(self, *args):
        if self.loan_program_var.get() == "Adjustable Rate":
            year = simpledialog.askinteger("Adjustable Rate", "Enter the number of years:")
            if year is not None:
                self.update_reminders()
        else:
            self.update_reminders()

    def update_reminders(self):
        try:
            if self.result_var.get():
                today = datetime.today()
                payment_due_date = today + timedelta(days=30)
                self.due_dates_text.config(text=f"Next Payment Due Date: {payment_due_date.strftime('%Y-%m-%d')}")

                # Remove previous pie chart if exists
                for widget in self.chart_frame.winfo_children():
                    widget.destroy()

                # Display Pie Chart
                self.display_pie_chart()

                # Update calendar
                self.update_calendar()
                self.update_countdown()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_pie_chart(self):
        # Dummy data for pie chart
        labels = 'Principal Payment', 'Interest Payment', 'Tax Payment'
        sizes = [60, 30, 10]  # Example values
        colors = ['#ff9999','#66b3ff','#99ff99']

        fig, ax = plt.subplots(figsize=(5, 3), subplot_kw=dict(aspect="equal"))
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

        for text in texts:
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_fontsize(12)

        plt.setp(autotexts, size=10, weight="bold")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def edit_profile(self):
        self.clear_content_frame()
        self.create_profile_edit_page()

    def create_profile_edit_page(self):
        self.profile_edit_frame = tk.Frame(self.content_frame, bg=self.current_colors['background'])

        tk.Label(self.profile_edit_frame, text="Edit Profile", font=("Arial", 18, "bold"), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=10)

        self.name_var = tk.StringVar(value=self.profile_data['name'])
        self.email_var = tk.StringVar(value=self.profile_data['email'])
        self.income_var = tk.StringVar(value=self.profile_data['income'])
        self.expenses_var = tk.StringVar(value=self.profile_data['expenses'])
        self.credit_score_var = tk.StringVar(value=self.profile_data['credit_score'])

        tk.Label(self.profile_edit_frame, text="Name:", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.profile_edit_frame, textvariable=self.name_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.profile_edit_frame, text="Email Address:", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.profile_edit_frame, textvariable=self.email_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.profile_edit_frame, text="Monthly Income (₹):", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.profile_edit_frame, textvariable=self.income_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.profile_edit_frame, text="Monthly Expenses (₹):", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.profile_edit_frame, textvariable=self.expenses_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.profile_edit_frame, text="Credit Score:", font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text']).pack(pady=5)
        tk.Entry(self.profile_edit_frame, textvariable=self.credit_score_var, font=("Arial", 14)).pack(pady=5)

        tk.Button(self.profile_edit_frame, text="Save", command=self.save_profile, bg=self.current_colors['accent'], fg=self.current_colors['text'], font=("Arial", 12, "bold"), relief=tk.RAISED).pack(pady=10)

        self.profile_edit_frame.pack(fill=tk.BOTH, expand=True)

    def save_profile(self):
        name = self.name_var.get()
        email = self.email_var.get()
        income = self.income_var.get()
        expenses = self.expenses_var.get()
        credit_score = self.credit_score_var.get()
        if not (name and email and income and expenses and credit_score):
            messagebox.showerror("Input Error", "Please fill in all profile fields.")
            return
        self.profile_data['name'] = name
        self.profile_data['email'] = email
        self.profile_data['income'] = income
        self.profile_data['expenses'] = expenses
        self.profile_data['credit_score'] = credit_score
        messagebox.showinfo("Profile Saved", "Profile details have been saved.")
        self.show_profile()

    def update_calendar(self):
        # Placeholder for calendar update
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        today = datetime.today()
        month_days = calendar.monthrange(today.year, today.month)[1]
        cal_text = calendar.month_name[today.month] + " " + str(today.year) + "\n"

        for day in range(1, month_days + 1):
            cal_text += f"{day:2} "
            if (day % 7 == 0):
                cal_text += "\n"

        cal_label = tk.Label(self.calendar_frame, text=cal_text, font=("Courier", 12), bg=self.current_colors['background'], fg=self.current_colors['text'])
        cal_label.pack(pady=10)

    def update_countdown(self):
        # Display countdown to the next payment
        today = datetime.today()
        due_date = today + timedelta(days=30)
        days_remaining = (due_date - today).days
        countdown_text = f"Days remaining until next payment: {days_remaining} days"
        countdown_label = tk.Label(self.calendar_frame, text=countdown_text, font=("Arial", 14), bg=self.current_colors['background'], fg=self.current_colors['text'])
        countdown_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MortgageCalculatorApp(root)
    root.mainloop()






