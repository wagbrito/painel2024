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
sheet_name = 'Medias'
sheet = client.open('Painel2024').worksheet(sheet_name)

# Transformando a planilha em um DataFrame
df = pd.DataFrame(sheet.get_all_records())

def exibir_salas():

    #Gráfico de Médias gerais - por bimestre
    st.subheader('Comparativo de médias por bimestre')
    st.write('O gráfico abaixo compara a média das notas por bimestre, excluíndo apenas a disciplina Eletiva')

    df_media_bimestre = df[['Turma', 'M1', 'M2']]
    fig_bim = px.bar(df_media_bimestre, x='Turma', y=['M1', 'M2'], barmode='group')
    fig_bim.update_traces(name='1º Bimestre', selector=dict(name='M1'))
    fig_bim.update_traces(name='2º Bimestre', selector=dict(name='M2'))
    fig_bim.update_layout(yaxis_title='Média', legend=dict(orientation="h", y=1.13))

    # Configurando para mostrar o texto dentro das barras
    fig_bim.update_traces(text=df_media_bimestre['M1'], textposition='auto', selector=dict(name='1º Bimestre'))
    fig_bim.update_traces(text=df_media_bimestre['M2'], textposition='auto', selector=dict(name='2º Bimestre'))

    # Exibindo o gráfico
    st.plotly_chart(fig_bim, use_container_width=True)

    #Gráfico de Médias gerais
    st.subheader('Comparativo de médias gerais')
    st.write('O gráfico abaixo soma as médias de todos os bimestres, excluíndo a disciplina Eletiva')

    df_media_geral = df[['Turma', 'MT']]
    fig_geral = px.bar(df_media_geral, x='Turma', y=['MT'])
    fig_geral.update_layout(yaxis_title='Média geral', legend=dict(orientation="h", y=1.13))
    fig_geral.update_traces(text=df_media_geral['MT'], textposition='inside', showlegend=False)

    st.plotly_chart(fig_geral, use_container_width=True)

    # #Médias por disciplina
    # st.subheader('Comparativo de média por bimestre e disciplina')
    # st.write('O gráfico abaixo permite selecionar um ou mais salas e comparar as médias bimestrais. É possível também selecionar mais que uma disciplina, excluindo Eletiva.')
    # # Selecionar as turmas disponíveis

    # turmas = sorted(df['Turma'].unique())
    # turmas_selecionadas = st.multiselect('Selecione uma ou mais turmas', turmas)

    # # Dataframe das disciplinas
    # df_disciplinas = df[['Turma', 'LP1', 'LP2', 'Ing1', 'Ing2',	'Art1', 'Art2',	'EF1', 'EF2',	'Geo1',	'Geo2',
    #                      'His1', 'His2', 'Mat1', 'Mat2', 'Oe1', 'Oe2', 'Pv1', 'Pv2', 'Tec1', 'Tec2', 'Esp1', 'Esp2',
    #                         'Pe1', 'Pe2', 'Cie1', 'Cie2', 'Fin1', 'Fin2', 'Bio1', 'Bio2', 'Fis1', 'Fis2', 'Qui1', 'Qui2', 'Fil1', 'Fil2', 'Red1', 'Red2']]

    # # Mapear as disciplinas
    # disciplinas = {
    #     'Português': ['LP1', 'LP2'],
    #     'Inglês': ['Ing1', 'Ing2'],
    #     'Educação Física': ['EF1', 'EF2'],
    #     'Arte': ['Art1', 'Art2'],
    #     'Geografia': ['Geo1', 'Geo2'],
    #     'História': ['His1', 'His2'],
    #     'Matemática': ['Mat1', 'Mat2'],
    #     'Ciências': ['Cie1', 'Cie2'],
    #     'Práticas Experimentais': ['Pe1', 'Pe2'],
    #     'Projeto de Vida': ['Pv1', 'Pv2'],
    #     'Orientação de Estudos': ['Oe1', 'Oe2'],
    #     'Tecnologia': ['Tec1', 'Tec2'],
    #     'Educação Financeira': ['Fin1', 'Fin2'],
    #     'Biologia': ['Bio1', 'Bio2'],
    #     'Física': ['Fis1', 'Fis2'],
    #     'Química': ['Qui1', 'Qui2'],
    #     'Filosofia': ['Fil1', 'Fil2'],
    #     'Esporte-Arte-Dança': ['Esp1', 'Esp2'],
    #     'Redação': ['Red1', 'Red2']
    # }

    # # Selecionar as disciplinas desejadas
    # disciplinas_selecionadas = st.multiselect('Selecione uma ou mais disciplinas', list(disciplinas.keys()))

    # # Filtrar os dados
    # dados_filtrados = {}
    # for disciplina in disciplinas_selecionadas:
    #     cols = ['Turma'] + disciplinas[disciplina]
    #     dados_filtrados[disciplina] = df_disciplinas[cols][df_disciplinas['Turma'].isin(turmas_selecionadas)]

    # # Criar o gráfico
    # fig = go.Figure()

    # for disciplina, dados in dados_filtrados.items():
    #     for coluna in dados.columns[1:]:
    #         legenda_disciplina = disciplina
    #         if coluna.endswith('1'):
    #             legenda_disciplina += ' - 1B'
    #         elif coluna.endswith('2'):
    #             legenda_disciplina += ' - 2B'
    #         fig.add_trace(go.Bar(x=dados['Turma'], y=dados[coluna], name=legenda_disciplina))

    # # Personalizar o layout do gráfico
    # fig.update_layout(title='Médias das Disciplinas',
    #                 xaxis_title='Turma',
    #                 yaxis_title='Média',
    #                 barmode='group',
    #                 legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    #                 height=600)

    # # Adicionar rótulos aos eixos x e y
    # fig.update_xaxes(title_font=dict(size=14))
    # fig.update_yaxes(title_font=dict(size=14))

    # # Estilizar as barras
    # fig.update_traces(marker_line_color='black', marker_line_width=0.5)

    #     # Exibir o gráfico
    # st.plotly_chart(fig)

    # Definição das disciplinas
    disciplinas = {
        'Português': ['LP1', 'LP2'],
        'Inglês': ['Ing1', 'Ing2'],
        'Educação Física': ['EF1', 'EF2'],
        'Arte': ['Art1', 'Art2'],
        'Geografia': ['Geo1', 'Geo2'],
        'História': ['His1', 'His2'],
        'Matemática': ['Mat1', 'Mat2'],
        'Ciências': ['Cie1', 'Cie2'],
        'Práticas Experimentais': ['Pe1', 'Pe2'],
        'Projeto de Vida': ['Pv1', 'Pv2'],
        'Orientação de Estudos': ['Oe1', 'Oe2'],
        'Tecnologia': ['Tec1', 'Tec2'],
        'Educação Financeira': ['Fin1', 'Fin2'],
        'Biologia': ['Bio1', 'Bio2'],
        'Física': ['Fis1', 'Fis2'],
        'Química': ['Qui1', 'Qui2'],
        'Filosofia': ['Fil1', 'Fil2'],
        'Esporte-Arte-Dança': ['Esp1', 'Esp2'],
        'Redação': ['Red1', 'Red2']
    }

    # Médias por disciplina
    st.subheader('Comparativo de média por bimestre e disciplina')
    st.write('O gráfico abaixo permite selecionar um ou mais salas e comparar as médias bimestrais. É possível também selecionar mais que uma disciplina, excluindo Eletiva.')

    # Selecionar turmas e disciplinas
    turmas_selecionadas = st.multiselect('Selecione uma ou mais turmas', sorted(df['Turma'].unique()))
    disciplinas_selecionadas = st.multiselect('Selecione uma ou mais disciplinas', list(disciplinas.keys()))

    # Filtrar dados
    df_filtrado = df[['Turma'] + sum(disciplinas.values(), [])]
    df_filtrado = df_filtrado[df_filtrado['Turma'].isin(turmas_selecionadas)]

    # Criar o gráfico
    fig = go.Figure()

    for disciplina, colunas in disciplinas.items():
        if disciplina in disciplinas_selecionadas:
            for coluna in colunas:
                if coluna in df_filtrado.columns:
                    legenda_disciplina = disciplina + (' - 1B' if coluna.endswith('1') else ' - 2B')
                    fig.add_trace(go.Bar(x=df_filtrado['Turma'], y=df_filtrado[coluna], name=legenda_disciplina))

    # Personalizar o layout do gráfico
    fig.update_layout(title='Médias das Disciplinas',
                    xaxis_title='Turma',
                    yaxis_title='Média',
                    barmode='group',
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    height=600)

    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_font=dict(size=14))
    fig.update_yaxes(title_font=dict(size=14))

    # Estilizar as barras
    fig.update_traces(marker_line_color='black', marker_line_width=0.5)

    # Exibir o gráfico
    st.plotly_chart(fig)



    


