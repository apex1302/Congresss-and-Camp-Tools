from mastodon import Mastodon, StreamListener
import tkinter as tk
from tkinter import messagebox, filedialog
import configparser

# Configurations
def save_config(file_path, config):
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def create_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'api_base_url': 'https://mastodon.social',
        'email': '',
        'password': ''
    }
    return config

def gui():
    def save_and_close():
        config['DEFAULT']['api_base_url'] = url_entry.get()
        config['DEFAULT']['email'] = email_entry.get()
        config['DEFAULT']['password'] = password_entry.get()
        save_config(config_path, config)
        messagebox.showinfo("Info", "Configurations saved successfully.")
        root.destroy()

    root = tk.Tk()
    root.title("Mastodon Bot Config")

    tk.Label(root, text="API Base URL:").grid(row=0, column=0, padx=10, pady=5)
    url_entry = tk.Entry(root, width=40)
    url_entry.grid(row=0, column=1, padx=10, pady=5)
    url_entry.insert(0, config['DEFAULT'].get('api_base_url', ''))

    tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=5)
    email_entry = tk.Entry(root, width=40)
    email_entry.grid(row=1, column=1, padx=10, pady=5)
    email_entry.insert(0, config['DEFAULT'].get('email', ''))

    tk.Label(root, text="Password:").grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(root, width=40, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)
    password_entry.insert(0, config['DEFAULT'].get('password', ''))

    tk.Button(root, text="Save", command=save_and_close).grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

# Listener Class
class TrumpGedachtListener(StreamListener):
    def __init__(self, api):
        super().__init__()
        self.api = api

    def on_update(self, status):
        # Check for keywords in the Toot
        content = status.content.lower()
        if "trump" in content and "gedacht" in content:
            print(f"Gefundener Toot: {status.content}")
            # Post "told you so"
            self.api.status_post(
                "told you so", in_reply_to_id=status.id
            )
            print("Antwort gepostet.")

# Main Application
config_path = 'config.ini'
try:
    config = load_config(config_path)
except FileNotFoundError:
    config = create_config()
    save_config(config_path, config)

# Ensure required fields are set
if not config['DEFAULT'].get('email') or not config['DEFAULT'].get('password'):
    gui()

mastodon = Mastodon(
    client_id=None,
    api_base_url=config['DEFAULT']['api_base_url']
)
mastodon.log_in(
    config['DEFAULT']['email'],
    config['DEFAULT']['password'],
    to_file='usercred.secret'
)

listener = TrumpGedachtListener(mastodon)
mastodon.stream_public(listener)

