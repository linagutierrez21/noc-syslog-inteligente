import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT", SENDER_EMAIL)

def enviar_alerta_correo(asunto: str, cuerpo: str):
    """Envía una alerta de manera segura por correo electrónico (Gmail SMTP)."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("⚠️ [Advertencia] Credenciales de correo no configuradas en el archivo .env")
        return False
    
    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = SENDER_EMAIL
    msg["To"] = ALERT_RECIPIENT
    
    try:
        # Conexión segura con el servidor SMTP de Gmail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Inicia la seguridad TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("✅ Alerta de correo electrónico de Gmail enviada exitosamente.")
            return True
    except Exception as e:
        print(f"❌ Error al enviar el correo electrónico por Gmail: {e}")
        return False