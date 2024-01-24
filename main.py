import sys
import logging
import tkinter as tk
import tkinter.filedialog as tkfiledialog
from tkinter import scrolledtext
from pysitemap import crawler
from pysitemap.parsers.lxml_parser import Parser
import os

def generate_sitemap():
    root_url = entry.get()
    if root_url:
        try:
            processing_button.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)  # Clear existing text
            result_text.insert(tk.END, "Generating sitemap, please wait...\n")
            root.update_idletasks()

            # Redirect standard output to the Text widget
            sys.stdout = StdoutRedirector(result_text)

            crawler(
                root_url, out_file='debug/sitemap.xml', exclude_urls=[".pdf", ".jpg", ".zip"],
                http_request_options={"ssl": False}, parser=Parser
            )

            result_text.insert(tk.END, f"Sitemap generated successfully for {root_url}\n")
            download_button.config(state=tk.NORMAL)
        except Exception as e:
            result_text.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            processing_button.config(state=tk.DISABLED)
            # Reset standard output to the default
            sys.stdout = sys.__stdout__

    else:
        result_text.insert(tk.END, "Please enter a valid URL.\n")
        download_button.config(state=tk.DISABLED)

def download_sitemap():
    try:
        sitemap_path = 'debug/sitemap.xml'
        if os.path.exists(sitemap_path):
            with open(sitemap_path, 'rb') as file:
                content = file.read()

            # Prompt user to choose a location to save the file
            file_path = tkfiledialog.asksaveasfilename(
                defaultextension=".xml",
                filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'wb') as download_file:
                    download_file.write(content)
                result_text.insert(tk.END, "Sitemap downloaded successfully.\n")
            else:
                result_text.insert(tk.END, "Download canceled.\n")
        else:
            result_text.insert(tk.END, "Sitemap not found. Generate it first.\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")

# Custom class to redirect standard output to the Text widget
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Sitemap Generator")

# Create a label
label = tk.Label(root, text="Enter the website URL:")
label.pack(pady=10)

# Create an entry widget for the URL
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create a button to generate the sitemap
generate_button = tk.Button(root, text="Generate Sitemap", command=generate_sitemap)
generate_button.pack(pady=10)

# Create a processing button
processing_button = tk.Button(root, text="Processing...", state=tk.DISABLED)
processing_button.pack(pady=10)

# Create a button to download the sitemap
download_button = tk.Button(root, text="Download Sitemap", state=tk.DISABLED, command=download_sitemap)
download_button.pack(pady=10)

# Create a Text widget to display processing messages
result_text = scrolledtext.ScrolledText(root, width=40, height=10)
result_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
