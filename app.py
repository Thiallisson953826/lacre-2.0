import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.title("📦 Coleta de Palete e Lacres")

# Campos de entrada
sigla_loja = st.text_input("Loja para onde vai (Ex: TDC)")
palete = st.text_input("Bipar o Palete (Ex: PL95382613)")
lacres = st.text_input("Digitar os Lacres (separados por vírgula)")

# Lista de e-mails com siglas para identificar melhor
emails_identificados = {
    "TLC - thiallisson@live.com": "thiallisson@live.com",
    "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
    "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
    "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br",
    "LOG - logistica@empresa.com": "logistica@empresa.com",
    "SUP - supervisor@empresa.com": "supervisor@empresa.com",
    "LAC - lacrescaixaazul@gmail.com": "lacrescaixaazul@gmail.com"
    # Pode adicionar mais aqui tranquilamente
}

# Multiselect para escolher um ou mais e-mails
emails_escolhidos = st.multiselect("Escolha os e-mails para envio", list(emails_identificados.keys()))

# Botão para enviar
if st.button("Enviar"):
    if not (sigla_loja and palete and lacres and emails_escolhidos):
        st.warning("⚠️ Preencha todos os campos!")
    else:
        try:
            # Configurações do servidor
            SMTP_SERVER = st.secrets["smtp_server"]
            SMTP_PORT = st.secrets["smtp_port"]
            USER = st.secrets["username"]
            PASSWORD = st.secrets["password"]

            # Converte os e-mails selecionados
            lista_emails = [emails_identificados[e] for e in emails_escolhidos]

            # Monta o e-mail
            msg = MIMEMultipart()
            msg["Subject"] = f"Coleta {palete} - {sigla_loja}"
            msg["From"] = USER
            msg["To"] = ", ".join(lista_emails)  # todos no "Para", ou use BCC se preferir

            corpo = f"""
Palete: {palete}
Lacres: {lacres}
Loja de destino: {sigla_loja}
Data e hora do envio: {datetime.now():%d/%m/%Y %H:%M:%S}
"""

            msg.attach(MIMEText(corpo, "plain"))

            # Envia o e-mail
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(USER, PASSWORD)
            server.sendmail(USER, lista_emails, msg.as_string())
            server.quit()

            st.success("✅ E-mail enviado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao enviar: {e}")

