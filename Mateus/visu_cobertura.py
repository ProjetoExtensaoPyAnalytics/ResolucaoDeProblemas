import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Dicionário com informações das vacinas
VACINAS_INFO = {
    'BCG': {
        'nome_completo': 'BCG',
        'dose': 'Dose única',
        'doencas': 'Formas graves da tuberculose (miliar e meníngea)'
    },
    'dTpa Adulto': {
        'nome_completo': 'Difteria, Tétano, Pertussis (dTpa - acelular)',
        'dose': 'Uma dose - Reforço a cada 10 anos ou 5 anos em caso de ferimentos graves',
        'doencas': 'Difteria, Tétano e Coqueluche'
    },
    'DTP': {
        'nome_completo': 'Adsorvida Difteria, Tétano e pertussis (DTP)',
        'dose': '3 doses (2, 4 e 6 meses)',
        'doencas': 'Difteria, tétano e coqueluche'
    },
    'DTP REF (4 e 6 anos)': {
        'nome_completo': 'Adsorvida Difteria, Tétano e pertussis (DTP)',
        'dose': 'Reforço aos 4 anos',
        'doencas': 'Difteria, tétano e coqueluche'
    },
    'DTP (1º Reforço)': {
        'nome_completo': 'Adsorvida Difteria, Tétano e pertussis (DTP)',
        'dose': 'Primeiro reforço aos 15 meses',
        'doencas': 'Difteria, tétano e coqueluche'
    },
    'Hepatite B': {
        'nome_completo': 'Hepatite B (recombinante)',
        'dose': 'Dose única ao nascer',
        'doencas': 'Hepatite B'
    },
    'Hepatite B (< 30 Dias)': {
        'nome_completo': 'Hepatite B (recombinante)',
        'dose': 'Dose inicial até 30 dias de vida',
        'doencas': 'Hepatite B'
    },
    'Penta (DTP/Hep B/Hib)': {
        'nome_completo': 'Adsorvida Difteria, Tétano, pertussis, Hepatite B (recombinante) e Haemophilus influenzae B (conjugada)',
        'dose': '3 doses (2, 4 e 6 meses)',
        'doencas': 'Difteria, Tétano, Coqueluche, Hepatite B e infecções causadas pelo Haemophilus influenzae B'
    },
    'Polio Injetável (VIP)': {
        'nome_completo': 'Poliomielite 1, 2 e 3 (inativada) - (VIP)',
        'dose': '3 doses (2, 4 e 6 meses)',
        'doencas': 'Poliomielite'
    },
    'Polio 4 anos': {
        'nome_completo': 'Poliomielite 1 e 3 (atenuada) - (VOPb)',
        'dose': 'Reforço aos 4 anos',
        'doencas': 'Poliomielite'
    },
    'Polio Oral Bivalente': {
        'nome_completo': 'Poliomielite 1 e 3 (atenuada) - (VOPb)',
        'dose': '1º reforço aos 15 meses',
        'doencas': 'Poliomielite'
    },
    'Pneumo 10': {
        'nome_completo': 'Pneumocócica 10-valente (Conjugada)',
        'dose': '2 doses (2 e 4 meses)',
        'doencas': 'Infecções invasivas (como meningite e pneumonia) e otite média aguda, causadas pelos 10 sorotipos de Streptococus pneumoniae'
    },
    'Pneumo 10 (1ª Reforço)': {
        'nome_completo': 'Pneumocócica 10-valente (Conjugada)',
        'dose': 'Reforço aos 12 meses',
        'doencas': 'Infecções invasivas (como meningite e pneumonia) e otite média aguda, causadas pelos 10 sorotipos de Streptococus pneumoniae'
    },
    'Rotavirus': {
        'nome_completo': 'Rotavírus humano G1P1 [8] (atenuada)',
        'dose': '2 doses (2 e 4 meses)',
        'doencas': 'Diarreia por rotavírus (Gastroenterites)'
    },
    'Meningo C': {
        'nome_completo': 'Meningocócica C (conjugada)',
        'dose': '2 doses (3 e 5 meses)',
        'doencas': 'Doença invasiva causada pela Neisseria meningitidis do sorogrupo C'
    },
    'Meningo C (1ª Reforço)': {
        'nome_completo': 'Meningocócica C (conjugada)',
        'dose': 'Reforço aos 12 meses',
        'doencas': 'Doença invasiva causada pela Neisseria meningitidis do sorogrupo C'
    },
    'Febre Amarela': {
        'nome_completo': 'Febre amarela (atenuada)',
        'dose': '1 dose aos 9 meses + 1 reforço aos 4 anos. Dose única caso não tenha recebido nenhuma dose até os 5 anos',
        'doencas': 'Febre amarela'
    },
    'Hepatite A': {
        'nome_completo': 'Adsorvida hepatite A (inativada)',
        'dose': '1 dose aos 15 meses',
        'doencas': 'Hepatite A'
    },
    'Tríplice Viral - 1ª Dose': {
        'nome_completo': 'Sarampo, caxumba, rubéola (Tríplice viral)',
        'dose': '1ª dose aos 12 meses',
        'doencas': 'Sarampo, caxumba e rubéola'
    },
    'Tríplice Viral - 2ª Dose': {
        'nome_completo': 'Sarampo, caxumba, rubéola (Tríplice viral)',
        'dose': '2ª dose aos 15 meses',
        'doencas': 'Sarampo, caxumba e rubéola'
    },
    'Tetra Viral (SRC+VZ)': {
        'nome_completo': 'Tetraviral',
        'dose': '1 dose aos 15 meses',
        'doencas': 'Sarampo, caxumba, rubéola e varicela'
    },
    'Varicela': {
        'nome_completo': 'Varicela (monovalente)',
        'dose': '1 dose aos 4 anos',
        'doencas': 'Varicela'
    },
    'Sarampo': {
        'nome_completo': 'Sarampo (monovalente)',
        'dose': '1 dose aos 12 meses',
        'doencas': 'Sarampo'
    }
}

