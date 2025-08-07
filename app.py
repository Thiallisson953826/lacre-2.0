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
if "loja" not in st.session_state:
    st.session_state.loja = ""
if "palete" not in st.session_state:
    st.session_state.palete = ""

# Campo da loja → quando digitar e pressionar Enter, muda para campo palete
def loja_digitada():
    st.session_state.palete_focus = True

# Campo do palete → quando digitar e pressionar Enter, muda para lacre
def palete_digitado():
    st.session_state.lacre_focus = True

# Campo do lacre → ao mudar, já adiciona
def adicionar_lacre():
    novo = st.session_state.novo_lacre.strip()
    if novo and novo not in st.session_state.lacres:
        st.session_state.lacres.append(novo)
    st.session_state.novo_lacre = ""

# CAMPO LOJA
st.text_input("Loja para onde vai (Ex: TDC)", key="loja", on_change=loja_digitada)

# CAMPO PALETE (só foca se loja já foi preenchida)
if st.session_state.get("palete_focus"):
    st.text_input("Bipar o Palete (Ex: PL95382613)", key="palete", on_change=palete_digitado)
else:
    st.text_input("Bipar o Palete (Ex: PL95382613)", key="palete")

# CAMPO LACRE (ativo sempre)
st.text_input("Bipar Lacre (um por vez)", key="novo_lacre", on_change=adicionar_lacre)

# Mostra lista de lacres bipados
lacres_formatados = ", ".join(st.session_state.lacres)
st.text_area("Lacres bipados", value=lacres_formatados, height=100, disabled=True)

# Lista de e-mails
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

# BOTÃO DE ENVIO
if st.button("Enviar"):
    if not (st.session_state.loja and st.session_state.palete and st.session_state.lacres and emails_escolhidos):
        st.warning("⚠️ Preencha todos os campos e bipar pelo menos um lacre!")
    else:
        try:
            SMTP_SERVER = st.secrets["smtp_server"]
            SMTP_PORT = st.secrets["smtp_port"]
            USER = st.secrets["username"]
            PASSWORD = st.secrets["password"]

            lista_emails = [emails_identificados[e] for e in emails_escolhidos]

            msg = MIMEMultipart()
            msg["Subject"] = f"Coleta {st.session_state.palete} - {st.session_state.loja}"
            msg["From"] = USER
            msg["To"] = ", ".join(lista_emails)

            hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            corpo = f"""
Palete: {st.session_state.palete}
Lacres: {lacres_formatados}
Loja de destino: {st.session_state.loja}
Data e hora do envio: {hora_atual}
"""
            msg.attach(MIMEText(corpo, "plain"))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(USER, PASSWORD)
            server.sendmail(USER, lista_emails, msg.as_string())
            server.quit()

            st.success("✅ E-mail enviado com sucesso!")

            # Limpa os campos após envio
            st.session_state.lacres = []
            st.session_state.palete = ""
            st.session_state.loja = ""

        except Exception as e:
            st.error(f"❌ Erro ao enviar: {e}")
