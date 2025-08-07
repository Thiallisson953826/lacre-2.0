import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Configurações do servidor SMTP (Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "lacrescaixaazul@gmail.com"
PASSWORD = "rslzwudhmedqolqo"

st.title("📦 Coleta por Palete - Envio por E-mail")

# Lista fixa de e-mails disponíveis
emails_disponiveis = [
    "thiallisson@live.com",
    "eslandialia@hotmail.com",
    "Wolfman13690@gmail.com",
    "Edvaldo.pereira@armazemparaiba.com.br"
]

# Seleção dos e-mails permitidos
destinatarios = st.multiselect(
    "Selecione os destinatários:",
    options=emails_disponiveis
)

assunto = st.text_input("Assunto")
mensagem = st.text_area("Mensagem")

if st.button("Enviar E-mail"):
    if not destinatarios:
        st.error("Você deve selecionar pelo menos um destinatário.")
    elif not assunto or not mensagem:
        st.error("Assunto e mensagem são obrigatórios.")
    else:
        try:
            # Criação da mensagem
            msg = MIMEText(mensagem)
            msg["Subject"] = assunto
            msg["From"] = USERNAME
            msg["To"] = ", ".join(destinatarios)

            # Envio do e-mail
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(USERNAME, PASSWORD)
                server.sendmail(USERNAME, destinatarios, msg.as_string())

            st.success(f"E-mail enviado com sucesso para: {', '.join(destinatarios)}")

        except Exception as e:
            st.error(f"Erro ao enviar e-mail: {e}")