# Leitura do arquivo CSV
cobertura_ararangua = pd.read_csv('cobertura_vacinal_ararangua_atualizado.csv', index_col=0)

# Converter índice para numérico
cobertura_ararangua.index = pd.to_numeric(cobertura_ararangua.index)

# Filtrar apenas os anos de 2014 até 2024
cobertura_ararangua = cobertura_ararangua[cobertura_ararangua.index >= 2014]

# Remover as colunas da Tetravalente e Sarampo
colunas_para_remover = ['Tetravalente (DTP/Hib)', 'Sarampo']
for coluna in colunas_para_remover:
    if coluna in cobertura_ararangua.columns:
        cobertura_ararangua = cobertura_ararangua.drop(coluna, axis=1)

# Título principal e introdução
st.write(""" # Cobertura vacinal em Araranguá """)
st.write("""
Este painel apresenta dados históricos sobre a cobertura vacinal no município de Araranguá, Santa Catarina. A cobertura vacinal é um indicador que mede a porcentagem da população-alvo que recebeu as vacinas recomendadas no Programa Nacional de Imunizações (PNI).
Essa informação é importante pois permite avaliar a efetividade das campanhas de vacinação e identificar onde a imunização pode ser aprimorada, auxiliando na tomada de decisões estratégicas para melhorar a proteção da população contra doenças evitáveis. 
""")

# Barra lateral para selecionar a visualização
st.sidebar.title("Cobertura Vacinal")
visualization = st.sidebar.radio(
    "Escolha a visualização:",
    ["Análise Temporal", "Análise por ano"]
)

# Seção de Evolução Temporal
if visualization == "Análise Temporal":
    st.write("""
    ## Análise Temporal da Cobertura Vacinal
    
    Este gráfico permite acompanhar a evolução da cobertura vacinal ao longo dos anos. 
    Você pode selecionar múltiplas vacinas para comparação e ajustar o período de análise 
    usando os controles abaixo. A linha tracejada vermelha indica a meta de 95% de cobertura.
    """)
    
    # Inicializar o intervalo de anos no session_state, se não estiver presente
    if 'intervalo_anos' not in st.session_state:
        st.session_state['intervalo_anos'] = (2014, 2024)

    def atualizar_intervalo():
        st.session_state['intervalo_anos'] = st.session_state['novo_intervalo']
    
    # Controles para o gráfico de linha
    vacina_selecionada = st.multiselect(
        "Escolha as vacinas",
        options=cobertura_ararangua.columns,
        default=['BCG']
    )
    
    # Usar o intervalo atual do session_state para filtrar
    df_filtrado = cobertura_ararangua.loc[
        st.session_state['intervalo_anos'][0]:st.session_state['intervalo_anos'][1], 
        vacina_selecionada
    ]
    
    # Criar gráfico de linha com Plotly
    if len(vacina_selecionada) > 0:
        fig = px.line(
            df_filtrado,
            x=df_filtrado.index,
            y=vacina_selecionada,
            title='Cobertura ao longo do tempo',
            labels={'value': 'Cobertura (%)', 'variable': 'Vacina', 'index': 'Ano'},
            line_shape='linear'
        )

        # Adicionar a linha de meta de cobertura (95%)
        fig.add_trace(
            go.Scatter(
                x=df_filtrado.index,
                y=[95] * len(df_filtrado.index),
                mode='lines',
                line=dict(dash='dash', color='red'),
                name='Meta de cobertura (95%)'
            )
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            legend_title_text='Vacina',
            yaxis_title="Cobertura (%)",
            xaxis_title="Ano"
        )

        # Exibir o gráfico
        st.plotly_chart(fig)

        # Slider para seleção do intervalo de anos abaixo do gráfico
        st.slider(
            "Escolha o intervalo de anos:",
            min_value=int(2014),
            max_value=int(cobertura_ararangua.index.max()),
            value=st.session_state['intervalo_anos'],
            key='novo_intervalo',
            on_change=atualizar_intervalo,
            format="%i"
        )
        
        # Informações das vacinas selecionadas
        st.write("## Informações sobre as vacinas selecionadas:")

        if 'Febre Amarela' in vacina_selecionada:
            st.info("""
                    **Nota sobre a Febre Amarela:** Os valores muito baixos (próximos a 0%) antes de 2018 provavelmente se devem a diferenças na metodologia de registro dos dados. 
                    """)
        if 'Tetra Viral (SRC+VZ)' in vacina_selecionada:
            st.info("""
                    **Nota sobre a Tetra Viral:** A vacina apresenta uma queda significativa a partir de 2021 (21.91%) e foi descontinuada após 2022, sendo substituída pelo uso da Tríplice Viral (sarampo, caxumba e rubéola) em conjunto com a Varicela aplicada separadamente.
                    """)
        
        for vacina in vacina_selecionada:
            if vacina in VACINAS_INFO:
                info = VACINAS_INFO[vacina]
                with st.expander(f"{vacina} ", expanded=True):
                    st.markdown(f"""
                    **Doenças prevenidas:** {info['doencas']}  
                    **Esquema de doses:** {info['dose']}  
                    """)
            else:
                st.write("Por favor, selecione pelo menos uma vacina para visualizar os dados.")

