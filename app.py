import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Swipe App", layout="centered")

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False

if 'indice_imagem' not in st.session_state:
    st.session_state.indice_imagem = 0

urls_imagens = [
    "https://picsum.photos/id/1011/400/500",
    "https://picsum.photos/id/1012/400/500",
    "https://picsum.photos/id/1013/400/500",
    "https://picsum.photos/id/1014/400/500",
    "https://picsum.photos/id/1015/400/500"
]

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
    
    imagem_atual = urls_imagens[st.session_state.indice_imagem % len(urls_imagens)]
    
    swipe_js = f"""
    <style>
        .container {{
            position: relative;
            width: 100%;
            max-width: 400px;
            height: 500px;
            margin: 0 auto;
            overflow: hidden;
            border-radius: 20px;
        }}
        .swipe-card {{
            width: 100%;
            height: 100%;
            background-image: url('{imagem_atual}');
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            position: absolute;
            touch-action: none;
            user-select: none;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 2;
        }}
        .overlay-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 15px rgba(0,0,0,0.9);
            z-index: 3;
            display: none;
            text-align: center;
            width: 100%;
            pointer-events: none;
            font-family: sans-serif;
        }}
    </style>
    <div class="container">
        <div id="overlay-right" class="overlay-text" style="color: #4CAF50;">SE INTERESSOU</div>
        <div id="overlay-left" class="overlay-text" style="color: #FF5252;">NÃO SE INTERESSOU</div>
        <div id="card" class="swipe-card"></div>
    </div>
    <script>
        const card = document.getElementById('card');
        const overlayRight = document.getElementById('overlay-right');
        const overlayLeft = document.getElementById('overlay-left');
        let startX;
        let currentX;

        card.addEventListener('pointerdown', (e) => {{
            startX = e.clientX;
            card.style.transition = 'none';
        }});

        document.addEventListener('pointermove', (e) => {{
            if (!startX) return;
            currentX = e.clientX;
            const diffX = currentX - startX;
            card.style.transform = `translateX(${{diffX}}px) rotate(${{diffX / 20}}deg)`;
            
            if (diffX > 50) {{
                overlayRight.style.display = 'block';
                overlayLeft.style.display = 'none';
            }} else if (diffX < -50) {{
                overlayLeft.style.display = 'block';
                overlayRight.style.display = 'none';
            }} else {{
                overlayRight.style.display = 'none';
                overlayLeft.style.display = 'none';
            }}
        }});

        document.addEventListener('pointerup', (e) => {{
            if (!startX) return;
            const diffX = currentX - startX;
            const threshold = window.innerWidth * 0.3;

            if (diffX > threshold) {{
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(1000px) rotate(30deg)';
                window.parent.postMessage({{type: 'swipe', direction: 'right'}}, '*');
            }} else if (diffX < -threshold) {{
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(-1000px) rotate(-30deg)';
                window.parent.postMessage({{type: 'swipe', direction: 'left'}}, '*');
            }} else {{
                card.style.transition = '0.3s';
                card.style.transform = 'translateX(0px) rotate(0deg)';
                overlayRight.style.display = 'none';
                overlayLeft.style.display = 'none';
            }}
            startX = null;
        }});
    </script>
    """

    components.html(swipe_js, height=550)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):
            st.session_state.indice_imagem += 1
            st.toast("Você não se interessou.")
            st.rerun()
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):
            st.session_state.indice_imagem += 1
            st.toast("Interesse registrado!", icon="🔥")
            st.rerun()
