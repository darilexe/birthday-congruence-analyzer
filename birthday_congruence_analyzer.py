import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import sys

def is_leap_year(year):
    """Determine if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def analyze_birthdays(event=None):
    """Main logic to calculate and display the congruence."""
    full_name = entry_name.get().strip()

    if not full_name:
        messagebox.showerror("Missing Input", "Please enter a full name.")
        return

    month_str = combo_month.get()
    day_str = combo_day.get()
    year_str = combo_year.get()

    try:
        # Check if it's a real date 
        b_date = datetime.datetime.strptime(f"{month_str} {day_str} {year_str}", "%b %d %Y")
        birth_month = b_date.month
        start_year = b_date.year
        birthdate_str = b_date.strftime("%b %d, %Y")
    except ValueError:
        messagebox.showerror("Invalid Date", "The selected date does not exist on the calendar.")
        return

    # Weekday
    original_weekday = combo_weekday.get()
    if not original_weekday:
        messagebox.showerror("Missing Input", "Please select a weekday.")
        return
    weekdays_index = weekdays.index(original_weekday)

    # Enable text box to write new results
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)

    # Format the header
    output_str = "----- Birthday Congruence Analyzer -----\n"
    output_str += "-----------------------------------------\n"
    output_str += f"Name : {full_name}\n"
    output_str += f"Birthday : {birthdate_str}\n"
    output_str += f"Weekday : {original_weekday}\n"
    output_str += "+---------------------------------------+\n"
    output_str += f"| Birthdays occurring on {original_weekday:<14} |\n"
    output_str += "+---------------------------------------+\n"
    output_str += " Age  |   Year   |   Weekday\n"
    output_str += "-----------------------------------------\n"

    # Get the starting day
    current_index = weekdays_index
    occurrences = 0

    # Simulate ages 0 through 72
    for age in range(73):
        current_year = start_year + age
        current_weekday_str = weekdays[current_index]

        if current_weekday_str == original_weekday:
            output_str += f" {age:<4} |   {current_year:<6} |   {current_weekday_str}\n"
            occurrences += 1

        leap_check_year = current_year + 1 if birth_month > 2 else current_year
        shift = 2 if is_leap_year(leap_check_year) else 1

        # Iterate through the string list by shifting the index
        current_index = (current_index + shift) % 7

    output_str += f"Total Occurrences: {occurrences}\n"
    output_str += "2023***** - Darryl Baranda\n"

    # Insert text
    text_output.insert(tk.END, output_str)
    text_output.config(state=tk.DISABLED)

# ==========================================
# GUI Setup & Modern Theming
# ==========================================
root = tk.Tk()
root.title("Birthday Congruence Analyzer")
root.geometry("520x680")
root.resizable(False, False) 

BG_COLOR = "#121413"       # Soft Dark Slate
ENTRY_BG = "#1F2422"       # Dark Gray for inputs
FG_COLOR = "#E8E8E8"       # Off-White 
ACCENT_COLOR = "#1A5F38"   # Pine Green
ACCENT_HOVER = "#23804B"   # Pine Green for button hover

root.configure(bg=BG_COLOR, padx=25, pady=25)

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

title_label = tk.Label(root, text="Congruence Analyzer", font=("Roboto", 18, "bold"), bg=BG_COLOR, fg=ACCENT_HOVER)
title_label.pack(anchor=tk.W, pady=(0, 20))

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox",
                fieldbackground=ENTRY_BG,
                background=ENTRY_BG,
                foreground=FG_COLOR,
                darkcolor=ENTRY_BG,
                lightcolor=ENTRY_BG,
                bordercolor=ACCENT_COLOR,
                arrowcolor=ACCENT_HOVER)
style.map('TCombobox', fieldbackground=[('readonly', ENTRY_BG)], selectbackground=[('readonly', ENTRY_BG)], selectforeground=[('readonly', FG_COLOR)])

# Input Frame
frame_inputs = tk.Frame(root, bg=BG_COLOR)
frame_inputs.pack(fill=tk.X, pady=(0, 15))

# Form styling configuration
label_font = ("Roboto", 11, "bold")
entry_font = ("Roboto", 11)

# Name
tk.Label(frame_inputs, text="Full Name:", font=label_font, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky=tk.W, pady=10)
entry_name = tk.Entry(frame_inputs, width=32, font=entry_font, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, highlightthickness=1, highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_HOVER, relief="flat")
entry_name.grid(row=0, column=1, pady=10, padx=15, sticky=tk.W, ipady=4)

# Birthdate 
tk.Label(frame_inputs, text="Birthdate:", font=label_font, bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky=tk.W, pady=10)
date_frame = tk.Frame(frame_inputs, bg=BG_COLOR)
date_frame.grid(row=1, column=1, sticky=tk.W, pady=10, padx=15)

months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
combo_month = ttk.Combobox(date_frame, values=months_list, state="readonly", width=5, font=entry_font)
combo_month.pack(side=tk.LEFT, padx=(0, 8))
combo_month.set("Mar")

days_list = [str(i) for i in range(1, 32)]
combo_day = ttk.Combobox(date_frame, values=days_list, state="readonly", width=4, font=entry_font)
combo_day.pack(side=tk.LEFT, padx=(0, 8))
combo_day.set("10")

current_year = datetime.datetime.now().year
years_list = [str(i) for i in range(current_year, 1949, -1)]
combo_year = ttk.Combobox(date_frame, values=years_list, state="readonly", width=6, font=entry_font)
combo_year.pack(side=tk.LEFT)
combo_year.set("2005")

# Weekday Dropdown
tk.Label(frame_inputs, text="Weekday:", font=label_font, bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky=tk.W, pady=10)
weekdays_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
combo_weekday = ttk.Combobox(frame_inputs, values=weekdays_list, state="readonly", width=29, font=entry_font)
combo_weekday.grid(row=2, column=1, pady=10, padx=15, sticky=tk.W)
combo_weekday.set("Thursday")

def on_enter(e):
    btn_analyze['background'] = ACCENT_HOVER
def on_leave(e):
    btn_analyze['background'] = ACCENT_COLOR

btn_analyze = tk.Label(root, text="ANALYZE BIRTHDAYS", font=("Roboto", 11, "bold"), bg=ACCENT_COLOR, fg="#FFFFFF", pady=10, cursor="hand2")
btn_analyze.pack(fill=tk.X, pady=15)
btn_analyze.bind("<Enter>", on_enter)
btn_analyze.bind("<Leave>", on_leave)
btn_analyze.bind("<Button-1>", analyze_birthdays)

# --- Output Frame ---
output_border = tk.Frame(root, bg=ACCENT_COLOR, padx=2, pady=2)
output_border.pack(fill=tk.BOTH, expand=True, pady=5)

text_output = tk.Text(output_border, height=18, width=50, font=("Roboto Mono", 11),
                      state=tk.DISABLED, bg=ENTRY_BG, fg=FG_COLOR,
                      insertbackground=FG_COLOR, highlightthickness=0, borderwidth=0, padx=15, pady=15)
text_output.pack(fill=tk.BOTH, expand=True)

root.mainloop()