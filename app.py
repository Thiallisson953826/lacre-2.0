import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.set_page_config(page_title="Coleta por Palete - Envio por E-mail")

st.title("📦 Coleta por Palete e Lacres")

# Inicializa variáveis de sessão
if "lacres" not in st.session_state:
    st.session_state.lacres = []
if "novo_lacre" not in st.session_state:
    st.session_state.novo_lacre = ""

# Função para limpar o campo após bipar
def adicionar_lacre():
    novo = st.session_state.novo_lacre.strip()
    if novo and novo not in st.session_state.lacres:
        st.session_state.lacres.append(novo)
    st.session_state.novo_lacre = ""  # Limpa o campo

# Campos principais
sigla_loja = st.text_input("Loja para onde vai (Ex: TDC)")
palete = st.text_input("Bipar o Palete (Ex: PL95382613)")

# Campo do lacre que dispara ação ao alterar
st.text_input("Bipar Lacre (um por vez)", key="novo_lacre", on_change=adicionar_lacre)

# Exibe lacres formatados
lacres_formatados = ", ".join(st.session_state.lacres)
st.text_area("Lacres bipados", value=lacres_formatados, height=100, disabled=True)

# E-mails
emails_identificados = {
    "TLC - thiallisson@live.com": "thiallisson@live.com",
    "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
    "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
    "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br",
    "LOG - logistica@empresa.com": "logistica@empresa.com",
    "SUP - supervisor@empresa.com": "supervisor@empresa.com",
    "LAC - lacrescaixaazul@gmail.com": "lacrescaixaazul@gmail.com"
}

emails_escolhidos = st.multiselect("Escolha os e-mails para envio", list(emails_identificados.keys()))

# Botão enviar
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
            st.session_state.lacres = []
        except Exception as e:
            st.error(f"❌ Erro ao enviar: {e}")
