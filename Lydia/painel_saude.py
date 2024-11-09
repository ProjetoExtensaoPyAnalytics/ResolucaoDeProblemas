import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados():
    df4 = pd.read_csv('obitos_completo.csv')  # Dados adicionais para óbitos
    return df4

def transformar_dados(df):
    df_melted = df.melt(
        id_vars=['Indicador', 'Etiqueta'],
        value_vars=[str(ano) for ano in range(2006, 2023)],
        var_name='Ano',
        value_name='Valor'
    )
    df_melted['Ano'] = df_melted['Ano'].astype(int)
    return df_melted

def plotar_bagrupada(df, tipo='barra', x_col='Ano', y_col='Valor', color_col=None, title=None, show_legend=False, cores=None):
    if tipo == 'barra_agrupada':
        fig1 = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            barmode='group',
            color_discrete_sequence=cores if cores else px.colors.qualitative.Plotly,
            title=title
        )
        fig1.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            showlegend=show_legend,
            width=2000,
            height=500
        )
        fig1.update_xaxes(type='category')
        return fig1

# Função para plotar gráficos de barras empilhadas
def plotar_bempilhada(df, tipo='barra', x_col='Ano', y_col='Valor', color_col=None, title=None, show_legend=False, cores=None):
    if tipo == 'barra_empilhada':
        fig2 = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            barmode='stack',
            color_discrete_sequence=cores if cores else px.colors.qualitative.Plotly,
            title=title
        )
        fig2.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            showlegend=show_legend,
            width=2000,
            height=500
        )
        fig2.update_xaxes(type='category')
        return fig2

# Carregar e transformar dados
df4 = carregar_dados()
df4_melted = transformar_dados(df4)

# Definir lista de indicadores permitidos
indicadores_desejados = [
    'Algumas doenças infecciosas e parasitárias',
    'Neoplasmas (Tumores)',
    'Doenças do sangue e dos órgãos hematopoéticos e alguns transtornos imunitários',
    'Doenças endócrinas, nutricionais e metabólicas',
    'Transtornos mentais e comportamentais',
    'Doenças do sistema nervoso',
    'Doenças do olho e anexos',
    'Doenças do ouvido e da apófise mastoide',
    'Doenças do aparelho circulatório',
    'Doenças do aparelho respiratório',
    'Doenças do aparelho digestivo',
    'Doenças da pele e do tecido subcutâneo',
    'Doenças do sistema osteomuscular e do tecido conjuntivo',
    'Doenças do aparelho geniturinário',
    'Gravidez, parto e puerpério',
    'Algumas afecções originadas no período perinatal',
    'Malformações congênitas, deformidades e anomalias cromossômicas',
    'Sintomas, sinais e achados anormais em exames clínicos e de laboratório, não classificados em outra parte',
    'Lesões, envenenamentos e algumas outras consequências de causas externas',
    'Causas externas de morbidade e mortalidade',
    'Fatores que influenciam o estado de saúde e o contato com serviços de saúde'
]

# Filtrar DataFrame para incluir apenas os indicadores desejados
df3_melted = df4_melted[df4_melted['Indicador'].isin(indicadores_desejados)]


cores_personalizadas = [
    '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3',
    '#FF6692', '#B6E880', '#FF97FF', '#FECB52', '#1F77B4', '#FF7F0E',
    '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F',
    '#BCBD22', '#17BECF'
]

# Filtros para Indicador e Anos
indicadores_unicos = df3_melted['Indicador'].unique()
anos_unicos = sorted(df3_melted['Ano'].unique())

visualizacao = st.sidebar.radio("Selecione o tipo de visualização:", ["Óbitos por Causa", "Óbitos por Sexo"])

if visualizacao == "Óbitos por Causa":

    st.write(""" # Causas de Óbitos por Doenças no Município de Araranguá """)
    st.write(""" Este painel apresenta dados históricos sobre as principais doenças que causaram óbitos entre os cidadãos do município de Araranguá, em Santa Catarina. Analisar as causas e taxa de mortalidade de uma população é um indicador essencial para avaliar a saúde da população e direcionar políticas públicas de prevenção, diagnóstico e tratamento das doenças que mais afetam a populção geral.
   
    """)

    # Controle de filtros usando session_state
    if "indicadores_selecionados_causa" not in st.session_state:
        st.session_state.indicadores_selecionados_causa = indicadores_unicos
    if "anos_selecionados_causa" not in st.session_state:
        st.session_state.anos_selecionados_causa = (min(anos_unicos), max(anos_unicos))


    indicadores_selecionados = st.multiselect(
        "Selecione os indicadores para Óbitos por Causa:", 
        indicadores_unicos, 
        default=st.session_state.indicadores_selecionados_causa
    )
    anos_selecionados = st.slider(
        "Selecione o intervalo de anos para Óbitos por Causa:",
        min_value=min(anos_unicos),
        max_value=max(anos_unicos),
        value=st.session_state.anos_selecionados_causa,
        step=1
    )

    st.session_state.indicadores_selecionados_causa = indicadores_selecionados
    st.session_state.anos_selecionados_causa = anos_selecionados

    df_filtrado_causa = df3_melted[(
        df3_melted['Indicador'].isin(indicadores_selecionados)) & 
        (df3_melted['Ano'].between(anos_selecionados[0], anos_selecionados[1])) & 
        (df3_melted['Etiqueta'] == 'Total')
    ] 

    st.subheader("Evolução dos Casos de Óbito por Causa")
    if not df_filtrado_causa.empty:
        fig_causa = plotar_bagrupada(df_filtrado_causa, tipo='barra_agrupada', color_col='Indicador', title="Óbitos por Causa", show_legend=False, cores=cores_personalizadas)
        st.plotly_chart(fig_causa, use_container_width=True)
    else:
        st.write("Nenhum dado disponível para os filtros selecionados.")

