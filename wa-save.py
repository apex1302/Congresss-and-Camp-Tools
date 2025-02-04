from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# WebDriver einrichten
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./whatsapp_data")  # Speichert Session
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#  WhatsApp Web öffnen
driver.get("https://web.whatsapp.com/")
input("Scanne den QR-Code und drücke ENTER...")  # Warte auf manuelles Login

#  Status-Bereich öffnen
status_xpath = "//div[@title='Status']"
try:
    driver.find_element(By.XPATH, status_xpath).click()
    time.sleep(3)
except:
    print("Status-Button nicht gefunden!")
    driver.quit()

#  Alle Statusmeldungen abrufen
status_list = driver.find_elements(By.XPATH, "//div[contains(@aria-label, ' von ')]")

# Sicherstellen, dass es Statusmeldungen gibt
if not status_list:
    print("Keine Statusmeldungen gefunden.")
    driver.quit()

#  Durch Status scrollen und Screenshots speichern
output_folder = "whatsapp_status_backup"
os.makedirs(output_folder, exist_ok=True)

for idx, status in enumerate(status_list):
    try:
        status.click()
        time.sleep(3)
        
        # Screenshot des Status speichern
        screenshot_path = os.path.join(output_folder, f"status_{idx}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Status gespeichert: {screenshot_path}")

        # Weiter zum nächsten Status
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)
        time.sleep(2)

    except Exception as e:
        print(f"Fehler beim Speichern: {e}")

# Beenden
driver.quit()
print("Status-Backup abgeschlossen.")

