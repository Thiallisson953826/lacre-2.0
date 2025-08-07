import streamlit as st

st.set_page_config(page_title="📦 Coleta por Palete", layout="wide")

# ---------- BOTÃO FIXO NO CANTO SUPERIOR ESQUERDO ----------
with st.sidebar:
    st.markdown("### 📧 Lista de E-mails")
    if st.button("➕ Adicionar E-mail"):
        st.session_state.show_email_form = True  # Abre o formulário

# ---------- FORMULÁRIO PARA ADICIONAR E-MAIL ----------
if st.session_state.get("show_email_form"):
    with st.sidebar:
        novo_email = st.text_input("Digite o novo e-mail", key="input_email")
        if st.button("Salvar E-mail"):
            if novo_email:
                # Armazena a lista de e-mails
                if "emails" not in st.session_state:
                    st.session_state.emails = []
                st.session_state.emails.append(novo_email)
                st.success(f"E-mail adicionado: {novo_email}")
                st.session_state.show_email_form = False
                st.session_state.input_email = ""
                st.experimental_rerun()
            else:
                st.warning("Digite um e-mail válido.")

# ---------- EXIBIR LISTA DE E-MAILS SALVOS ----------
with st.sidebar:
    if "emails" in st.session_state and st.session_state.emails:
        st.markdown("#### 📃 E-mails cadastrados:")
        for email in st.session_state.emails:
            st.markdown(f"- {email}")

# ---------- INPUT DE LOJA ----------
st.title("📦 Coleta por Palete - Envio por E-mail")

loja = st.text_input("Digite o número da loja e pressione ENTER", key="loja_input")

# ---------- SE TIVER LOJA, MOSTRA O QUE FOR NECESSÁRIO ----------
if loja:
    st.success(f"Loja selecionada: {loja}")
    # Aqui você pode colocar o restante do fluxo do app
    # Exemplo: campos para bipar palete, lacre, enviar e-mail etc.
    palete = st.text_input("📦 Bipar Palete")
    lacre_1 = st.text_input("🔐 Lacre 1")
    lacre_2 = st.text_input("🔐 Lacre 2")
    if st.button("📨 Enviar por e-mail"):
        if st.session_state.get("emails"):
            st.success("E-mail enviado com sucesso!")
        else:
            st.error("Nenhum e-mail cadastrado.")
