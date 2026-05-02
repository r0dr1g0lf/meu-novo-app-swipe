import streamlit as st
import streamlit.components.v1 as components
import base64
import time

st.set_page_config(page_title="Swipe App", layout="centered")

@st.cache_resource
def obter_banco_dados():
    return []

@st.cache_resource
def obter_interesses():
    return {}

banco_usuarios = obter_banco_dados()
interesses = obter_interesses()

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False

if 'indice_imagem' not in st.session_state:
    st.session_state.indice_imagem = 0

def get_image_base64(image_file):
    if hasattr(image_file, 'getvalue'):
        return base64.b64encode(image_file.getvalue()).decode()
    return None

if not st.session_state.usuario_logado:
    st.title("📱 Bem-vindo!")
    nome = st.text_input("Qual seu nome?")
    
    metodo_foto = st.radio("Como deseja adicionar sua foto?", ["Carregar arquivo", "Tirar foto"])
    
    foto_perfil = None
    if metodo_foto == "Carregar arquivo":
        foto_perfil = st.file_uploader("Escolha uma foto", type=['png', 'jpg', 'jpeg'])
    else:
        foto_perfil = st.camera_input("Tirar foto")

    if st.button("Começar Avaliação"):
        if nome and foto_perfil:
            foto_base64 = get_image_base64(foto_perfil)
            banco_usuarios.append({"nome": nome, "foto": foto_base64})
            
            st.session_state.usuario_logado = True
            st.session_state.nome_usuario = nome
            st.session_state.foto_usuario = foto_perfil
            st.rerun()
        elif not nome:
            st.error("Por favor, digite seu nome.")
        elif not foto_perfil:
            st.error("Por favor, adicione uma foto.")

else:
    # Componente invisível para forçar a atualização da página a cada 5 segundos
    # Isso garante que novos cadastros apareçam para quem já está logado
    components.html(
        """
        <script>
        window.parent.document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                window.parent.location.reload();
            }, 5000); 
        });
        </script>
        """,
        height=0,
    )

    col_perfil1, col_perfil2 = st.columns([1, 4])
    with col_perfil1:
        st.image(st.session_state.foto_usuario, width=70)
    with col_perfil2:
        st.write(f"Olá, **{st.session_state.nome_usuario}**! Deslize ou clique:")
    
    outros_usuarios = [u for u in banco_usuarios if u['nome'] != st.session_state.nome_usuario]
    
    if len(outros_usuarios) > 0:
        usuario_atual = outros_usuarios[st.session_state.indice_imagem % len(outros_usuarios)]
        imagem_data = f"data:image/png;base64,{usuario_atual['foto']}"
        nome_exibido = usuario_atual['nome']
        
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
                background-image: url('{imagem_data}');
                background-size: cover;
                background-position: center;
                border-radius: 20px;
                position: absolute;
                touch-action: none;
                user-select: none;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                z-index: 2;
            }}
            .name-label {{
                position: absolute;
                bottom: 20px;
                left: 20px;
                color: white;
                font-family: sans-serif;
                font-size: 28px;
                font-weight: bold;
                text-shadow: 2px 2px 8px rgba(0,0,0,1);
                z-index: 4;
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
                z-index: 5;
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
            <div id="card" class="swipe-card">
                <div class="name-label">{nome_exibido}</div>
            </div>
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
                meu_nome = st.session_state.nome_usuario
                nome_alvo = nome_exibido
                
                if meu_nome not in interesses:
                    interesses[meu_nome] = set()
                interesses[meu_nome].add(nome_alvo)
                
                if nome_alvo in interesses and meu_nome in interesses[nome_alvo]:
                    st.success(f"Match com {nome_alvo}!")
                    st.balloons()
                else:
                    st.toast("Interesse registrado!", icon="🔥")
                
                st.session_state.indice_imagem += 1
                st.rerun()
    else:
        st.info("Aguardando outros usuários se cadastrarem para exibir as fotos.")
        st.write("A página atualizará automaticamente quando houver novos usuários.")
        time.sleep(2)
        st.rerun()
