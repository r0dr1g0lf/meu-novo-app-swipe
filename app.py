import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Swipe App", layout="centered")[cite: 4]

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False[cite: 4]

if not st.session_state.usuario_logado:
    st.title("📱 Bem-vindo!")[cite: 4]
    nome = st.text_input("Qual seu nome?")[cite: 4]
    if st.button("Começar Avaliação"):[cite: 4]
        if nome:
            st.session_state.usuario_logado = True[cite: 4]
            st.session_state.nome_usuario = nome[cite: 4]
            st.rerun()[cite: 4]
        else:
            st.error("Por favor, digite seu nome.")[cite: 4]

else:
    st.write(f"Olá, **{st.session_state.nome_usuario}**! Deslize ou clique:")[cite: 4]
    
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
        }
        #status-msg {
            position: absolute;
            z-index: 1;
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            width: 100%;
            pointer-events: none;
            display: none;
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
            card.style.transform = `translateX(${diffX}px) rotate(${diffX / 20}deg)`;
        });

        document.addEventListener('pointerup', (e) => {
            if (!startX) return;
            const diffX = currentX - startX;
            const threshold = window.innerWidth * 0.4;

            if (diffX > threshold) {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(1000px) rotate(30deg)';
                statusMsg.innerText = "SEINTERESSOU";
                statusMsg.style.color = "green";
                statusMsg.style.display = "block";
                window.parent.postMessage({type: 'swipe', direction: 'right'}, '*');
            } else if (diffX < -threshold) {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(-1000px) rotate(-30deg)';
                statusMsg.innerText = "NÃO SE INTERESSOU";
                statusMsg.style.color = "red";
                statusMsg.style.display = "block";
                window.parent.postMessage({type: 'swipe', direction: 'left'}, '*');
            } else {
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(0px) rotate(0deg)';
            }
            startX = null;
        });
    </script>
    """[cite: 4]

    components.html(swipe_js, height=550)[cite: 4]

    col1, col2 = st.columns(2)[cite: 4]
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):[cite: 4]
            st.toast("Você não se interessou.")[cite: 4]
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):[cite: 4]
            st.toast("Interesse registrado!", icon="🔥")[cite: 4]
