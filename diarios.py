import streamlit as st

def exibir_diarios():
    st.write("Em breve :)")
# # Seleção do bimestre e da disciplina
#     bimestre = st.selectbox('Selecione o Bimestre:', ['1º Bimestre', '2º Bimestre'])
#     disciplina = st.selectbox('Selecione a Disciplina:', ['LP', 'Ing', 'Mat'])

#     # Mapeamento dos dataframes de acordo com o bimestre selecionado
#     if bimestre == '1º Bimestre':
#         if disciplina == 'LP':
#             diario_df = df3.loc[df3['Aluno'] == tutorado, ['ATV1', 'D1', 'ATV2', 'D2']]
#         elif disciplina == 'Ing':
#             diario_df = df1['Ing1']
#         elif disciplina == 'Mat':
#             diario_df = df1['Mat1']
#     else:
#         if disciplina == 'LP':
#             diario_df = df4.loc[df4['Aluno'] == tutorado, ['ATV1', 'D1', 'P1', 'ATV2', 'D2']]
#         elif disciplina == 'Ing':
#             diario_df = df2['Ing2']
#         elif disciplina == 'Mat':
#             diario_df = df2['Mat2']

#     st.write("Diário Selecionado:")
#     for coluna in diario_df.columns:
#         st.write(f"{coluna}: {diario_df[coluna].values[0]}")