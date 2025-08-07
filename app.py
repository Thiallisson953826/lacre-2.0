import streamlit as st
import re

st.set_page_config(page_title="📦 Coleta por Palete - Envio por E-mail", layout="wide")

# Inicializa session_state para lista de e-mails
if "emails_adicionais" not in st.session_state:
    st.session_state.emails_adicionais = []

# Função para adicionar e-mail
def adicionar_email():
    novo_email = st.session_state.get("novo_email_input", "")
    if re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
        if novo_email not in st.session_state.emails_adicionais:
            st.session_state.emails_adicionais.append(novo_email)
            st.success(f"E-mail adicionado: {novo_email}")
            st.session_state.novo_email_input = ""  # Limpa o campo
        else:
            st.warning("Este e-mail já foi adicionado.")
    else:
        st.error("E-mail inválido.")

# ---------------------------
# 🔼 FIXO EM TODAS AS TELAS
# ---------------------------
with st.container():
    st.markdown("### ✉️ Adicionar E-mail")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input("Digite o e-mail", key="novo_email_input", label_visibility="collapsed")
    with col2:
        st.button("➕ Adicionar E-mail", on_click=adicionar_email, use_container_width=True)

    # Lista de e-mails
    if st.session_state.emails_adicionais:
        st.markdown("**E-mails adicionados:**")
        for i, email in enumerate(st.session_state.emails_adicionais, 1):
            st.write(f"{i}. {email}")
# ---------------------------

# AQUI CONTINUA O RESTANTE DO TEU APP 👇

st.title("📦 Coleta por Palete - Envio por E-mail")

# Campo para bipar o palete
palete = st.text_input("Bipar Palete")

# Campo para digitar o Lacre 1
lacre1 = st.text_input("Lacre 1")

# Campo para digitar o Lacre 2
lacre2 = st.text_input("Lacre 2")

# Simulação de envio (exemplo)
if st.button("Enviar Palete"):
    st.success("Palete enviado com sucesso!")

# AQUI ENTRARIA TODO O RESTO DO TEU PROCESSO...
