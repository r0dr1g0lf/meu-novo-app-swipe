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
        .container {
            position: relative;
            width: 100%;
            height: 550px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background-color: #f0f2f6;
            border-radius: 20px;
        }
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
            z-index: 2;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            cursor: grab;
        }
        .swipe-card:active {
            cursor: grabbing;
        }
        #status-msg {
            position: absolute;
            z-index: 1;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            width: 100%;
            pointer-events: none;
            display: none;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
    </style>
    <div class="container">
        <div id="status-msg"></div>
        <div id="card" class="swipe-card"></div>
    </div>
    <script>
        const card = document.getElementById('card');
        const statusMsg = document.getElementById('status-msg');
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
            const rotation = diffX / 20;
            card.style.transform = `translateX(${diffX}px) rotate(${rotation}deg)`;
        });

        document.addEventListener('pointerup', (e) => {
            if (!startX) return;
            const diffX = currentX - startX;
            const threshold = window.innerWidth * 0.3;

            if (diffX > threshold) {
                card.style.transition = '0.5s';
                card.style.transform = 'translateX(1000px) rotate(30deg)';
                statusMsg.innerText = "SEINTERESSOU";
                statusMsg.style.color = "#28a745";
                statusMsg.style.display = "block";
            } else if (diffX < -threshold) {
                card.style.transition = '0.5s';
                card.style.transform = 'translateX(-1000px) rotate(-30deg)';
                statusMsg.innerText = "NÃO SE INTERESSOU";
                statusMsg.style.color = "#dc3545";
                statusMsg.style.display = "block";
            } else {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(0px) rotate(0deg)';
            }
            startX = null;
        });
    </script>
    """

    components.html(swipe_js, height=560)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):
            st.toast("Você não se interessou.")
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):
            st.toast("Interesse registrado!", icon="🔥")
