import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Swipe App", layout="centered")

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False[cite: 1]

if 'indice_imagem' not in st.session_state:
    st.session_state.indice_imagem = 0[cite: 1]

if 'banco_de_fotos' not in st.session_state:
    st.session_state.banco_de_fotos = [
        "https://picsum.photos/id/1011/400/500",
        "https://picsum.photos/id/1012/400/500",
        "https://picsum.photos/id/1013/400/500",
        "https://picsum.photos/id/1014/400/500",
        "https://picsum.photos/id/1015/400/500"
    ]

if not st.session_state.usuario_logado:
    st.title("📱 Bem-vindo!")
    nome = st.text_input("Qual seu nome?")[cite: 1]
    
    metodo_foto = st.radio("Como deseja adicionar sua foto?", ["Carregar arquivo", "Tirar foto"])[cite: 1]
    
    foto_perfil = None
    if metodo_foto == "Carregar arquivo":
        foto_perfil = st.file_uploader("Escolha uma foto", type=['png', 'jpg', 'jpeg'])[cite: 1]
    else:
        foto_perfil = st.camera_input("Tirar foto")[cite: 1]

    if st.button("Começar Avaliação"):
        if nome and foto_perfil:
            st.session_state.usuario_logado = True[cite: 1]
            st.session_state.nome_usuario = nome[cite: 1]
            st.session_state.foto_usuario = foto_perfil[cite: 1]
            st.session_state.banco_de_fotos.append(foto_perfil)
            st.rerun()[cite: 1]
        elif not nome:
            st.error("Por favor, digite seu nome.")[cite: 1]
        elif not foto_perfil:
            st.error("Por favor, adicione uma foto.")[cite: 1]

else:
    col_perfil1, col_perfil2 = st.columns([1, 4])[cite: 1]
    with col_perfil1:
        st.image(st.session_state.foto_usuario, width=70)[cite: 1]
    with col_perfil2:
        st.write(f"Olá, **{st.session_state.nome_usuario}**! Deslize ou clique:")[cite: 1]
    
    imagem_atual = st.session_state.banco_de_fotos[st.session_state.indice_imagem % len(st.session_state.banco_de_fotos)]
    
    if hasattr(imagem_atual, 'read'):
        bytes_data = imagem_atual.getvalue()
        base64_image = base64.b64encode(bytes_data).decode()
        img_src = f"data:image/jpeg;base64,{base64_image}"
    else:
        img_src = imagem_atual[cite: 1]

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
            background-image: url('{img_src}');
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
    """[cite: 1]

    components.html(swipe_js, height=550)[cite: 1]

    col1, col2 = st.columns(2)[cite: 1]
    with col1:
        if st.button("⬅️ Esquerda (Não)", use_container_width=True):[cite: 1]
            st.session_state.indice_imagem += 1[cite: 1]
            st.toast("Você não se interessou.")[cite: 1]
            st.rerun()[cite: 1]
    with col2:
        if st.button("Direita (Sim) ➡️", use_container_width=True):[cite: 1]
            st.session_state.indice_imagem += 1[cite: 1]
            st.toast("Interesse registrado!", icon="🔥")[cite: 1]
            st.rerun()[cite: 1]