elif visualizacao == "Óbitos por Sexo":

    st.write(""" # Principais Causas de Óbitos por Doenças em Pessoas do Sexo Masculino e Feminino""")
    st.write("""
    Este painel apresenta dados históricos sobre as principais doenças que causaram óbitos entre pessoas do sexo masculino e feminino no município de Araranguá, Santa Catarina. Analisar a causa da mortalidade entre os sexos é um indicador essencial para orientar políticas de saúde pública e alocação de recursos para prevenção, diagnóstico e tratamento das condições específicas de determinados grupos populacionais em maior risco.
    """)

    #Masculino
    #Controle de filtros
    if "indicadores_selecionados_masculino" not in st.session_state:
        st.session_state.indicadores_selecionados_masculino = indicadores_unicos
    if "anos_selecionados_masculino" not in st.session_state:
        st.session_state.anos_selecionados_masculino = (min(anos_unicos), max(anos_unicos))

    if "indicadores_selecionados_feminino" not in st.session_state:
        st.session_state.indicadores_selecionados_feminino = indicadores_unicos
    if "anos_selecionados_feminino" not in st.session_state:
        st.session_state.anos_selecionados_feminino = (min(anos_unicos), max(anos_unicos))

    indicadores_masculino = st.multiselect(
        "Selecione as causas (Masculino):", 
        indicadores_unicos, 
        default=st.session_state.indicadores_selecionados_masculino
    )
    anos_masculino = st.slider(
        "Selecione o intervalo de anos (Masculino):",
        min_value=min(anos_unicos),
        max_value=max(anos_unicos),
        value=st.session_state.anos_selecionados_masculino,
        step=1
    )

    #Salvar status dos filtros
    st.session_state.indicadores_selecionados_masculino = indicadores_masculino
    st.session_state.anos_selecionados_masculino = anos_masculino

    df_filtrado_sexo_masculino = df3_melted[(
        df3_melted['Indicador'].isin(indicadores_masculino)) & 
        (df3_melted['Ano'].between(anos_masculino[0], anos_masculino[1])) & 
        (df3_melted['Etiqueta'] == 'Masculino')
    ] 

    df_sexo_agrupado_masculino = df_filtrado_sexo_masculino.groupby(['Indicador', 'Ano', 'Etiqueta']).sum().reset_index()

    st.subheader("Causa dos Óbitos Masculinos ao Longo dos Anos")
    fig_masculino = plotar_bempilhada(
        df_sexo_agrupado_masculino,
        tipo='barra_empilhada',
        color_col='Indicador',
        title=None,
        show_legend=False,
        cores=cores_personalizadas
    )
    fig_masculino.update_layout(
        yaxis_range=[0, df_sexo_agrupado_masculino['Valor'].max() * 1.1]
    )
    st.plotly_chart(fig_masculino, use_container_width=True)

    # Feminino
    indicadores_feminino = st.multiselect(
        "Selecione as causas (Femino):", 
        indicadores_unicos, 
        default=st.session_state.indicadores_selecionados_feminino
    )
    anos_feminino = st.slider(
        "Selecione o intervalo de anos (Femino):",
        min_value=min(anos_unicos),
        max_value=max(anos_unicos),
        value=st.session_state.anos_selecionados_feminino,
        step=1
    )

    # Salvar status dos filtros
    st.session_state.indicadores_selecionados_feminino = indicadores_feminino
    st.session_state.anos_selecionados_feminino = anos_feminino

    df_filtrado_sexo_feminino = df3_melted[(
        df3_melted['Indicador'].isin(indicadores_feminino)) & 
        (df3_melted['Ano'].between(anos_feminino[0], anos_feminino[1])) & 
        (df3_melted['Etiqueta'] == 'Feminino')
    ] 

    df_sexo_agrupado_feminino = df_filtrado_sexo_feminino.groupby(['Indicador', 'Ano', 'Etiqueta']).sum().reset_index()

    st.subheader("Causa dos Óbitos Femininos ao Longo dos Anos")
    fig_feminino = plotar_bempilhada(
        df_sexo_agrupado_feminino,
        tipo='barra_empilhada',
        color_col='Indicador',
        title=None,
        show_legend=False,
        cores=cores_personalizadas
    )
    fig_feminino.update_layout(
        yaxis_range=[0, df_sexo_agrupado_feminino['Valor'].max() * 1.1]
    )
    st.plotly_chart(fig_feminino, use_container_width=True)


