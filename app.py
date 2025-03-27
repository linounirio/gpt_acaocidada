import streamlit as st
import os
import io
from google import genai
from google.genai import types
from dotenv import load_dotenv
from time import sleep

st.set_page_config(page_title="Chatbot", layout="wide")

load_dotenv()
CHAVE_API_GEMINI =os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=CHAVE_API_GEMINI)
modelo="gemini-2.0-flash"

def sidebar():
    uploaded = st.file_uploader(label="Escolha os arquivos", type=['pdf'],accept_multiple_files=True)
    
    if uploaded:
        dicionario = {x.name: x for x in uploaded}
        st.session_state['qtd_arq']=len(uploaded)
        for index,objeto in enumerate(uploaded):
            if index==0:
                doc_0=io.BytesIO(objeto.getvalue())
                arq00 = cliente.files.upload(file=doc_0,config=dict(mime_type='application/pdf'))
                st.session_state['arq00']=arq00
            elif index==1:
                doc_1=io.BytesIO(objeto.getvalue())
                arq01 = cliente.files.upload(file=doc_1,config=dict(mime_type='application/pdf'))
                st.session_state['arq01']=arq01
            elif index==2:
                doc_2=io.BytesIO(objeto.getvalue())
                arq02 = cliente.files.upload(file=doc_2,config=dict(mime_type='application/pdf'))
                st.session_state['arq02']=arq02
            elif index==3:
                doc_3=io.BytesIO(objeto.getvalue())
                arq03 = cliente.files.upload(file=doc_3,config=dict(mime_type='application/pdf'))
                st.session_state['arq03']=arq03
            elif index==4:
                doc_4=io.BytesIO(objeto.getvalue())
                arq04 = cliente.files.upload(file=doc_4,config=dict(mime_type='application/pdf'))
                st.session_state['arq04']=arq04
            elif index==5:
                doc_5=io.BytesIO(objeto.getvalue())
                arq05 = cliente.files.upload(file=doc_5,config=dict(mime_type='application/pdf'))
                st.session_state['arq05']=arq05
            else:
                st.warning('Verifique os arquivo pdf')

def bot(prompt_user):
    maximo_tentativas = 1
    repeticao = 0
    sessoes = ['arq00','arq01','arq02','arq03','arq04','arq05']
    qtd = int(st.session_state['qtd_arq'])
    if qtd==1:
        arq00=st.session_state[sessoes[0]]
        content=[arq00,prompt_user]
    elif qtd==2:
        arq00=st.session_state[sessoes[0]]
        arq01=st.session_state[sessoes[1]]
        content=[arq00,arq01,prompt_user]
    elif qtd==3:
        arq00=st.session_state[sessoes[0]]
        arq01=st.session_state[sessoes[1]]
        arq02=st.session_state[sessoes[2]]
        content=[arq00,arq01,arq02,prompt_user]
    elif qtd==4:
        arq00=st.session_state[sessoes[0]]
        arq01=st.session_state[sessoes[1]]
        arq02=st.session_state[sessoes[2]]
        arq03=st.session_state[sessoes[3]]
        content=[arq00,arq01,arq02,arq03,prompt_user]
    elif qtd==5:
        arq00=st.session_state[sessoes[0]]
        arq01=st.session_state[sessoes[1]]
        arq02=st.session_state[sessoes[2]]
        arq03=st.session_state[sessoes[3]]
        arq04=st.session_state[sessoes[4]]
        content=[arq00,arq01,arq02,arq03,arq04,prompt_user]
    elif qtd==6:
        arq00=st.session_state[sessoes[0]]
        arq01=st.session_state[sessoes[1]]
        arq02=st.session_state[sessoes[2]]
        arq03=st.session_state[sessoes[3]]
        arq04=st.session_state[sessoes[4]]
        arq05=st.session_state[sessoes[5]]
        content=[arq00,arq01,arq02,arq03,arq04,arq05,prompt_user]
    #content = [content0,content1,content2,content3,content4,content5]    
    while True:
        try:
            prompt_system = f"""
            Você é um assistente amigável do projeto Ação Cidadã, é especialista em análise de documentação 
            de projetos entre governo e o terceiro setor.
    
            Utilize as informações dos documentos fornecidos para suas respostas.

            Sempre que houver $ na sua saída, substitua por S. 
            """
            resposta = cliente.models.generate_content(
                model=modelo,
                contents=content,
                config=types.GenerateContentConfig(
                    max_output_tokens=8000,
                    temperature=0.2
                )
            )
            return resposta.text
        except Exception as erro:
            repeticao +=1
            if repeticao >= maximo_tentativas:
                return "Erro no Gemini: %s" %erro
            sleep(50)
    
def pag_chat():
    col1,col2=st.columns([0.2,0.8])
    col1.image(image="acaocidada_icon.png")
    col2.header("Bem-vindo(a) ao Assistente", divider=True)
    prompt_user = st.chat_input("Escreva sua pergunta aqui")
    
    if prompt_user:
        #Assistente
        chat=st.chat_message('ai')
        chat.markdown(bot(prompt_user=prompt_user))
        #Humano
        chat= st.chat_message("human")
        chat.markdown(prompt_user)

def main():
    with st.sidebar:
        sidebar()
    pag_chat()

if __name__=="__main__":
    main()