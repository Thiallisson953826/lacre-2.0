import streamlit as st

# Inicializa os estados
if "etapa" not in st.session_state:
    st.session_state.etapa = 1
if "loja" not in st.session_state:
    st.session_state.loja = ""
if "palete" not in st.session_state:
    st.session_state.palete = ""
if "lacres" not in st.session_state:
    st.session_state.lacres = []
if "emails" not in st.session_state:
    st.session_state.emails = []
if "show_email_input" not in st.session_state:
    st.session_state.show_email_input = False
if "loja_input_val" not in st.session_state:
    st.session_state.loja_input_val = ""
if "palete_input_val" not in st.session_state:
    st.session_state.palete_input_val = ""
if "novo_email_temp" not in st.session_state:
    st.session_state.novo_email_temp = ""

# --------- BARRA LATERAL DE E-MAILS ---------
with st.sidebar:
    st.subheader("📧 Lista de E-mails")

    if st.button("➕ Adicionar e-mail"):
        st.session_state.show_email_input = not st.session_state.show_email_input

    if st.session_state.show_email_input:
        st.session_state.novo_email_temp = st.text_input("Digite um e-mail", value=st.session_state.novo_email_temp)
        if st.button("✅ Confirmar e-mail"):
            email = st.session_state.novo_email_temp.strip()
            if email and email not in st.session_state.emails:
                st.session_state.emails.append(email)
                st.success("E-mail adicionado!")
                st.session_state.novo_email_temp = ""
                st.session_state.show_email_input = False
            elif email in st.session_state.emails:
                st.warning("Este e-mail já foi adicionado.")

    for email in st.session_state.emails:
        st.write(f"• {email}")

# --------- ETAPAS PRINCIPAIS ---------
st.title("📦 Coleta por Palete")

# Etapa 1: Digitar loja
if st.session_state.etapa == 1:
    loja = st.text_input("Digite a Loja", key="loja_input_key", value=st.session_state.loja_input_val)
    if loja:
        st.session_state.loja = loja
        st.session_state.etapa = 2
        st.session_state.loja_input_val = ""
        st.experimental_rerun()

# Etapa 2: Digitar palete
elif st.session_state.etapa == 2:
    palete = st.text_input("Bipar Palete", key="palete_input_key", value=st.session_state.palete_input_val)
    if palete:
        st.session_state.palete = palete
        st.session_state.etapa = 3
        st.session_state.palete_input_val = ""
        st.experimental_rerun()

# Etapa 3: Bipar lacres
elif st.session_state.etapa == 3:
    st.write(f"📍 Loja: {st.session_state.loja} | 📦 Palete: {st.session_state.palete}")

    novo_lacre = st.text_input("Bipar Lacre", key="lacre_input_key")
    if novo_lacre:
        if novo_lacre in st.session_state.lacres:
            st.warning("⚠️ Lacre já foi bipado!")
        else:
            st.session_state.lacres.append(novo_lacre)
            st.experimental_rerun()

    st.write("✅ Lacres bipados:")
    for i, lacre in enumerate(st.session_state.lacres, start=1):
        st.write(f"{i}. {lacre}")

    if st.button("📨 Enviar lacres por e-mail"):
        if not st.session_state.emails:
            st.error("Adicione pelo menos um e-mail na barra lateral!")
        elif not st.session_state.lacres:
            st.error("Nenhum lacre bipado.")
        else:
            # Aqui entra o código de envio de e-mail real se quiser
            st.success("Lacres enviados com sucesso!")
            # Limpa tudo
            st.session_state.etapa = 1
            st.session_state.loja = ""
            st.session_state.palete = ""
            st.session_state.lacres = []
            st.session_state.emails = []
            st.session_state.show_email_input = False
            st.session_state.loja_input_val = ""
            st.session_state.palete_input_val = ""
            st.session_state.novo_email_temp = ""
            st.experimental_rerun()
