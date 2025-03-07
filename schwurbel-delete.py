import re
import sys
import logging
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppWebRedactor:
    """
    A tool that scans WhatsApp Web and redacts messages with excessive emojis.
    """
    def __init__(self, output_file="chat_log.json"):
        self.driver = None
        self.output_file = output_file
        self.emoji_pattern = re.compile(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]+", re.UNICODE)

    def start_browser(self):
        """Launches Chrome and opens WhatsApp Web."""
        logging.info("Launching browser...")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://web.whatsapp.com")
        logging.info("Please scan the QR code to log in.")
        time.sleep(15)  # Wait for user to scan QR manually

    def fetch_messages(self):
        """Fetches messages from the chat list."""
        logging.info("Fetching messages...")
        try:
            messages = self.driver.find_elements(By.XPATH, "//div[@class='_21Ahp']")
            chat_lines = [msg.text for msg in messages]
            return chat_lines
        except Exception as e:
            logging.error(f"Error fetching messages: {e}")
            return []

    def count_emojis(self, text: str) -> int:
        """Counts emojis in a given text line."""
        return len(self.emoji_pattern.findall(text))

    def process_chat(self):
        """Reads WhatsApp messages, redacts lines with more than two emojis, and saves them to a JSON file."""
        logging.info("Processing chat...")
        messages = self.fetch_messages()
        processed_chat = []

        for line in messages:
            emoji_count = self.count_emojis(line)
            if emoji_count > 2:
                logging.info(f"Redacting line: {line.strip()} (Contains {emoji_count} emojis)")
                processed_chat.append({"original": line, "redacted": "[REDACTED]"})
            else:
                processed_chat.append({"original": line, "redacted": line})
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(processed_chat, f, indent=4, ensure_ascii=False)
        
        logging.info(f"Chat saved to {self.output_file}")
        return processed_chat

    def close_browser(self):
        """Closes the browser session."""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    redactor = WhatsAppWebRedactor()
    redactor.start_browser()
    result = redactor.process_chat()
    redactor.close_browser()
    
    print("\nProcessed Chat:")
    for entry in result:
        print(entry["redacted"])

