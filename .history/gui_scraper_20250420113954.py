import tkinter as tk
from tkinter import messagebox
from scraper import get_page_data_selenium
import json
import datetime

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

# Output area
tk.Label(root, text="Output:").grid(row=3, column=0, padx=10, pady=10)
output_text = tk.Text(root, wrap=tk.WORD)
output_text.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# Configure the root grid to allow resizing
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()