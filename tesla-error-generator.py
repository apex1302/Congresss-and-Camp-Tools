import json
import random

# Mögliche Kategorien von Fehlern
categories = [
    "Geräusche", "Motoraussetzer", "Batterieprobleme", "Lenkung", "Bremsen", "Bordcomputer",
    "Display-Fehlermeldungen", "Lichtsystem", "Fahrassistent", "Ladetechnik", "Heizung & Klima",
    "Sensorik", "Konnektivität", "Sicherheitsfunktionen", "Innenraum-Elektronik", "Softwarefehler",
    "Ladeinfrastruktur", "Fahrzeugkommunikation", "Autopilot", "Fahrzeugverriegelung"
]

# Beispielhafte Fehler für jede Kategorie
error_templates = {
    "Geräusche": [
        "Klappergeräusch aus dem {bereich} bei Unebenheiten.",
        "Summen aus dem {ort} beim {aktion}.",
        "Knacken beim {manöver}.",
        "Rattern aus dem Unterboden beim {fahrzustand}.",
        "Unregelmäßiges Pfeifen bei {situation}.",
        "Brummen aus dem {bauteil} bei niedrigen Geschwindigkeiten."
    ],
    "Motoraussetzer": [
        "Plötzlicher Leistungsverlust auf der {straße}.",
        "Unregelmäßiges Ruckeln beim {fahrstil}.",
        "Motor geht kurz aus und startet {zeitpunkt} neu.",
        "Fehlermeldung: '{meldung}'.",
        "Fahrzeug nimmt kein Gas an und zeigt {warnung}.",
        "Plötzlicher kompletter Systemneustart während der {aktion}."
    ],
    "Batterieprobleme": [
        "Plötzlich starker Reichweitenverlust innerhalb {strecke} km.",
        "Lädt extrem langsam trotz {ladequelle}.",
        "Fehlermeldung: '{meldung}'.",
        "Auto lässt sich nach {dauer} Parken nicht mehr starten.",
        "Batteriestatus schwankt stark innerhalb kurzer Zeit.",
        "Ungewöhnlich hohe Energieverluste im {zustand}."
    ]
}

# Dynamische Platzhalterwerte
variations = {
    "bereich": ["Armaturenbrett", "Türverkleidung", "Kofferraum", "Motorraum"],
    "ort": ["Heckbereich", "vorderen Radkasten", "Innenraum"],
    "aktion": ["Beschleunigen", "Bremsen", "Kurvenfahrt"],
    "manöver": ["Einschlagen der Lenkung", "Parken", "Autobahnfahrt"],
    "fahrzustand": ["langsamer Fahrt", "schnellem Tempo", "Stop-and-Go-Verkehr"],
    "situation": ["geöffnetem Fenster", "hoher Luftfeuchtigkeit", "kalten Temperaturen"],
    "bauteil": ["Fahrwerk", "Vorderachse", "Hinterachse"],
    "straße": ["Autobahn", "Landstraße", "Innenstadt"],
    "fahrstil": ["starkem Beschleunigen", "konstantem Tempo", "Rekuperation"],
    "zeitpunkt": ["nach wenigen Sekunden", "erst nach Neustart"],
    "meldung": ["Leistungsreduzierung - Werkstatt aufsuchen", "Batterieüberhitzung - Leistung begrenzt"],
    "warnung": ["Warnleuchte für Antrieb", "Systemmeldung im Display"],
    "strecke": ["50", "100", "150"],
    "ladequelle": ["Supercharger", "Wallbox", "öffentlicher Ladesäule"],
    "dauer": ["1 Stunde", "über Nacht"],
    "zustand": ["Standby-Modus", "normaler Nutzung"]
}

# Generiere 1000 zufällige Fehler
errors = []
for _ in range(1000):
    category = random.choice(categories)
    error_template = random.choice(error_templates.get(category, ["Unbekannter Fehler in dieser Kategorie."]))
    error_description = error_template.format(**{key: random.choice(values) for key, values in variations.items() if "{" + key + "}" in error_template})
    errors.append({"Kategorie": category, "Beschreibung": error_description})

# Speichere die Fehler in einer JSON-Datei
with open("tesla_model3_fehler.json", "w", encoding="utf-8") as file:
    json.dump(errors, file, indent=4, ensure_ascii=False)

print("1000 Fehler wurden erfolgreich in 'tesla_model3_fehler.json' gespeichert.")

