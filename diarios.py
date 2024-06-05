import pandas as pd
import streamlit as st
import gspread
import plotly.express as px
import plotly.graph_objects as go

# Acessando as credenciais do secrets.toml
creds = st.secrets["gcp"]

# Set up credentials to access Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
client = gspread.service_account_from_dict(creds)

# Acessando a planilha Google
sheet_name1 = 'LP1'
sheet1 = client.open('Painel2024').worksheet(sheet_name1)
sheet_name2 = 'LP2'
sheet2 = client.open('Painel2024').worksheet(sheet_name2)

# Transformando a planilha em um DataFrame
registros1 = sheet1.get_all_records()
registros2 = sheet2.get_all_records()
df1 = pd.DataFrame(registros1).replace('', pd.NA)
df2 = pd.DataFrame(registros2).replace('', pd.NA)

# Lista de tutores únicos
tutores_unicos_df1 = sorted(df1['Tutor'].dropna().unique())
tutores_unicos_df2 = sorted(df2['Tutor'].dropna().unique())
tutores_unicos = sorted(set(tutores_unicos_df1).union(tutores_unicos_df2))

def exibir_diarios():
    st.write("Legenda: ATV = Atividade. D = Descrição. P = Peso. O número indica qual é a atividade.")
    
    col1, col2 = st.columns([1, 3])

    tutorado = None  # Inicializa tutorado com None

    with col1:
        # Adiciona o selectbox do tutor à primeira coluna
        tutor = st.selectbox('Selecione o(a) tutor(a)', [''] + tutores_unicos)

    with col2:
        # Verifica se um tutor foi selecionado
        if tutor:
            # Filtra os dados com base na seleção do tutor
            alunos_do_tutor = sorted(df1.loc[df1['Tutor'] == tutor]['Aluno'])

            # Adiciona o selectbox do tutorado à segunda coluna
            tutorado = st.selectbox('Selecione o(a) tutorado(a)', [''] + alunos_do_tutor)

    # Seleção do bimestre e da disciplina
    bimestre = st.selectbox('Selecione o Bimestre:', ['1º Bimestre', '2º Bimestre'])
    disciplina = st.selectbox('Selecione a Disciplina:', ['LP', 'Ing', 'Mat'])

    if tutorado:  # Verifica se tutorado foi selecionado
        # Mapeamento dos dataframes de acordo com o bimestre selecionado
        if bimestre == '1º Bimestre':
            if disciplina == 'LP':
                diario_df = df1.loc[df1['Aluno'] == tutorado, :]
            elif disciplina == 'Ing':
                diario_df = df1['Ing1']
            elif disciplina == 'Mat':
                diario_df = df1['Mat1']
            separacao = 2  # Definindo a separação para cada duas colunas

        if bimestre == '2º Bimestre':
            if disciplina == 'LP':
                diario_df = df2.loc[df2['Aluno'] == tutorado, :]
            elif disciplina == 'Ing':
                diario_df = df2['Ing2']
            elif disciplina == 'Mat':
                diario_df = df2['Mat2']
            separacao = 3  # Definindo a separação para cada três colunas

        # Substituindo valores <NA> por strings vazias
        diario_df = diario_df.fillna('')
        
        # Excluindo as três primeiras colunas
        colunas_exibidas = diario_df.columns[3:]

        # Exibindo colunas com linha separadora de acordo com o bimestre
        for i, coluna in enumerate(colunas_exibidas, start=1):
            st.write(f"{coluna}: {diario_df[coluna].values[0]}")
            if i % separacao == 0:
                st.write("---")  # Adiciona uma linha separadora
    else:
        st.write("Por favor, selecione um tutorado para visualizar o diário.")

               