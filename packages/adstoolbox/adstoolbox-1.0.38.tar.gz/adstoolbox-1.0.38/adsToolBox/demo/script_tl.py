import requests
import imaplib
import os
import email
from email import policy

TENANT_ID = "7638e353-5319-43ae-b3d3-2ac7fd0ac61f"
CLIENT_ID = "d01021f8-4d0d-4371-a2a8-df64a370f432"
CLIENT_SECRET = "9o98Q~767iNq9_SCntzLEEjnfziMSBDOWf3FlaD5"

lst_mail=["chavegrandn@chavegrand.com","collecte_milkoffice@eurial.eu","eaiadmin@allianceinfo.fr"
    ,"exploit_supplyamont@sodiaal.fr", "courrier@laiteriedepamplie.com", "echanges.amont@laita.fr"
    ,"no_reply.eai@lactalis.fr", "Elodie.HERAUD@lamanufacturedulait.com", "infolabo@infolabo.com"
    ,"c.henneveu@cabinetsofar.com"]

TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://outlook.office365.com/.default'
}

response = requests.post(TOKEN_URL, data=payload)
token_data = response.json()

ACCESS_TOKEN = token_data.get("access_token")
if not ACCESS_TOKEN:
    print("Erreur d'authentification :", token_data)
    exit()
print("Token obtenu.")
IMAP_SERVER = "outlook.office365.com"
EMAIL = "echange@terralacta.com"
FOLDER = "/tmp"

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)
try:
    imap_conn = imaplib.IMAP4_SSL(IMAP_SERVER)
    auth_string = f"user={EMAIL}\1auth=Bearer {ACCESS_TOKEN}\1\1"
    imap_conn.authenticate("XOAUTH2", lambda x: auth_string.encode("utf-8"))
    print("Connexion à la boîte mail réussie.")
    # Sélection de la boîte mail (mode read pour ne pas marquer les mails)
    imap_conn.select("INBOX", readonly=True)
    for sender in lst_mail:
        status, email_ids = imap_conn.search(None, f'UNSEEN FROM "{sender}"')
        if status != "OK" or not email_ids[0]:
            print(f"Aucun email non lu trouvé pour {sender}.")
            continue
        email_ids = email_ids[0].split()
        print(f"{len(email_ids)} emails non lus de {sender}")

        for email_id in email_ids:
            # Récupération du mail
            status, msg_data = imap_conn.fetch(email_id, "(RFC822)")

            if status != "OK":
                print(f"Impossible de récupérer l'email {email_id}.")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email, policy=policy.default)

            # Extraction des pièces jointes
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        filepath = os.path.join(FOLDER, filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Pièce jointe enregistrée : {filepath}")
    imap_conn.logout()
    print("Déconnexion.")

except Exception as e:
    print("Erreur de connexion IMAP :", str(e))