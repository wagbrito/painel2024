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
sheet_name1 = 'Notas'
sheet1 = client.open('Painel2024').worksheet(sheet_name1)
sheet_name2 = 'PP'
sheet2 = client.open('Painel2024').worksheet(sheet_name2)

# Transformando a planilha em um DataFrame
df1 = pd.DataFrame(sheet1.get_all_records())
df2 = pd.DataFrame(sheet2.get_all_records())

# Lista de tutores únicos
tutores_unicos_df1 = sorted(df1['Tutor'].unique())
tutores_unicos_df2 = sorted(df2['Tutor'].unique())
tutores_unicos = sorted(set(tutores_unicos_df1).union(tutores_unicos_df2))

#sidebar
with st.sidebar:
    st.write("Paula Santos")

    # Adiciona o selectbox do tutor à primeira coluna
    tutor = st.selectbox('Selecione o(a) tutor(a)', tutores_unicos)

    # Verifica se um tutor foi selecionado
    if tutor:
        # Filtra os dados com base na seleção do tutor
        alunos_do_tutor = sorted(df1.loc[df1['Tutor'] == tutor]['Aluno'])

        # Adiciona o selectbox do tutorado à segunda coluna
        tutorado = st.selectbox('Selecione o(a) tutorado(a)', alunos_do_tutor)

# Verifica se um tutorado foi selecionado
if 'tutorado' in locals():
    st.title("NOTAS - TUTORADO(A)")
    
    # Obter todas as disciplinas disponíveis
    disciplinas_disponiveis = df1.columns[df1.columns.str.contains('\d+$')].tolist()
    
    # Filtrar apenas as disciplinas presentes no DataFrame do aluno
    disciplinas = [disciplina for disciplina in disciplinas_disponiveis if disciplina in df1.columns]

    # Lista para armazenar as disciplinas com valores não nulos para o aluno atual
    disciplinas_com_valores = []

    # Verifica se há valores não nulos para cada disciplina do aluno atual
    for disciplina in disciplinas:
        if df1.loc[df1['Aluno'] == tutorado, disciplina].notnull().any():
            disciplinas_com_valores.append(disciplina)

    if disciplinas_com_valores:
        # Filtrar as notas do aluno atual
        notas_df_aluno1 = df1.loc[df1['Aluno'] == tutorado, disciplinas_com_valores]
        notas_aluno1 = notas_df_aluno1.values.tolist()[0]

        # Cria o gráfico
        fig = go.Figure()
        fig.add_trace(go.Bar(x=disciplinas_com_valores, y=notas_aluno1, name='1º Bimestre', text=notas_aluno1, textposition='auto'))

        # Exibe o gráfico
        st.plotly_chart(fig)
        st.write("Para entender o gráfico: a disciplina está abreviada e o número indica qual é o bimestre")

    # Resultado da Prova Paulista
    st.title("PROVA PAULISTA - 2024")
    
    prova_paulista1 = df2.loc[df2['Aluno'] == tutorado, ['LP1', 'Ing1', 'Mat1', 'Cie1', 'Geo1', 'His1']]
    pp1 = prova_paulista1.values.tolist()[0]

    # Nomes das colunas
    nomes_colunas = ['Português (LP1)', 'Inglês (Ing1)', 'Matemática (Mat1)', 'Ciências (Cie1)', 'Geografia (Geo1)', 'História (His1)']

    # Divide a tela em duas colunas
    col1, col2 = st.columns(2)

    # Exibe as notas da Prova Paulista com os nomes das colunas na primeira coluna
    for i in range(len(pp1)//2):  # Divida o comprimento por 2 para exibir metade das disciplinas em cada coluna
        col1.write(nomes_colunas[i] + ": " + str(pp1[i]))

    # Exibe as notas restantes da Prova Paulista com os nomes das colunas na segunda coluna
    for i in range(len(pp1)//2, len(pp1)):  # Exibe a segunda metade das disciplinas na segunda coluna
        col2.write(nomes_colunas[i] + ": " + str(pp1[i]))

else:
    st.title("PAINEL DE NOTAS PEI PAULA SANTOS - 2024")  # Mensagem de aviso quando nenhum tutor é selecionado
    st.write("Escolha o tutor no menu ao lado para aparecer as informações sobre os alunos")

      

