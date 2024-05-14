import streamlit as st
from streamlit_option_menu import option_menu
from notas import exibir_notas
from diarios import exibir_diarios
from salas import exibir_salas


#Título no navegador
st.set_page_config(page_title = "Painel - PEI Paula Santos", page_icon=':bar_chart:', layout="wide") 

with st.sidebar:
    selected = option_menu(
        menu_title="Principal",
        options=['Principal', 'Notas', 'Diários', 'Salas'],
    )

if selected == "Principal":
    # Título
    st.title("Painel da PEI Paula Santos")

    # Conteúdo
    st.write(
        """
        Esse painel foi criado com o objetivo de facilitar algumas informações sobre os alunos e alunas da escola PEI
        Professor Paula Santos, da cidade de Salto (SP). As opções que aparecem na barra lateral possuem informações que
        ajudam a entender o desempenho acadêmico do corpo discente e construir estratégias de acordo com as premissas da PEI.
        """
    )

    st.subheader('Dados')
    st.write(
        """
        Todas as informações desse painel são obtidas através do Google Planilhas, no modo leitura. Dessa forma não existe a possibilidade
        de qualquer dado ser modificado através desse painel. ATENÇÃO: Em Notas, caso você ache que as notas não estão batendo, basta clicar no
        botão "Atualizar dado"
        """
    )
 
if selected == "Notas":
    exibir_notas()
if selected == 'Diários':
    exibir_diarios()
if selected == "Salas":
    exibir_salas()



      

