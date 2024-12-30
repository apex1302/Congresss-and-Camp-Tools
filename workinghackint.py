import socket
import ssl
import time
import random

# Configuration
server = "palermo.hackint.org"  # The IRC server
port = 6697  # Secure port
channel = "#38c3-hall-1"  # The channel you want to join
nickname = "dad420"  # Your nickname
password = "your_password"  # NickServ password

# List of 500 dad jokes (simplified here, replace with the full list you want)
dad_jokes = [
"Warum können Bienen so gut rechnen? Weil sie immer im Bienenstock arbeiten!",
"Was macht ein Pirat am Computer? Er drückt die Enter-Taste!",
"Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann!",
"Was macht ein Keks unter einem Baum? Krümel!",
"Warum ging der Pilz auf die Party? Weil er ein Champignon war!",
"Warum hat der Mathematikbuch immer schlechte Laune? Weil es so viele Probleme hat!",
"Was ist orange und läuft durch den Wald? Eine Wanderine!",
"Warum können Skelette so schlecht lügen? Weil sie keinen Mumm haben!",
"Was macht ein Teddybär, wenn er hungrig ist? Er geht zum Bärenladen!",
"Warum können Vögel so gut singen? Weil sie die besten Noten haben!",
"Wie nennt man einen Bumerang, der nicht zurückkommt? Ein Stock!",
"Was ist schwarz und weiß und sitzt auf einem Baum? Ein Schachbrett!",
"Warum schlich der Apfel durch die Gegend? Weil er ein kleiner Streber war!",
"Warum können Bienen keine Musik machen? Weil sie immer im Einklang sind!",
"Wie nennt man ein durstiges Wasser? Ein Fluss!",
"Warum ging der Pilz nicht zur Party? Weil er der Stängel war!",
"Was macht ein Keks unter Wasser? Krümel tauchen!",
"Was ist grün und schießt in die Luft? Ein Spritzgurke!",
"Warum ging der Strom nicht ins Kino? Er hatte schon genug Spannung!",
"Warum können Geister keine guten Lügen erzählen? Weil man durch sie hindurchsehen kann!",
"Was ist braun und läuft durch den Wald? Ein Waldhonig!",
"Warum ging der Lehrer ins Gefängnis? Weil er seine Schüler unter Druck setzte!",
"Warum ging der Bäcker in die Schule? Um mehr zu kneten!",
"Was ist klein, rund und braun? Ein Marzipan!",
"Was macht ein Känguru, wenn es hungrig ist? Es geht auf Känguruhjagd!",
"Warum kann der Golfball nicht tanzen? Weil er immer ins Loch fällt!",
"Was macht ein Hund in der Bibliothek? Er liest ein Buch!",
"Warum schlich der Apfel durch den Wald? Er war auf der Flucht vor dem Apfelstrudel!",
"Warum haben Vampire so gute Manieren? Sie vermeiden immer, auf die Zähne zu beißen!",
"Was tut ein Mathematiker, wenn er einen Fehler macht? Er rechnet ihn aus!",
"Warum ist der Computer schlecht im Sport? Weil er immer eine Maus braucht!",
"Was ist klein und kann im Regen nicht nass werden? Ein Papierschirm!",
"Warum kann man keine Geheimnisse in einer Bäckerei bewahren? Weil der Teig immer ausplaudert!",
"Was sagt der eine Berg zum anderen? Wir sehen uns auf der Spitze!",
"Warum gehen Taschen nicht ins Fitnessstudio? Sie haben schon genug zu tragen!",
"Was macht ein Frosch, der keinen Job hat? Er quakt sich durch!",
"Warum wollte der Apfel nie ins Internet? Weil er die Cookies nicht mochte!",
"Warum gab der Papagei keinen Kommentar ab? Er wollte nicht in den Schlagzeilen sein!",
"Was macht ein Schaf, wenn es im Regen steht? Es zieht die Wolle hoch!",
"Warum schlich der Schatten immer hinter dem Baum? Er hatte Angst vor dem Licht!",
]

# Set up the socket and SSL connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(sock)

# Connect to the IRC server
sock.connect((server, port))

# Function to send IRC messages
def send_irc_message(message):
    print(f"Sent: {message}")
    sock.send((message + "\r\n").encode('utf-8'))

# Register the nickname with NickServ if needed
send_irc_message(f"USER {nickname} 0 * :{nickname}")
send_irc_message(f"NICK {nickname}")

# Give some time for the server to process the NICK and USER commands
time.sleep(3)

# Identify with NickServ if you've already registered
send_irc_message(f"PRIVMSG NickServ :IDENTIFY {password}")

# Wait a bit for NickServ to identify you
time.sleep(3)

# Monitor incoming messages and responses from the IRC server
print("Waiting for MOTD and server response...")

# Wait for MOTD and server messages
while True:
    response = sock.recv(2048).decode('utf-8', errors='ignore')
    print(f"Received: {response}")

    # Respond to PING to keep the connection alive
    if "PING" in response:
        send_irc_message(f"PONG {response.split()[1]}")

    # Check for MOTD completion to join the channel
    if "End of /MOTD command" in response:
        print("Received MOTD. Ready to interact with the server.")
        
        # Join the channel after MOTD
        send_irc_message(f"JOIN {channel}")
        time.sleep(5)  # Give the server time to process the JOIN
        
        # Send the initial message to confirm
        send_irc_message(f"NAMES {channel}")
        time.sleep(3)  # Delay before sending any other messages
        
        print("Joined the channel. Sending jokes...")

        # Send a random dad joke every 90 seconds
        while True:
            # Choose a random joke from the list
            random_joke = random.choice(dad_jokes)
            send_irc_message(f"PRIVMSG {channel} :{random_joke}")
            time.sleep(32)  # Wait 90 seconds before sending the next joke

