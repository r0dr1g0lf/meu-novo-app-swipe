import streamlit as st

# Configuração para parecer um app de celular
st.set_page_config(page_title="Swipe App", layout="centered")

# Simulação simples de banco de dados na sessão
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False

# --- TELA DE CADASTRO/LOGIN ---
if not st.session_state.usuario_logado:
    st.title("📱 Bem-vindo!")
    nome = st.text_input("Qual seu nome?")
    if st.button("Começar Avaliação"):
        if nome:
            st.session_state.usuario_logado = True
            st.session_state.nome_usuario = nome
            st.rerun()
        else:
            st.error("Por favor, digite seu nome.")

# --- TELA DE SWIPE ---
else:
    st.write(f"Olá, **{st.session_state.nome_usuario}**! Deslize ou clique:")
    
    # Exemplo de imagem
    st.image("https://picsum.photos/400/500", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):
            st.toast("Você não se interessou.")
            # Aqui depois salvaremos no banco
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):
            st.toast("Interesse registrado!", icon="🔥")
            # Aqui depois salvaremos no banco