import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados():
    df4 = pd.read_csv('obitos - completo.csv')  # Dados adicionais para óbitos
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

def plotar_bagrupada(df, tipo='barra', x_col='Ano', y_col='Valor', color_col=None, title=None, show_legend=True, cores=None):
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
            showlegend=True,
            width=2000,
            height=500,
            legend=dict(
            )
        )
        fig1.update_xaxes(type='category')
        return fig1

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

# Mapeando as cores aos indicadores
cor_legend = dict(zip(indicadores_desejados, cores_personalizadas))

# Filtros para Indicador e Anos
indicadores_unicos = df3_melted['Indicador'].unique()
anos_unicos = sorted(df3_melted['Ano'].unique())


faixa_etaria = [
        'Menos de 1 ano de idade',
        '1 a 4 anos de idade', '5 a 9 anos', '10 a 14 anos de idade',
        '15 a 19 anos', '20 a 29 anos de idade', '30 a 39 anos de idade',
        '40 a 49 anos de idade', '50 a 59 anos de idade',
        '60 a 69 anos de idade', '70 a 79 anos de idade',
        '80 anos ou mais de idade', 'Idade ignorada', 'Ignorado'
        ]

df2_melted = df4_melted[df4_melted['Indicador'].isin(faixa_etaria)]

# Filtros para Indicador e Anos
faixa_etaria_unica = df2_melted['Indicador'].unique()
ano_unico = sorted(df2_melted['Ano'].unique())

