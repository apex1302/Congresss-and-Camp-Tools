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
        'password': '',
        'scan_text': 'trump,gedacht',
        'reply_text': 'told you so'
    }
    return config

def gui():
    def save_and_close():
        config['DEFAULT']['api_base_url'] = url_entry.get()
        config['DEFAULT']['email'] = email_entry.get()
        config['DEFAULT']['password'] = password_entry.get()
        config['DEFAULT']['scan_text'] = scan_text_entry.get()
        config['DEFAULT']['reply_text'] = reply_text_entry.get()
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

    tk.Label(root, text="Scan Text (comma-separated):").grid(row=3, column=0, padx=10, pady=5)
    scan_text_entry = tk.Entry(root, width=40)
    scan_text_entry.grid(row=3, column=1, padx=10, pady=5)
    scan_text_entry.insert(0, config['DEFAULT'].get('scan_text', ''))

    tk.Label(root, text="Reply Text:").grid(row=4, column=0, padx=10, pady=5)
    reply_text_entry = tk.Entry(root, width=40)
    reply_text_entry.grid(row=4, column=1, padx=10, pady=5)
    reply_text_entry.insert(0, config['DEFAULT'].get('reply_text', ''))

    tk.Button(root, text="Save", command=save_and_close).grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()

# Listener Class
class TrumpGedachtListener(StreamListener):
    def __init__(self, api, scan_text, reply_text):
        super().__init__()
        self.api = api
        self.scan_text = scan_text
        self.reply_text = reply_text

    def on_update(self, status):
        # Check for keywords in the Toot
        content = status.content.lower()
        if all(word in content for word in self.scan_text):
            print(f"Gefundener Toot: {status.content}")
            # Post the reply text
            self.api.status_post(
                self.reply_text, in_reply_to_id=status.id
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

scan_text = config['DEFAULT']['scan_text'].split(',')
reply_text = config['DEFAULT']['reply_text']

mastodon = Mastodon(
    client_id=None,
    api_base_url=config['DEFAULT']['api_base_url']
)
mastodon.log_in(
    config['DEFAULT']['email'],
    config['DEFAULT']['password'],
    to_file='usercred.secret'
)

listener = TrumpGedachtListener(mastodon, scan_text, reply_text)
mastodon.stream_public(listener)

