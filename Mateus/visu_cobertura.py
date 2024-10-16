import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px



cobertura_ararangua=pd.read_csv('ararangua_cobertura_vacinal.csv')
cobertura_ararangua.drop(' Total', axis=1, inplace=True)


# Anos como índices
cobertura_ararangua=cobertura_ararangua.set_index('Vacina').T
cobertura_ararangua.index = pd.to_numeric(cobertura_ararangua.index)
cobertura_ararangua.index = cobertura_ararangua.index.astype('int')


st.write(""" # Cobertura vacinal em Araranguá """)



# Sidebar para selecionar vacina
vacina_selecionada = st.sidebar.multiselect("Escolha a vacina", cobertura_ararangua.columns)
intervalo=st.sidebar.slider("Escolha os anos que gostaria de selecionar", min_value=2012, max_value=2022, value=(2012, 2022), format="%i")

# Filtrar os dados com base nas seleções
df_filtrado = cobertura_ararangua.loc[intervalo[0]:intervalo[1], vacina_selecionada]

# Gráfico de linha usando Plotly
if not df_filtrado.empty:
    fig = px.line(df_filtrado, x=df_filtrado.index, y=df_filtrado.columns,
                  title='Doses de vacinas aplicadas ao longo do tempo',
                  labels={'value': 'Número de doses', 'variable': 'Vacina', 'index': 'Ano'},
                  line_shape='linear')
    fig.update_layout(xaxis=dict(tickmode='linear', dtick=1),
                      legend_title_text='Vacina')
    st.plotly_chart(fig)
else:
    st.write("Por favor, selecione pelo menos uma vacina para visualizar os dados.")


st.write("Fonte dos dados: https://datasus.saude.gov.br/acesso-a-informacao/imunizacoes-desde-1994/")