# Seção do Panorama Anual
elif visualization == "Análise por ano":
    st.write("""
    ## Análise por ano da Cobertura Vacinal
    
    Esta visualização apresenta um comparativo da cobertura de todas as vacinas para o ano selecionado. 
    As vacinas são ordenadas da maior para a menor cobertura, permitindo identificar rapidamente 
    quais imunizantes atingiram as metas estabelecidas e quais precisam de atenção especial. 
    """)

# Continuação do código anterior...
    
    # Seletor de ano para o mapa de calor
    ano_heatmap = st.selectbox(
        "Selecione o ano para visualizar o panorama anual",
        options=sorted(cobertura_ararangua.index.unique(), reverse=True),
        index=0
    )

    # Pegar dados do ano selecionado, remover NaN e ordenar por cobertura
    dados_ano = cobertura_ararangua.loc[ano_heatmap].dropna()
    dados_ordenados = dados_ano.sort_values(ascending=False)

    # Criar gráfico de barras horizontais
    fig = go.Figure()

    # Função para determinar a cor baseada no valor da cobertura
    def get_color(value):
        if value >= 95:  # Meta de cobertura
            return '#20B2AA'  # Verde água
        elif value > 70:
            return '#FFD700'  # Amarelo
        elif value > 40:
            return '#FFA500'  # Laranja
        else:
            return '#FF0000'  # Vermelho

    # Criar lista de cores baseada nos valores
    colors = [get_color(value) for value in dados_ordenados.values]

    # Adicionar barras
    fig.add_trace(go.Bar(
        x=dados_ordenados.values,
        y=dados_ordenados.index,
        orientation='h',
        marker=dict(
            color=colors,
            showscale=False
        ),
        text=[f'{value:.1f}%' for value in dados_ordenados.values],
        textposition='auto',
        showlegend=False,
        hovertemplate='<b>%{y}</b><br>' +
                      'Cobertura: %{x:.1f}%<extra></extra>'
    ))

    # Adicionar linhas de referência
    fig.add_shape(
        type="line",
        x0=40, x1=40,
        y0=-1, y1=len(dados_ordenados),
        line=dict(color="gray", width=1, dash="dash"),
    )

    fig.add_shape(
        type="line",
        x0=70, x1=70,
        y0=-1, y1=len(dados_ordenados),
        line=dict(color="gray", width=1, dash="dash"),
    )

    fig.add_shape(
        type="line",
        x0=95, x1=95,
        y0=-1, y1=len(dados_ordenados),
        line=dict(color="gray", width=1, dash="dash"),
    )

    # Atualizar layout
    fig.update_layout(
        title=f'Cobertura Vacinal em {ano_heatmap}',
        xaxis_title="Cobertura (%)",
        yaxis_title="Vacina",
        height=max(400, len(dados_ordenados) * 40),
        yaxis=dict(
            autorange="reversed"
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=False,
            range=[0, max(100, dados_ordenados.max() + 5)]
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        margin=dict(l=10, r=10, t=30, b=10)
    )

    # Adicionar legenda personalizada
    legenda = [
        dict(name="0-40%", color="#FF0000"),
        dict(name="41-70%", color="#FFA500"),
        dict(name=">70%", color="#FFD700"),
        dict(name="Meta de Cobertura ≥95%", color="#20B2AA")
    ]

    for i, item in enumerate(legenda):
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, color=item['color']),
            showlegend=True,
            name=item['name']
        ))

    # Mostrar o gráfico
    st.plotly_chart(fig, use_container_width=True)

    # Adicionar nota explicativa
    st.write("""
    **Categorias de cobertura:**
    - 🔴 0-40%: Cobertura crítica
    - 🟠 41-70%: Cobertura insuficiente
    - 🟡 >70%: Cobertura moderada
    - 🟢 ≥95%: Meta de cobertura atingida
    """)

# Fonte dos dados (fora dos blocos condicionais)
st.write("""
**Fonte dos dados:** 
- [DATASUS - Imunizações desde 1994](https://datasus.saude.gov.br/acesso-a-informacao/imunizacoes-desde-1994/)
- [Painel de Monitoramento de Coberturas Vacinais - Ministério da Saúde](https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html)
""")
