import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv('araranguá_doses.csv', sep=';')
    data['dt_vacina'] = pd.to_datetime(data['dt_vacina'])
    return data

dados = load_data()

# Título do app
st.title('Doses aplicadas em Araranguá')

# Sidebar para seleções do usuário
st.sidebar.header('Filtros')

# Seleção múltipla de vacinas
vacinas = sorted(dados['sg_vacina'].unique())
vacinas_selecionadas = st.sidebar.multiselect('Selecione as vacinas:', vacinas, default=[vacinas[0]])

# Determinar o intervalo de datas válido
data_min = dados['dt_vacina'].min().date()
data_max = dados['dt_vacina'].max().date()

# Seleção do intervalo de datas com validação
start_date = st.sidebar.date_input('Data inicial', data_min, min_value=data_min, max_value=data_max)
end_date = st.sidebar.date_input('Data final', data_max, min_value=start_date, max_value=data_max)

# Verificar se as datas selecionadas são válidas
if start_date > end_date:
    st.error('Erro: A data inicial deve ser anterior ou igual à data final.')
    st.stop()

# Seleção do tipo de visualização
tipo_visualizacao = st.sidebar.radio(
    "Selecione o tipo de visualização:",
    ('Diária', 'Semanal', 'Mensal')
)

# Filtrar os dados
dados_filtrados = dados[
    (dados['sg_vacina'].isin(vacinas_selecionadas)) &
    (dados['dt_vacina'].dt.date >= start_date) &
    (dados['dt_vacina'].dt.date <= end_date)
]

# Verificar se há dados no intervalo selecionado
if dados_filtrados.empty:
    st.warning('Não há dados disponíveis para o intervalo de datas e vacinas selecionados.')
    st.stop()

# Função para agrupar os dados
def agrupar_dados(df, tipo):
    if tipo == 'Diária':
        return df.groupby(['dt_vacina', 'sg_vacina']).size().unstack(fill_value=0)
    elif tipo == 'Semanal':
        df['semana'] = df['dt_vacina'].dt.to_period('W').astype(str)
        return df.groupby(['semana', 'sg_vacina']).size().unstack(fill_value=0)
    elif tipo == 'Mensal':
        df['mes'] = df['dt_vacina'].dt.to_period('M').astype(str)
        return df.groupby(['mes', 'sg_vacina']).size().unstack(fill_value=0)

dados_agrupados = agrupar_dados(dados_filtrados, tipo_visualizacao)

# Criar o gráfico usando Plotly
fig = go.Figure()

for vacina in dados_agrupados.columns:
    fig.add_trace(go.Scatter(x=dados_agrupados.index, y=dados_agrupados[vacina],
                             mode='lines', name=vacina))

fig.update_layout(
    title=f'Doses de vacinas aplicadas ({tipo_visualizacao.lower()})',
    xaxis_title='Período',
    yaxis_title='Número de doses',
    legend_title='Vacinas',
    hovermode='x unified'
)

# Configurar o idioma para português
fig.update_layout(
    xaxis=dict(title='Período'),
    yaxis=dict(title='Número de doses'),
    legend=dict(title='Vacinas'),
    hoverlabel=dict(namelength=-1)
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)


contagem_total = dados_agrupados.sum().sum()
st.write('Total de doses aplicadas no período:')
st.metric("Total", f"{contagem_total:,}")

# Distribuição de doses por idade
st.subheader('Distribuição de doses por idade')

# Agrupar dados por idade e vacina
dados_por_idade = dados_filtrados.groupby(['nu_idade_paciente', 'sg_vacina']).size().unstack(fill_value=0)

# Criar gráfico de barras empilhadas para distribuição por idade
fig_idade = go.Figure()

for vacina in dados_por_idade.columns:
    fig_idade.add_trace(go.Bar(x=dados_por_idade.index, y=dados_por_idade[vacina],
                               name=vacina))

fig_idade.update_layout(
    title='Distribuição de doses por idade',
    xaxis_title='Idade',
    yaxis_title='Número de doses',
    barmode='stack',
    legend_title='Vacinas',
    hovermode='x unified'
)

st.plotly_chart(fig_idade, use_container_width=True)

# Estatísticas sobre idades
st.write('Estatísticas de idade:')
col1, col2, col3 = st.columns(3)
col1.metric("Idade mínima", f"{dados_filtrados['nu_idade_paciente'].min()}")
col2.metric("Idade média", f"{dados_filtrados['nu_idade_paciente'].mean():.1f}")
col3.metric("Idade máxima", f"{dados_filtrados['nu_idade_paciente'].max()}")

st.write("Fonte dos dados: https://opendatasus.saude.gov.br/dataset/doses-aplicadas-pelo-programa-de-nacional-de-imunizacoes-pni")


