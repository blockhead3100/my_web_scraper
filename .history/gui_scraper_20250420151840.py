import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from scraper import get_page_data_selenium
import json
import datetime
import subprocess
import importlib.util

def check_and_install_packages():
    required_packages = ["selenium", "tkinter"]
    missing_packages = []

    for package in required_packages:
        if not importlib.util.find_spec(package):
            missing_packages.append(package)

    if missing_packages:
        try:
            subprocess.check_call(["python", "-m", "pip", "install"] + missing_packages)
            messagebox.showinfo("Installation", f"The following packages were installed: {', '.join(missing_packages)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install packages: {e}")
    else:
        messagebox.showinfo("Installation", "All required packages are already installed.")

def show_disclaimer():
    disclaimer_text = (
        "Disclaimer: This software is provided 'as-is' without any warranties. "
        "By using this software, you agree to the terms and conditions outlined in the license."
    )
    messagebox.showinfo("Disclaimer", disclaimer_text)

show_disclaimer()
check_and_install_packages()

def start_scraping():
    url = url_entry.get()
    data_type = data_type_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    if data_type == "Select Data Type":
        messagebox.showerror("Error", "Please select a data type")
        return

    try:
        # Pass the selected data type to the scraper function
        data = get_page_data_selenium(url, data_type)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, json.dumps(data, indent=4))

        # Save data to a JSON file
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"scraped_data_{data_type}_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Success", f"Data saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Web Scraper GUI")

# URL input
tk.Label(root, text="Enter URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Data type selection
tk.Label(root, text="Select Data Type:").grid(row=1, column=0, padx=10, pady=10)
data_type_var = tk.StringVar(value="Select Data Type")
data_type_menu = tk.OptionMenu(root, data_type_var, "Text", "Images", "Links", "Tables")
data_type_menu.grid(row=1, column=1, padx=10, pady=10)

# Scrape button
scrape_button = tk.Button(root, text="Start Scraping", command=start_scraping)
scrape_button.grid(row=2, column=0, columnspan=2, pady=10)

# Output area with scrollable frame
output_frame = ttk.Frame(root)
output_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

output_scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
output_scrollbar.pack(side="right", fill="y")

output_text = tk.Text(output_frame, wrap=tk.WORD, yscrollcommand=output_scrollbar.set)
output_text.pack(side="left", fill="both", expand=True)

output_scrollbar.config(command=output_text.yview)

# Configure the root grid to allow resizing
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()