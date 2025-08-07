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
if "novo_lacre" not in st.session_state:
    st.session_state.novo_lacre = ""
if "emails" not in st.session_state:
    st.session_state.emails = []
if "email_input" not in st.session_state:
    st.session_state.email_input = ""

# Etapa 1: Digitar loja
if st.session_state.etapa == 1:
    loja = st.text_input("Digite a Loja", key="loja_input", on_change=lambda: st.session_state.update({"loja": st.session_state.loja_input, "etapa": 2}))

# Etapa 2: Digitar palete
elif st.session_state.etapa == 2:
    palete = st.text_input("Bipar Palete", key="palete_input", on_change=lambda: st.session_state.update({"palete": st.session_state.palete_input, "etapa": 3}))

# Etapa 3: Bipar lacres
elif st.session_state.etapa == 3:
    st.write(f"📦 Loja: {st.session_state.loja} | Palete: {st.session_state.palete}")

    novo_lacre = st.text_input("Bipar Lacre", key="lacre_input")
    if novo_lacre:
        if novo_lacre in st.session_state.lacres:
            st.warning("⚠️ Lacre já foi bipado!")
        else:
            st.session_state.lacres.append(novo_lacre)
            st.experimental_rerun()

    st.write("✅ Lacres bipados:")
    for i, lacre in enumerate(st.session_state.lacres, start=1):
        st.write(f"{i}. {lacre}")

    # Campo para adicionar e-mails
    st.subheader("📧 Enviar para os e-mails:")
    st.text_input("Digite um e-mail", key="email_input_temp")
    if st.button("➕ Adicionar e-mail"):
        novo_email = st.session_state.email_input_temp.strip()
        if novo_email and novo_email not in st.session_state.emails:
            st.session_state.emails.append(novo_email)
            st.session_state.email_input_temp = ""
            st.experimental_rerun()
        elif novo_email in st.session_state.emails:
            st.warning("Este e-mail já foi adicionado.")
    
    st.write("📬 E-mails adicionados:")
    for email in st.session_state.emails:
        st.write(f"• {email}")

    if st.button("📨 Enviar lacres por e-mail"):
        # Aqui você colocaria o código de envio de e-mail
        st.success("Lacres enviados com sucesso!")
        # Limpa tudo
        st.session_state.etapa = 1
        st.session_state.loja = ""
        st.session_state.palete = ""
        st.session_state.lacres = []
        st.session_state.emails = []
