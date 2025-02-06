from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

# Function to generate random personal data
def generate_random_data():
    # Expanded list of first names (50 options)
    first_names = [
        "Max", "Anna", "Julia", "Tom", "Lisa", "Paul", "Sarah", "David", "Laura", "Michael",
        "Emma", "Daniel", "Sophie", "Alexander", "Maria", "Leon", "Lena", "Tim", "Hannah", "Felix",
        "Emily", "Lukas", "Mia", "Jonas", "Lea", "Ben", "Lara", "Niklas", "Johanna", "Simon",
        "Clara", "Philipp", "Valentina", "Moritz", "Elena", "Jan", "Amelie", "Fabian", "Luisa", "Tobias",
        "Marie", "Sebastian", "Charlotte", "Florian", "Lina", "Patrick", "Isabella", "Martin", "Maja", "Andreas"
    ]

    # Expanded list of last names (50 options)
    last_names = [
        "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
        "Schäfer", "Koch", "Bauer", "Richter", "Klein", "Wolf", "Schröder", "Neumann", "Schwarz", "Zimmermann",
        "Braun", "Krüger", "Hofmann", "Hartmann", "Lange", "Schmitt", "Werner", "Schmitz", "Krause", "Meier",
        "Lehmann", "Schmid", "Schulze", "Maier", "Köhler", "Herrmann", "König", "Walter", "Mayer", "Huber",
        "Kaiser", "Fuchs", "Peters", "Lang", "Scholz", "Möller", "Weiß", "Jung", "Hahn", "Vogel"
    ]

    # Expanded list of email domains (50 options)
    domains = [
        "gmail.com", "yahoo.com", "hotmail.com", "web.de", "outlook.com", "icloud.com", "aol.com", "protonmail.com",
        "zoho.com", "yandex.com", "gmx.de", "mail.com", "t-online.de", "live.com", "hotmail.de", "yahoo.de",
        "me.com", "msn.com", "googlemail.com", "freenet.de", "posteo.de", "arcor.de", "1und1.de", "vodafone.de",
        "kabelmail.de", "t-online.de", "online.de", "gmx.net", "gmx.at", "gmx.ch", "bluewin.ch", "swissonline.ch",
        "sunrise.ch", "orange.fr", "sfr.fr", "laposte.net", "libero.it", "virgilio.it", "alice.it", "tin.it",
        "rambler.ru", "mail.ru", "bk.ru", "inbox.ru", "list.ru", "ya.ru", "qq.com", "163.com", "126.com", "sina.com"
    ]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
    phone = f"+49{random.randint(100000000, 999999999)}"

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone
    }

# Initialize the WebDriver
driver = webdriver.Chrome()  # or use another browser driver

try:
    # Open the Tesla Drive page
    driver.get("https://www.tesla.com/de_DE/drive")

    # Wait for the page to load
    time.sleep(5)

    # Click on the "Jetzt Probefahrt buchen" button
    driver.find_element(By.XPATH, "//a[contains(text(), 'Jetzt Probefahrt buchen')]").click()

    # Wait for the next page to load
    time.sleep(5)

    # Select the Model Y
    driver.find_element(By.XPATH, "//div[contains(text(), 'Model Y')]").click()

    # Wait for the next page to load
    time.sleep(5)

    # Select the location "Heerbergstraße 7, 71384 Weinstadt, Germany"
    location_input = driver.find_element(By.ID, "location-input")
    location_input.send_keys("Heerbergstraße 7, 71384 Weinstadt, Germany")
    time.sleep(2)
    location_input.send_keys(Keys.RETURN)

    # Wait for the location to be selected
    time.sleep(5)

    # Generate random personal data
    personal_data = generate_random_data()

    # Fill in the form with random data
    driver.find_element(By.ID, "first-name").send_keys(personal_data["first_name"])
    driver.find_element(By.ID, "last-name").send_keys(personal_data["last_name"])
    driver.find_element(By.ID, "email").send_keys(personal_data["email"])
    driver.find_element(By.ID, "phone").send_keys(personal_data["phone"])

    # Select a random date and time (this part may need adjustment based on the actual form)
    date_picker = driver.find_element(By.ID, "date-picker")
    date_picker.click()
    time.sleep(2)
    available_dates = driver.find_elements(By.CLASS_NAME, "available-date")
    if available_dates:
        random.choice(available_dates).click()

    time.sleep(2)

    # Submit the form
    driver.find_element(By.XPATH, "//button[contains(text(), 'Termin buchen')]").click()

    # Wait for the confirmation page
    time.sleep(10)

finally:
    # Close the browser
    driver.quit()
