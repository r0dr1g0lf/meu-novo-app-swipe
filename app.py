import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Swipe App", layout="centered")

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False

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

else:
    st.write(f"Olá, **{st.session_state.nome_usuario}**! Deslize ou clique:")
    
    swipe_js = """
    <style>
        .swipe-card {
            width: 100%;
            max-width: 400px;
            height: 500px;
            background-image: url('https://picsum.photos/400/500');
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            position: relative;
            touch-action: none;
            user-select: none;
            margin: 0 auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
    </style>
    <div id="card" class="swipe-card"></div>
    <script>
        const card = document.getElementById('card');
        let startX;
        let currentX;

        card.addEventListener('pointerdown', (e) => {
            startX = e.clientX;
            card.style.transition = 'none';
        });

        document.addEventListener('pointermove', (e) => {
            if (!startX) return;
            currentX = e.clientX;
            const diffX = currentX - startX;
            card.style.transform = `translateX(${diffX}px) rotate(${diffX / 20}deg)`;
        });

        document.addEventListener('pointerup', (e) => {
            if (!startX) return;
            const diffX = currentX - startX;
            const threshold = window.innerWidth * 0.4;

            if (diffX > threshold) {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(1000px) rotate(30deg)';
                window.parent.postMessage({type: 'swipe', direction: 'right'}, '*');
            } else if (diffX < -threshold) {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(-1000px) rotate(-30deg)';
                window.parent.postMessage({type: 'swipe', direction: 'left'}, '*');
            } else {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(0px) rotate(0deg)';
            }
            startX = null;
        });
    </script>
    """

    components.html(swipe_js, height=550)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):
            st.toast("Não se interessou.")
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):
            st.toast("Se interessou!", icon="🔥")
