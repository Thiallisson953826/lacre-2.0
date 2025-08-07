import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Coleta por Palete - Envio por E-mail")

st.title("📦 Coleta por Palete - Envio por E-mail")

# Campo para bipar o palete
palete = st.text_input("Bipar Palete")

# Campo para digitar o Lacre 1
lacre1 = st.text_input("Lacre 1")

# Campo para digitar o Lacre 2
lacre2 = st.text_input("Lacre 2")

# Dicionário com siglas
emails_com_sigla = {
    "TLC - thiallisson@live.com": "thiallisson@live.com",
    "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
    "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
    "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br"
}

# Múltipla seleção com rótulo bonitinho
opcoes = list(emails_com_sigla.keys())
selecionados = st.multiselect("Selecione os destinatários", options=opcoes)

# Campo de assunto e mensagem
assunto = st.text_input("Assunto")
mensagem = st.text_area("Mensagem")

# Função de envio
def enviar_email(destinatarios, assunto, mensagem_formatada):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "lacrescaixaazul@gmail.com"
    password = "rslzwudhmedqolqo."

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = assunto

    msg.attach(MIMEText(mensagem_formatada, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, destinatarios, msg.as_string())
        st.success("E-mail enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

# Botão de envio
if st.button("Enviar E-mail"):
    if not selecionados:
        st.warning("Selecione ao menos um destinatário.")
    elif not palete or not lacre1 or not lacre2:
        st.warning("Preencha o palete e os lacres.")
    else:
        # Converte os selecionados para os e-mails reais
        destinatarios = [emails_com_sigla[item] for item in selecionados]

        corpo = f"""
Palete: {palete}
Lacre 1: {lacre1}
Lacre 2: {lacre2}

Mensagem adicional:
{mensagem}
"""
        enviar_email(destinatarios, assunto, corpo)
