import streamlit as st
from datetime import datetime

st.set_page_config(page_title="📦 Coleta por Palete")

st.title("📦 Coleta de Palete e Lacres")

# Inicializa etapas
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

def proxima_etapa(etapa):
    st.session_state.etapa = etapa
    st.experimental_rerun()

# Etapa 1: Loja
if st.session_state.etapa == 1:
    st.text_input(
        "Digite a Loja e aperte ENTER", 
        key="loja", 
        on_change=proxima_etapa, 
        args=(2,)
    )

# Etapa 2: Palete
elif st.session_state.etapa == 2:
    st.text_input(
        "Bipar Palete e aperte ENTER", 
        key="palete", 
        on_change=proxima_etapa, 
        args=(3,)
    )

# Etapa 3: Lacres
elif st.session_state.etapa == 3:
    st.text_area("Bipar os Lacres (separados por vírgula)", key="lacres")

    if st.button("Enviar"):
        loja = st.session_state.get("loja", "")
        palete = st.session_state.get("palete", "")
        lacres = st.session_state.get("lacres", "")
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        st.success("✅ Dados enviados com sucesso!")
        st.text(f"📍 Loja: {loja}")
        st.text(f"📦 Palete: {palete}")
        st.text(f"🔒 Lacres: {lacres}")
        st.text(f"🕒 Data/Hora: {agora}")
