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
if "enviado" not in st.session_state:
    st.session_state.enviado = False

# Avança para etapa 2
def etapa_2():
    st.session_state.etapa = 2

# Avança para etapa 3
def etapa_3():
    st.session_state.etapa = 3

# Etapa 1: Loja
if st.session_state.etapa == 1:
    st.text_input("Digite a Loja e aperte ENTER", key="loja", on_change=etapa_2)

# Etapa 2: Palete
elif st.session_state.etapa == 2:
    st.text_input("Bipar Palete e aperte ENTER", key="palete", on_change=etapa_3)

# Etapa 3: Lacres + Email
elif st.session_state.etapa == 3 and not st.session_state.enviado:
    st.text_area("Bipar os Lacres (separados por vírgula)", key="lacres")

    email_opcoes = {
        "TLC - thiallisson@live.com": "thiallisson@live.com",
        "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
        "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
        "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br"
    }

    emails_destino = st.multiselect("Escolha os e-mails para envio", options=list(email_opcoes.keys()), key="emails")

    if st.button("📤 Enviar"):
        loja = st.session_state.get("loja", "")
        palete = st.session_state.get("palete", "")
        lacres = st.session_state.get("lacres", "")
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if not (loja and palete and lacres and emails_destino):
            st.warning("⚠️ Preencha todos os campos!")
        else:
            emails_real = [email_opcoes[nome] for nome in emails_destino]

            # Configuração do e-mail (requer configuração no secrets)
            try:
                SMTP_SERVER = st.secrets["smtp_server"]
                SMTP_PORT = st.secrets["smtp_port"]
                USER = st.secrets["username"]
                PASSWORD = st.secrets["password"]

                msg = MIMEMultipart()
                msg["Subject"] = f"Coleta {palete} - {loja}"
                msg["From"] = USER
                msg["To"] = ", ".join(emails_real)

                corpo = f"""
📦 Palete: {palete}
🔒 Lacres: {lacres}
🏬 Loja: {loja}
🕒 Data/Hora: {agora}
"""

                msg.attach(MIMEText(corpo, "plain"))

                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(USER, PASSWORD)
                server.sendmail(USER, emails_real, msg.as_string())
                server.quit()

                st.success("✅ E-mail enviado com sucesso!")
                st.session_state.enviado = True

                # Exibe resumo
                st.markdown(f"""
                **📍 Loja:** {loja}  
                **📦 Palete:** {palete}  
                **🔒 Lacres:** {lacres}  
                **📧 Enviado para:** {", ".join(emails_real)}  
                **🕒 Data/Hora:** {agora}
                """)
            except Exception as e:
                st.error(f"❌ Erro ao enviar: {e}")
