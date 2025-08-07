import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.set_page_config(page_title="Coleta por Palete - Envio por E-mail")

st.title("📦 Coleta por Palete e Lacres")

# Inicializa a lista de lacres na sessão
if "lacres" not in st.session_state:
    st.session_state.lacres = []

# Campos principais
sigla_loja = st.text_input("Loja para onde vai (Ex: TDC)")
palete = st.text_input("Bipar o Palete (Ex: PL95382613)")

# Campo para bipar lacre individual
novo_lacre = st.text_input("Bipar Lacre (pressione Enter para adicionar)")

# Se um novo lacre foi digitado
if novo_lacre:
    if novo_lacre not in st.session_state.lacres:
        st.session_state.lacres.append(novo_lacre)
    # Limpa o campo após bipar
    st.experimental_rerun()

# Exibe os lacres bipados em uma linha
lacres_formatados = ", ".join(st.session_state.lacres)
st.text_area("Lacres bipados", value=lacres_formatados, height=100, disabled=True)

# Lista de e-mails com siglas
emails_identificados = {
    "TLC - thiallisson@live.com": "thiallisson@live.com",
    "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
    "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
    "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br",
    "LOG - logistica@empresa.com": "logistica@empresa.com",
    "SUP - supervisor@empresa.com": "supervisor@empresa.com",
    "LAC - lacrescaixaazul@gmail.com": "lacrescaixaazul@gmail.com"
}

# Seleção de múltiplos e-mails
emails_escolhidos = st.multiselect("Escolha os e-mails para envio", list(emails_identificados.keys()))

# Botão de enviar
if st.button("Enviar"):
    if not (sigla_loja and palete and st.session_state.lacres and emails_escolhidos):
        st.warning("⚠️ Preencha todos os campos e bipar pelo menos um lacre!")
    else:
        try:
            SMTP_SERVER = st.secrets["smtp_server"]
            SMTP_PORT = st.secrets["smtp_port"]
            USER = st.secrets["username"]
            PASSWORD = st.secrets["password"]

            lista_emails = [emails_identificados[e] for e in emails_escolhidos]

            msg = MIMEMultipart()
            msg["Subject"] = f"Coleta {palete} - {sigla_loja}"
            msg["From"] = USER
            msg["To"] = ", ".join(lista_emails)

            corpo = f"""
Palete: {palete}
Lacres: {lacres_formatados}
Loja de destino: {sigla_loja}
Data e hora do envio: {datetime.now():%d/%m/%Y %H:%M:%S}
"""
            msg.attach(MIMEText(corpo, "plain"))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(USER, PASSWORD)
            server.sendmail(USER, lista_emails, msg.as_string())
            server.quit()

            st.success("✅ E-mail enviado com sucesso!")
            st.session_state.lacres = []  # Limpa os lacres depois de enviar
        except Exception as e:
            st.error(f"❌ Erro ao enviar: {e}")

