import pandas as pd
import streamlit as st
import gspread
import plotly.graph_objects as go

# Acessando as credenciais do secrets.toml
creds = st.secrets["gcp"]

# Set up credentials to access Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
client = gspread.service_account_from_dict(creds)

# Acessando a planilha Google
sheet_name1 = 'Notas'
sheet_name2 = 'PP'

def atualizar_dados():
    global df1, df2, tutores_unicos
    # Acessando a planilha Google
    sheet1 = client.open('Painel2024').worksheet(sheet_name1)
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

def exibir_notas():
    global df1, df2
    atualizar_dados()  # Certifique-se de que os dados estejam atualizados

    col1, col2, col3 = st.columns([1, 3, 1])

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

    with col3:
        if st.button('Atualizar dados'):
            atualizar_dados()

    if 'tutorado' in locals():
        st.title("NOTAS - TUTORADO(A)")
            
        # Obter todas as disciplinas disponíveis
        disciplinas_disponiveis = df1.columns[df1.columns.str.contains('\d+$')].tolist()
            
        # Filtrar apenas as disciplinas presentes no DataFrame do aluno
        disciplinas = [disciplina for disciplina in disciplinas_disponiveis if disciplina in df1.columns]

        if disciplinas:
            notas_df_aluno1 = df1.loc[df1['Aluno'] == tutorado, disciplinas]
                
            disciplinas_com_notas = [coluna for coluna in notas_df_aluno1.columns if notas_df_aluno1[coluna].notnull().any()]

            if disciplinas_com_notas:
                notas_aluno1 = notas_df_aluno1[disciplinas_com_notas].values.tolist()[0]

                fig = go.Figure()
                # Loop sobre as disciplinas
                    for disciplina in disciplinas_com_notas:
                        # Definindo a cor com base no sufixo numérico
                        valor_barra = notas_aluno1[disciplinas_com_notas.index(disciplina)]
                        
                        if disciplina.endswith('1'):
                            cor = 'blue'
                        elif disciplina.endswith('2'):  # Nova condição para a cor verde
                            cor = 'red'
                        else:
                            cor = 'green'
                    
                        fig.add_trace(go.Bar(x=[disciplina], y=[valor_barra], marker_color=cor, text=[valor_barra], textposition='auto'))


                # Atualizar layout para desabilitar todas as opções interativas e travar o gráfico
                fig.update_layout(
                    showlegend=False,
                    xaxis={"fixedrange": True},  # Travar eixo X
                    yaxis={"fixedrange": True},  # Travar eixo Y
                    margin={"l": 0, "r": 0, "t": 0, "b": 0},  # Remover margens
                    dragmode=False,  # Desabilitar o modo de arrastar
                    hovermode=False,  # Desabilitar o modo de hover
                    uirevision="True"  # Impedir que a interface seja alterada
                )

                # Exibir o gráfico no Streamlit
                st.plotly_chart(fig, use_container_width=True)
                st.write("Para entender o gráfico: a disciplina está abreviada e o número indica qual é o bimestre")
            else:
                st.write("Não há notas disponíveis para o tutorado selecionado.")

                # Exibir as médias das notas para cada disciplina

        
        # Resultado da Prova Paulista
        st.title("PROVA PAULISTA")
            
        # Obter todas as disciplinas disponíveis
        disciplinas_disponiveis = df2.columns[df2.columns.str.contains('\d+$')].tolist()
            
        # Filtrar apenas as disciplinas presentes no DataFrame do aluno
        disciplinas = [disciplina for disciplina in disciplinas_disponiveis if disciplina in df2.columns]

        if disciplinas:
            provapaulista_df_aluno1 = df2.loc[df2['Aluno'] == tutorado, disciplinas]
                
            disciplinas_com_notas = [coluna for coluna in provapaulista_df_aluno1.columns if provapaulista_df_aluno1[coluna].notnull().any()]

            if disciplinas_com_notas:
                provapaulista1 = provapaulista_df_aluno1[disciplinas_com_notas].values.tolist()[0]

                fig = go.Figure()
                for disciplina in disciplinas_com_notas:
                # Definindo a cor com base no sufixo numérico
                    valor_barra = provapaulista1[disciplinas_com_notas.index(disciplina)]
                    cor = 'blue' if disciplina.endswith('1') else 'red'
                    fig.add_trace(go.Bar(x=[disciplina], y=[provapaulista1[disciplinas_com_notas.index(disciplina)]], marker_color=cor, text=[valor_barra], textposition='auto'))
                # Atualizar layout para desabilitar todas as opções interativas e travar o gráfico
                    fig.update_layout(
                        showlegend=False,
                        xaxis={"fixedrange": True},  # Travar eixo X
                        yaxis={"fixedrange": True},  # Travar eixo Y
                        margin={"l": 0, "r": 0, "t": 0, "b": 0},  # Remover margens
                        dragmode=False,  # Desabilitar o modo de arrastar
                        hovermode=False,  # Desabilitar o modo de hover
                        uirevision="True"  # Impedir que a interface seja alterada
                    )

                st.plotly_chart(fig, use_container_width=True)
                st.write("Para entender o gráfico: a disciplina está abreviada e o número indica qual é o bimestre. Os valores estão em %")
            else:
                st.write("Não há notas disponíveis para o tutorado selecionado.")

