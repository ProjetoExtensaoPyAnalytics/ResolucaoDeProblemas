import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def carregar_dados():
    df1 = pd.read_csv('dados_doencas.csv')
    df2 = pd.read_csv('dados_obitos.csv') 
    df3 = pd.read_csv('doencas_obitos.csv')
    return df1, df2, df3

def plotar_grafico_barras(df, x_col, y_col, color_col=None, title=None, show_legend=False, cores=None):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        barmode='group',
        color_discrete_sequence=cores if cores else px.colors.qualitative.Plotly,
        title=title
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=show_legend,
        width=2000,
        height=500
    )
    return fig

def plotar_grafico_linha(df, x_col, y_col, color_col=None, title=None, show_legend=False, cores=None):
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        color_discrete_sequence=cores if cores else px.colors.qualitative.Plotly,
        title=title
    )
    fig.update_xaxes(type='category')
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        xaxis_tickangle=0,
        showlegend=show_legend,
        width=2000,
        height=500
    )
    return fig

def plotar_grafico_pareto(df_barras, df_linha, x_col, y_barras_col, y_linha_col, title):
    fig = px.bar(
        df_barras,
        x=x_col,
        y=y_barras_col,
        labels={y_barras_col: 'Número de Internações'},
        title=title
    )
    fig.update_traces(hovertemplate='<b>Número de Internações</b>: %{y}<extra></extra>')
    
    fig.add_trace(go.Scatter(
        x=df_linha[x_col],
        y=df_linha[y_linha_col],
        line=dict(color='red', width=2),
        marker=dict(size=8),
        hovertemplate='<b>Número de Óbitos</b>: %{y:.2f}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title='Número de Internações',
        xaxis_tickangle=0,
        hovermode="x unified",
        template='plotly_white',
        yaxis=dict(showgrid=True),
    )
    fig.update_xaxes(type='category')
    return fig

df1, df2, df3 = carregar_dados()

st.write("""
# Painel de Informações sobre as Doenças do Município de Araranguá
""")

cores_personalizadas = [
    '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', 
    '#FF6692', '#B6E880', '#FF97FF', '#FECB52', '#1F77B4', '#FF7F0E',
    '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F',  
    '#BCBD22', '#17BECF'
] 

st.subheader("Evolução dos Casos de Internação ao Longo dos Anos")
fig1 = plotar_grafico_barras(df1, 'Ano', 'Casos', 'Causas', show_legend=False, cores=cores_personalizadas)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Internações por Doença")
doencas = df1['Causas'].unique()
selected_doencas = st.selectbox("Selecione uma causa para internações:", doencas)
filtro_doencas = df1[df1['Causas'] == selected_doencas]
fig2 = plotar_grafico_barras(filtro_doencas, 'Ano', 'Casos')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Evolução dos Casos de Óbitos ao Longo dos Anos")
fig_linha = plotar_grafico_linha(df2, 'Ano', 'Óbitos', 'Causas', cores=cores_personalizadas)
st.plotly_chart(fig_linha, use_container_width=True)

st.subheader("Óbitos por Doença")
obitos = df2['Causas'].unique()
selected_obitos = st.selectbox("Selecione uma causa:", obitos)
filtro_obitos = df2[df2['Causas'] == selected_obitos]
fig3 = plotar_grafico_linha(filtro_obitos, 'Ano', 'Óbitos', cores=cores_personalizadas)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Comparação do Número de Internação e Óbitos")
doencas = df3['Causas'].unique()
selected = st.selectbox("Selecione uma causa de Internação:", doencas)
filtro = df3[df3['Causas'] == selected]

internacoes_por_ano = filtro.groupby('Ano')['Casos'].sum().reset_index()
obitos_por_ano = filtro.groupby('Ano')['Óbitos'].sum().reset_index()

fig4 = plotar_grafico_pareto(internacoes_por_ano, obitos_por_ano,'Ano', 'Casos', 'Óbitos', f'Internações e Óbitos por {selected} ao longo dos anos')
st.plotly_chart(fig4, use_container_width=True)
