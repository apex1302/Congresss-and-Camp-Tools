import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Database setup
def setup_database():
    conn = sqlite3.connect('whatsapp_data.db')
    c = conn.cursor()
    # Create tables for chats and statuses
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY, contact TEXT, message TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS statuses
                 (id INTEGER PRIMARY KEY, contact TEXT, status TEXT, timestamp TEXT)''')
    conn.commit()
    return conn, c

# Initialize Selenium WebDriver
def initialize_webdriver():
    # Path to your ChromeDriver
    service = Service('/path/to/chromedriver')  # Replace with your ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://web.whatsapp.com')
    return driver

# Wait for user to scan QR code
def wait_for_login(driver):
    print("Please scan the QR code to log in to WhatsApp Web.")
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_1Gy50'))  # Wait for chats to load
    )
    print("Login successful!")

# Extract and save chat messages
def save_chats(driver, conn, c):
    print("Extracting chat messages...")
    # Locate chat elements
    chats = driver.find_elements(By.CLASS_NAME, '_1Gy50')
    for chat in chats:
        try:
            contact = chat.find_element(By.CLASS_NAME, '_1wjpf').text
            messages = chat.find_elements(By.CLASS_NAME, '_3_7SH')
            for message in messages:
                msg_text = message.text
                timestamp = message.find_element(By.CLASS_NAME, '_3EFt_').text
                c.execute("INSERT INTO chats (contact, message, timestamp) VALUES (?, ?, ?)",
                          (contact, msg_text, timestamp))
            conn.commit()
        except Exception as e:
            print(f"Error extracting chat: {e}")

# Extract and save contact statuses
def save_statuses(driver, conn, c):
    print("Extracting contact statuses...")
    try:
        # Navigate to the status tab
        status_tab = driver.find_element(By.XPATH, '//div[@title="Status"]')
        status_tab.click()
        time.sleep(5)  # Wait for statuses to load

        # Locate status elements
        statuses = driver.find_elements(By.CLASS_NAME, '_2wP_Y')
        for status in statuses:
            contact = status.find_element(By.CLASS_NAME, '_2wP_Y').text
            status_text = status.find_element(By.CLASS_NAME, '_2wP_Y').text
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO statuses (contact, status, timestamp) VALUES (?, ?, ?)",
                      (contact, status_text, timestamp))
        conn.commit()
    except Exception as e:
        print(f"Error extracting statuses: {e}")

# Main function
def main():
    # Set up database
    conn, c = setup_database()

    # Initialize WebDriver
    driver = initialize_webdriver()

    # Wait for user to log in
    wait_for_login(driver)

    # Extract and save data
    try:
        while True:
            save_chats(driver, conn, c)
            save_statuses(driver, conn, c)
            print("Data saved. Waiting for the next cycle...")
            time.sleep(60)  # Run every minute
    except KeyboardInterrupt:
        print("Script stopped by user.")
    finally:
        # Clean up
        driver.quit()
        conn.close()
        print("WebDriver and database connection closed.")

if __name__ == "__main__":
    main()
