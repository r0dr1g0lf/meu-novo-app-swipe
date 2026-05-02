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
            
            for i, u in enumerate(banco_usuarios):
                if u['nome'] == nome:
                    banco_usuarios.pop(i)
            
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
    col_perfil1, col_perfil2 = st.columns([1, 4])
    with col_perfil1:
        st.image(st.session_state.foto_usuario, width=70)
    with col_perfil2:
        st.write(f"Olá, **{st.session_state.nome_usuario}**!")
    
    outros_usuarios = [u for u in banco_usuarios if u['nome'] != st.session_state.nome_usuario]
    
    if len(outros_usuarios) > 0:
        idx = st.session_state.indice_imagem % len(outros_usuarios)
        usuario_atual = outros_usuarios[idx]
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
        </style>
        <div class="container">
            <div id="card" class="swipe-card">
                <div class="name-label">{nome_exibido}</div>
            </div>
        </div>
        """

        components.html(swipe_js, height=520)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Pular", use_container_width=True):
                st.session_state.indice_imagem += 1
                st.rerun()
        with col2:
            if st.button("Direita (Match) ➡️", use_container_width=True):
                meu_nome = st.session_state.nome_usuario
                nome_alvo = nome_exibido
                
                if meu_nome not in interesses:
                    interesses[meu_nome] = set()
                interesses[meu_nome].add(nome_alvo)
                
                if nome_alvo in interesses and meu_nome in interesses[nome_alvo]:
                    st.success(f"Match com {nome_alvo}!")
                    st.balloons()
                else:
                    st.toast(f"Interesse em {nome_alvo} enviado!")
                
                st.session_state.indice_imagem += 1
                st.rerun()
    else:
        st.info("Aguardando novas pessoas entrarem...")
        
    st.divider()
    
    if st.button("Atualizar Lista"):
        st.rerun()

    if st.button("Sair / Trocar Foto"):
        st.session_state.usuario_logado = False
        st.rerun()
