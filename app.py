import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.set_page_config(page_title="📦 Coleta por Palete")
st.title("📦 Coleta de Palete e Lacres")

# Inicializa variáveis de estado
for key in ["etapa", "emails_adicionais", "loja_input", "palete_input", "lacres_input", "email_livre"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "etapa" else 1
        if key == "emails_adicionais":
            st.session_state[key] = []

# Funções para avanço de etapa automático
def avancar_etapa_1():
    if st.session_state.loja_input.strip():
        st.session_state.etapa = 2

def avancar_etapa_2():
    if st.session_state.palete_input.strip():
        st.session_state.etapa = 3

# Etapa 1: Loja
if st.session_state.etapa == 1:
    st.text_input("Digite a Loja e aperte ENTER", key="loja_input", on_change=avancar_etapa_1)

# Etapa 2: Palete
elif st.session_state.etapa == 2:
    st.text_input("Bipar Palete e aperte ENTER", key="palete_input", on_change=avancar_etapa_2)

# Etapa 3: Lacres com validação
elif st.session_state.etapa == 3:
    st.text_area("Bipar os Lacres (um por linha ou separados por vírgula)", key="lacres_input")

    if st.session_state.lacres_input:
        lacre_list = [l.strip() for l in st.session_state.lacres_input.replace('\n', ',').split(',') if l.strip()]
        lacre_unicos = list(dict.fromkeys(lacre_list))

        if len(lacre_list) != len(lacre_unicos):
            st.error("⚠️ Existem lacres duplicados! Remova os repetidos antes de continuar.")
        else:
            st.session_state.etapa = 4

# Etapa final: Envio de e-mails
if st.session_state.etapa == 4:
    email_opcoes = {
        "TLC - thiallisson@live.com": "thiallisson@live.com",
        "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
        "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
        "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br"
    }

    st.subheader("📧 E-mails de destino")
    emails_destino = st.multiselect("Escolha os e-mails da lista", options=list(email_opcoes.keys()))

    # Campo para adicionar e-mails extras
    st.text_input("Ou digite um e-mail manualmente e aperte ENTER", key="email_livre")
    novo_email = st.session_state.email_livre.strip()

    if novo_email:
        if re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
            if novo_email not in st.session_state.emails_adicionais:
                st.session_state.emails_adicionais.append(novo_email)
                st.success(f"✅ E-mail adicionado: {novo_email}")
            st.session_state.email_livre = ""
            st.experimental_rerun()
        else:
            st.error("❌ E-mail inválido. Verifique e tente novamente.")

    # Mostrar e-mails manuais adicionados
    if st.session_state.emails_adicionais:
        st.write("📌 E-mails manuais adicionados:")
        for e in st.session_state.emails_adicionais:
            st.write(f"• {e}")

    # Mostrar lista final de e-mails
    todos_emails = [email_opcoes[nome] for nome in emails_destino] + st.session_state.emails_adicionais
    if todos_emails:
        st.write("📬 Lista final de e-mails que receberão a coleta:")
        for e in todos_emails:
            st.write(f"• {e}")

    if st.button("Enviar"):
        loja = st.session_state.loja_input.strip()
        palete = st.session_state.palete_input.strip()
        lacre_list = [l.strip() for l in st.session_state.lacres_input.replace('\n', ',').split(',') if l.strip()]
        lacre_unicos = list(dict.fromkeys(lacre_list))

        if not todos_emails:
            st.warning("⚠️ Nenhum e-mail selecionado ou digitado!")
        else:
            SMTP_SERVER = st.secrets["smtp_server"]
            SMTP_PORT = st.secrets["smtp_port"]
            USER = st.secrets["username"]
            PASSWORD = st.secrets["password"]

            msg = MIMEMultipart()
            msg["Subject"] = f"Coleta {palete} - {loja}"
            msg["From"] = USER
            msg["To"] = ", ".join(todos_emails)

            corpo = f"""
📦 Palete: {palete}
🔒 Lacres: {', '.join(lacre_unicos)}
🏬 Loja: {loja}
🕒 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
            msg.attach(MIMEText(corpo, "plain"))

            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(USER, PASSWORD)
                server.sendmail(USER, todos_emails, msg.as_string())
                server.quit()
                st.success("✅ E-mail enviado com sucesso!")

                # Limpa os dados após envio
                for key in ["etapa", "emails_adicionais", "loja_input", "palete_input", "lacres_input", "email_livre"]:
                    st.session_state[key] = "" if key != "etapa" else 1
            except Exception as e:
                st.error(f"❌ Erro ao enviar: {e}")
