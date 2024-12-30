import os
import configparser
import time
import pjsua as pj  # PJSIP-Bibliothek

# Funktion zum Laden der SIP-Konfiguration
def load_sip_config():
    config = configparser.ConfigParser()
    config.read('sip_config.ini')
    return {
        'server': config.get('sip', 'server'),
        'username': config.get('sip', 'username'),
        'password': config.get('sip', 'password'),
        'domain': config.get('sip', 'domain')
    }

# Funktion zum Initialisieren der SIP-Verbindung
def init_sip(config):
    # Erstellen eines neuen SIP-Clients
    lib = pj.Lib()

    try:
        lib.init(log_cfg=pj.LogConfig(level=3, console_level=3))

        # Konfigurieren des SIP-Transportes
        transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))

        # Starten der SIP-Bibliothek
        lib.start()

        # Registrieren bei einem SIP-Server
        acc_cfg = pj.AccountConfig(domain=config['domain'], username=config['username'], password=config['password'])
        acc = lib.create_account(acc_cfg)
        print("SIP-Account registriert.")
        return lib, acc
    except pj.Error as e:
        print("Fehler beim Initialisieren von PJSIP: ", e)
        raise

# Funktion zum Anrufen einer Nummer
def call_number(acc, number):
    try:
        # Anruf an die angegebene Nummer
        call = acc.make_call(number)
        print(f"Rufe {number} an...")

        # Warten, bis der Anruf klingelt
        time.sleep(5)

        # Anruf beenden, um die Nummer zu überprüfen
        call.hangup()
        print(f"Anruf zu {number} beendet.")
        return True
    except pj.Error as e:
        print(f"Fehler beim Anrufen von {number}: ", e)
        return False

# Funktion zum Überprüfen und Speichern von gültigen Nummern
def check_numbers_in_range(start, end, acc):
    valid_numbers = []
    for number in range(start, end + 1):
        number_str = str(number)
        if call_number(acc, number_str):
            valid_numbers.append(number_str)
            with open("valid_numbers.txt", "a") as f:
                f.write(number_str + '\n')
            print(f"Nummer {number_str} ist gültig und wurde gespeichert.")
        else:
            print(f"Nummer {number_str} ist ungültig.")
    return valid_numbers

# Hauptlogik
def main():
    # SIP-Konfiguration laden
    config = load_sip_config()

    # SIP-Verbindung initialisieren
    lib, acc = init_sip(config)

    # Bereich von Telefonnummern definieren
    start_number = 1000
    end_number = 1010

    # Überprüfen der Telefonnummern im angegebenen Bereich
    valid_numbers = check_numbers_in_range(start_number, end_number, acc)

    # SIP-Verbindung schließen
    lib.destroy()
    print("SIP-Verbindung geschlossen.")

if __name__ == "__main__":
    main()

