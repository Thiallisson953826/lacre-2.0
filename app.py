import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="📦 Coleta por Palete")

st.title("📦 Coleta de Palete e Lacres")

# Inicializa variáveis de estado
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

# Etapa 1: Loja
if st.session_state.etapa == 1:
    loja = st.text_input("Digite a Loja e aperte ENTER", key="loja_input")
    if loja:
        st.session_state.loja = loja
        st.session_state.etapa = 2
        st.experimental_rerun()

# Etapa 2: Palete
elif st.session_state.etapa == 2:
    palete = st.text_input("Bipar Palete e aperte ENTER", key="palete_input")
    if palete:
        st.session_state.palete = palete
        st.session_state.etapa = 3
        st.experimental_rerun()

# Etapa 3: Lacres
elif st.session_state.etapa == 3:
    lacres = st.text_area("Bipar os Lacres (separados por vírgula)", key="lacres_input")
    if lacres:
        st.session_state.lacres = lacres

# Etapa final: E-mails e Envio
if st.session_state.etapa >= 3:
    # Emails disponíveis
    email_opcoes = {
        "TLC - thiallisson@live.com": "thiallisson@live.com",
        "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
        "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
        "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br"
    }

    emails_destino = st.multiselect("Escolha os e-mails para envio", options=list(email_opcoes.keys()))

    if st.button("Enviar"):
        loja = st.session_state.get("loja", "")
        palete = st.session_state.get("palete", "")
        lacres = st.session_state.get("lacres", "")
        
        if not (loja and palete and lacres and emails_destino):
            st.warning("⚠️ Preencha todos os campos!")
        else:
            # Dados do e-mail
            SMTP_SERVER = st.secrets["smtp_server"]
            SMTP_PORT = st.secrets["smtp_port"]
            USER = st.secrets["username"]
            PASSWORD = st.secrets["password"]

            emails_real = [email_opcoes[nome] for nome in emails_destino]

            msg = MIMEMultipart()
            msg["Subject"] = f"Coleta {palete} - {loja}"
            msg["From"] = USER
            msg["To"] = ", ".join(emails_real)

            corpo = f"""
📦 Palete: {palete}
🔒 Lacres: {lacres}
🏬 Loja: {loja}
🕒 Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""

            msg.attach(MIMEText(corpo, "plain"))

            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(USER, PASSWORD)
                server.sendmail(USER, emails_real, msg.as_string())
                server.quit()
                st.success("✅ E-mail enviado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao enviar: {e}")
