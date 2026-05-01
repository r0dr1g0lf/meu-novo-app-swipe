import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Swipe App", layout="centered")[cite: 2]

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False[cite: 2]

if 'resultado_swipe' not in st.session_state:
    st.session_state.resultado_swipe = ""

if not st.session_state.usuario_logado:
    st.title("📱 Bem-vindo!")[cite: 2]
    nome = st.text_input("Qual seu nome?")[cite: 2]
    if st.button("Começar Avaliação"):[cite: 2]
        if nome:
            st.session_state.usuario_logado = True[cite: 2]
            st.session_state.nome_usuario = nome[cite: 2]
            st.rerun()[cite: 2]
        else:
            st.error("Por favor, digite seu nome.")[cite: 2]

else:
    st.write(f"Olá, **{st.session_state.nome_usuario}**! Deslize ou clique:")[cite: 2]
    
    # Exibe a mensagem de texto visível baseada na ação
    if st.session_state.resultado_swipe == "sim":
        st.success("✅ Você se interessou!")
    elif st.session_state.resultado_swipe == "nao":
        st.error("❌ Você não se interessou.")

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
    """[cite: 2]

    components.html(swipe_js, height=550)[cite: 2]

    col1, col2 = st.columns(2)[cite: 2]
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):[cite: 2]
            st.session_state.resultado_swipe = "nao"
            st.rerun()
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):[cite: 2]
            st.session_state.resultado_swipe = "sim"
            st.rerun()
