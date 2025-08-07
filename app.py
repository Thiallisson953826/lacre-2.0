import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Configurações do servidor SMTP (Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "lacrescaixazul@gmail.com"
PASSWORD = "rslzwudhmedqolqo"

st.title("📦 Coleta por Palete - Envio por E-mail")

# Lista de e-mails disponíveis
emails_disponiveis = [
    "destinatario1@gmail.com",
    "destinatario2@gmail.com",
    "destinatario3@gmail.com",
    "thiallisson@live.com"
]

# Seleção de múltiplos e-mails
destinatarios = st.multiselect("Selecione os destinatários:", emails_disponiveis)

assunto = st.text_input("Assunto")
mensagem = st.text_area("Mensagem")

if st.button("Enviar E-mail"):
    if not destinatarios:
        st.error("Selecione pelo menos um destinatário.")
    elif not assunto or not mensagem:
        st.error("Preencha o assunto e a mensagem.")
    else:
        try:
            # Configura o e-mail
            msg = MIMEText(mensagem)
            msg["Subject"] = assunto
            msg["From"] = USERNAME
            msg["To"] = ", ".join(destinatarios)

            # Envia
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(USERNAME, PASSWORD)
                server.sendmail(USERNAME, destinatarios, msg.as_string())

            st.success(f"E-mail enviado com sucesso para: {', '.join(destinatarios)}")

        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