# Barra lateral para selecionar a visualização
st.sidebar.title("Mortalidade")
visualization = st.sidebar.radio(
    "Escolha a visualização:",
    ["Por causa", "Por causa e sexo", "Por faixa etária", "Por faixa etária e sexo"]
)
if visualization == "Por causa":
    st.write(""" # Principais Causas de Óbitos""")
    st.write("""Este painel apresenta dados históricos sobre as principais doenças que causaram óbitos entre os cidadãos do município de Araranguá, em Santa Catarina. Analisar as causas e taxa de mortalidade de uma população é um indicador essencial para avaliar a saúde da população e direcionar políticas públicas de prevenção, diagnóstico e tratamento das doenças que mais afetam a população geral.""")

    # Controle de filtros usando session_state
    if "indicadores_selecionados_causa" not in st.session_state:
        st.session_state.indicadores_selecionados_causa = indicadores_unicos
    if "anos_selecionados_causa" not in st.session_state:
        
        # Define os últimos 5 anos como padrão, mas permite ao usuário escolher outro intervalo
        anos_mais_recent = sorted(df3_melted['Ano'].unique())[-5:]  # Últimos 5 anos
        st.session_state.anos_selecionados_causa = (min(anos_mais_recent), max(anos_mais_recent))

    indicadores_selecionados = st.multiselect(
        "Selecione os indicadores para Óbitos por Causa:", 
        indicadores_unicos, 
        default=st.session_state.indicadores_selecionados_causa
    )
    
    anos_selecionados = st.slider(
        "Selecione o intervalo de anos para Óbitos por Causa:",
        min_value=min(anos_unicos),
        max_value=max(anos_unicos),
        value=st.session_state.anos_selecionados_causa,  # Padrão: últimos 5 anos
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
        fig_causa = plotar_bagrupada(
            df_filtrado_causa, tipo='barra_agrupada', 
            color_col='Indicador', 
            title=None, 
            show_legend=False, 
            cores=cores_personalizadas
        )
        fig_causa.update_layout(
            yaxis_range=[0, df_filtrado_causa['Valor'].max() * 1.1],
            legend=dict(
                orientation='h',  # Legenda horizontal
                yanchor='bottom',  # Ancorar no fundo da legenda
                y=1.15,  # Ajuste a posição vertical da legenda
                xanchor='center',  # Centraliza a legenda horizontalmente
                x=0.5  # Centraliza a legenda horizontalmente
            ),
                margin=dict(t=50, b=100, r=100),  # Ajuste as margens para dar mais espaço à legenda
                width=2400,  # Aumenta a largura do gráfico
                height=1000   # Aumenta a altura do gráfico
        )        
        
        st.plotly_chart(fig_causa, use_container_width=True)
    else:
        st.write("Nenhum dado disponível para os filtros selecionados.")

elif visualization == "Por causa e sexo":
    st.write(""" # Principais Causas de Óbitos em Pessoas do Sexo Masculino e Feminino""")
    st.write("""
    Este painel apresenta dados históricos sobre as principais doenças que causaram óbitos entre pessoas do sexo masculino e feminino no município de Araranguá, Santa Catarina. Analisar a causa da mortalidade entre os sexos é um indicador essencial para orientar políticas de saúde pública e alocação de recursos para prevenção, diagnóstico e tratamento das condições específicas de determinados grupos populacionais em maior risco.
    """)

    # Masculino
    # Controle de filtros
    if "indicadores_selecionados_masculino" not in st.session_state:
        st.session_state.indicadores_selecionados_masculino = indicadores_unicos
    if "anos_selecionados_masculino" not in st.session_state:
        st.session_state.anos_selecionados_masculino = (min(anos_unicos), max(anos_unicos))

    # Define os últimos 5 anos como padrão, mas permite ao usuário escolher outro intervalo
    anos_mais_recent = sorted(df3_melted['Ano'].unique())[-5:]  # Últimos 5 anos
    st.session_state.anos_selecionados_masculino = (min(anos_mais_recent), max(anos_mais_recent))


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

    # Salvar status dos filtros
    st.session_state.indicadores_selecionados_masculino = indicadores_masculino
    st.session_state.anos_selecionados_masculino = anos_masculino

    df_filtrado_sexo_masculino = df3_melted[(
        df3_melted['Indicador'].isin(indicadores_masculino)) & 
        (df3_melted['Ano'].between(anos_masculino[0], anos_masculino[1])) & 
        (df3_melted['Etiqueta'] == 'Masculino')
    ] 

    df_sexo_agrupado_masculino = df_filtrado_sexo_masculino.groupby(['Indicador', 'Ano', 'Etiqueta']).sum().reset_index()

    st.subheader("Causa dos Óbitos Masculinos ao Longo dos Anos")
    fig_masculino = plotar_bagrupada(
        df_sexo_agrupado_masculino,
        tipo='barra_agrupada',
        color_col='Indicador',
        title=None,
        show_legend=True,  # Mostrar legenda
        cores=cores_personalizadas
    )
    fig_masculino.update_layout(
        yaxis_range=[0, df_sexo_agrupado_masculino['Valor'].max() * 1.1],
        legend=dict(
            orientation='h',  # Legenda horizontal
            yanchor='bottom',  # Ancorar no fundo da legenda
            y=1.15,  # Ajuste a posição vertical da legenda
            xanchor='center',  # Centraliza a legenda horizontalmente
            x=0.5  # Centraliza a legenda horizontalmente
        ),
        margin=dict(t=50, b=100, r=100),  # Ajuste as margens para dar mais espaço à legenda
        width=2400,  # Aumenta a largura do gráfico
        height=1000   # Aumenta a altura do gráfico
    )

    st.plotly_chart(fig_masculino, use_container_width=True)

    # Feminino
    if "indicadores_selecionados_feminino" not in st.session_state:
        st.session_state.indicadores_selecionados_feminino = indicadores_unicos
    if "anos_selecionados_feminino" not in st.session_state:
        st.session_state.anos_selecionados_feminino = (min(anos_unicos), max(anos_unicos))

    # Define os últimos 5 anos como padrão, mas permite ao usuário escolher outro intervalo
    anos_mais_recent = sorted(df3_melted['Ano'].unique())[-5:]  # Últimos 5 anos
    st.session_state.anos_selecionados_feminino = (min(anos_mais_recent), max(anos_mais_recent))

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
    fig_feminino = plotar_bagrupada(
        df_sexo_agrupado_feminino,
        tipo='barra_agrupada',
        color_col='Indicador',
        title=None,
        show_legend=True,  # Mostrar legenda
        cores=cores_personalizadas
    )
    fig_feminino.update_layout(
        yaxis_range=[0, df_sexo_agrupado_feminino['Valor'].max() * 1.1],
        legend=dict(
            orientation='h',  # Legenda horizontal
            yanchor='bottom',  # Ancorar no fundo da legenda
            y=1.15,  # Ajuste a posição vertical da legenda
            xanchor='center',  # Centraliza a legenda horizontalmente
            x=0.5  # Centraliza a legenda horizontalmente
        ),
        margin=dict(t=50, b=100, r=100),  # Ajuste as margens para dar mais espaço à legenda
        width=2400,  # Aumenta a largura do gráfico
        height=1000   # Aumenta a altura do gráfico
    )

    st.plotly_chart(fig_feminino, use_container_width=True)


elif visualization == "Por faixa etária":
    st.write(""" # Quantidade de Óbitos por Faixa Etária""")
    st.write("""Este painel apresenta dados históricos sobre a quantidade de óbitos por faixa etária dos cidadãos do município de Araranguá, em Santa Catarina. Esse tipo de análise permite identificar grupos etários mais vulneráveis e possíveis fatores de risco específicos.""")

    # Controle de filtros usando session_state
    if "indicador_faixa_etaria" not in st.session_state:
        st.session_state.indicador_faixa_etaria = faixa_etaria_unica
    if "anos_faixa_etaria" not in st.session_state:

        # Define os últimos 5 anos como padrão, mas permite ao usuário escolher outro intervalo
        anos_mais_recent = sorted(df2_melted['Ano'].unique())[-5:]  # Últimos 5 anos
        st.session_state.anos_faixa_etaria = (min(anos_mais_recent), max(anos_mais_recent))

    faixa_etaria_selecionada = st.multiselect(
        "Selecione os indicadores para Óbitos por Faixa Etária:", 
        faixa_etaria_unica, 
        default=st.session_state.indicador_faixa_etaria
    )
    
    ano_selecionado = st.slider(
        "Selecione o intervalo de anos para Óbitos por Faixa Etária:",
        min_value=min(ano_unico),
        max_value=max(ano_unico),
        value=st.session_state.anos_faixa_etaria,  # Padrão: últimos 5 anos
        step=1
    )

    st.session_state.indicador_faixa_etaria = faixa_etaria_selecionada
    st.session_state.anos_faixa_etaria = ano_selecionado

    df_faixa_etaria = df2_melted[(
        df2_melted['Indicador'].isin(faixa_etaria_selecionada)) & 
        (df2_melted['Ano'].between(ano_selecionado[0], ano_selecionado[1])) & 
        (df2_melted['Etiqueta'] == 'Total_Grupo de Idade')
    ] 

    st.subheader("Quantidade de Óbito ao Longo dos Anos por Faixa Etária")
    if not df_faixa_etaria.empty:
        fig_faixa = plotar_bagrupada(
            df_faixa_etaria,
            tipo='barra_agrupada',
            color_col='Indicador',
            title=None,
            show_legend=False, 
            cores=cores_personalizadas
        )
        fig_faixa.update_layout(
            yaxis_range=[0, df_faixa_etaria['Valor'].max() * 1.1],
            legend=dict(
                orientation='h',  # Legenda horizontal
                yanchor='bottom',  # Ancorar no fundo da legenda
                y=1.15,  # Ajuste a posição vertical da legenda
                xanchor='center',  # Centraliza a legenda horizontalmente
                x=0.5  # Centraliza a legenda horizontalmente
            ),
                margin=dict(t=50, b=100, r=100),  # Ajuste as margens para dar mais espaço à legenda
                width=2400,  # Aumenta a largura do gráfico
                height=1000   # Aumenta a altura do gráfico
        )
            
        st.plotly_chart(fig_faixa, use_container_width=True)
    else:
        st.write("Nenhum dado disponível para os filtros selecionados.")

elif visualization == "Por faixa etária e sexo":
        st.write(""" # Quantidade de Óbitos por Faixa Etária e Sexo""")
        st.write(
            """Este painel apresenta dados históricos sobre a quantidade de óbitos por faixa etária e sexo dos cidadãos do município de Araranguá, Santa Catarina. Esse tipo de análise permite identificar fatores de risco específicos para cada sexo em diferentes idades.
        """)
        # Controle de filtros
        if "faixa_etaria_selecionada_masculino" not in st.session_state:
            st.session_state.faixa_etaria_selecionada_masculino = faixa_etaria_unica
        if "anos_selecionados_masculino" not in st.session_state:
            st.session_state.anos_selecionados_masculino = (min(ano_unico), max(ano_unico))

        if "faixa_etaria_selecionada_feminino" not in st.session_state:
            st.session_state.faixa_etaria_selecionada_feminino = faixa_etaria_unica
        if "anos_selecionados_feminino" not in st.session_state:
            st.session_state.anos_selecionados_feminino = (min(ano_unico), max(ano_unico))

        faixa_etaria_masculino = st.multiselect(
            "Selecione a faixa etária (Masculino):", 
            faixa_etaria_unica, 
            default=st.session_state.faixa_etaria_selecionada_masculino
        )
        ano_masculino = st.slider(
            "Selecione o intervalo de anos (Masculino):",
            min_value=min(ano_unico),
            max_value=max(ano_unico),
            value=st.session_state.anos_selecionados_masculino,
            step=1
        )

        # Salvar status dos filtros
        st.session_state.faixa_etaria_selecionada_masculino = faixa_etaria_masculino
        st.session_state.anos_selecionados_masculino = ano_masculino

        df_filtrado_sexo_masculino = df2_melted[(
            df2_melted['Indicador'].isin(faixa_etaria_masculino)) & 
            (df2_melted['Ano'].between(ano_masculino[0], ano_masculino[1])) & 
            (df2_melted['Etiqueta'] == 'Masculino_Grupo de Idade')
        ] 

        df_fe_agrupado_masculino = df_filtrado_sexo_masculino.groupby(['Indicador', 'Ano', 'Etiqueta']).sum().reset_index()

        st.subheader("Quantidade de Óbitos Masculinos ao Longo dos Anos por Faixa Etária")
        fig_masc = plotar_bagrupada(
            df_fe_agrupado_masculino,
            tipo='barra_agrupada',
            color_col='Indicador',
            title=None,
            show_legend=True,  # Mostrar legenda
            cores=cores_personalizadas
        )
        fig_masc.update_layout(
            yaxis_range=[0, df_fe_agrupado_masculino['Valor'].max() * 1.1],
            legend=dict(
                orientation='h',  # Legenda horizontal
                yanchor='bottom',  # Ancorar no fundo da legenda
                y=1.15,  # Ajuste a posição vertical da legenda
                xanchor='center',  # Centraliza a legenda horizontalmente
                x=0.5  # Centraliza a legenda horizontalmente
            ),
            margin=dict(t=50, b=100, r=100),  # Ajuste as margens para dar mais espaço à legenda
            width=2400,  # Aumenta a largura do gráfico
            height=1000   # Aumenta a altura do gráfico
        )

        st.plotly_chart(fig_masc, use_container_width=True)

        # Feminino
        faixa_etaria_feminino = st.multiselect(
            "Selecione a faixa etária (Femino):", 
            faixa_etaria_unica, 
            default=st.session_state.faixa_etaria_selecionada_feminino
        )
        ano_feminino = st.slider(
            "Selecione o intervalo de anos (Femino):",
            min_value=min(ano_unico),
            max_value=max(ano_unico),
            value=st.session_state.anos_selecionados_feminino,
            step=1
        )

        # Salvar status dos filtros
        st.session_state.faixa_etaria_selecionada_feminino = faixa_etaria_feminino
        st.session_state.anos_selecionados_feminino = ano_feminino

        df_filtrado_sexo_feminino = df2_melted[(
            df2_melted['Indicador'].isin(faixa_etaria_feminino)) & 
            (df2_melted['Ano'].between(ano_feminino[0], ano_feminino[1])) & 
            (df2_melted['Etiqueta'] == 'Feminino_Grupo de Idade')
        ] 

        df_fe_agrupado_feminino = df_filtrado_sexo_feminino.groupby(['Indicador', 'Ano', 'Etiqueta']).sum().reset_index()

        st.subheader("Quantidade de Óbitos Femininos ao Longo dos Anos por Faixa Etária")
        fig_femin = plotar_bagrupada(
            df_fe_agrupado_feminino,
            tipo='barra_agrupada',
            color_col='Indicador',
            title=None,
            show_legend=True,  # Mostrar legenda
            cores=cores_personalizadas
        )
        fig_femin.update_layout(
            yaxis_range=[0, df_fe_agrupado_feminino['Valor'].max() * 1.1],
            legend=dict(
                orientation='h',  # Legenda horizontal
                yanchor='bottom',  # Ancorar no fundo da legenda
                y=1.15,  # Ajuste a posição vertical da legenda
                xanchor='center',  # Centraliza a legenda horizontalmente
                x=0.5  # Centraliza a legenda horizontalmente
            ),
            margin=dict(t=50, b=100, r=100),  # Ajuste as margens para dar mais espaço à legenda
            width=2400,  # Aumenta a largura do gráfico
            height=1000   # Aumenta a altura do gráfico
        )

        st.plotly_chart(fig_femin, use_container_width=True)

# Fonte dos dados (fora dos blocos condicionais)
st.write("""
**Fonte dos dados:** 
- [IBGE](https://cidades.ibge.gov.br/brasil/sc/ararangua/pesquisa/17/15752)
""")
