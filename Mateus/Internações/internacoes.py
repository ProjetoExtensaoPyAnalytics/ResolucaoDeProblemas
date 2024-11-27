import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
#st.set_page_config(page_title="Análise de Doenças - Araranguá", layout="wide")

# Função para identificar o nível da categoria
def get_category_level(name):
    if name.startswith('..') and not name.startswith('....'):
        return 'subcategory'
    elif not name.startswith('..'):
        return 'main_category'
    return 'subsubcategory'

# Função para obter a categoria principal
def get_parent_categories(df):
    current_main = None
    categories = []
    
    for name in df['Lista Morb  CID-10']:
        if get_category_level(name) == 'main_category':
            current_main = name
        categories.append(current_main)
    
    return categories

# Função para converter valores para numérico
def convert_to_numeric(val):
    if isinstance(val, str):
        val = val.replace(',', '.').replace('-', '0')
        try:
            return float(val)
        except ValueError:
            return val
    return val

# Função para limpar nome das doenças
def clean_disease_name(name):
    return name.replace('..', '').strip()

# Função para obter as top 5 doenças por ano
def get_top_5_diseases_by_year(df):
    anos = [col for col in df.columns if col.isdigit()]
    result = []
    
    for ano in anos:
        top_5 = df[['Capítulo CID-10', ano]].sort_values(ano, ascending=False).head(5)
        for _, row in top_5.iterrows():
            result.append({
                'Ano': ano,
                'Doença': row['Capítulo CID-10'],
                'Internações': row[ano]
            })
    
    return pd.DataFrame(result)

# Leitura dos arquivos
df_cid10 = pd.read_csv('ararangua-cid10.csv', encoding='cp1252', sep=';', skiprows=4)
df_lista10 = pd.read_csv('ararangua-lista10.csv', encoding='cp1252', sep=';', skiprows=4)

# Processamento dos dataframes
df_cid10 = df_cid10.iloc[:-4, :-1]  # Remove as últimas 4 linhas e a última coluna
df_lista10 = df_lista10.iloc[:-4:, :-1]  # Remove a coluna Total

# Dicionário de substituições
rename_chapters = {
    'III. Doenças sangue órgãos hemat e transt imunitár': 'III. Doenças do sangue, órgãos hematopoéticos e transtornos imunitários',
    'IV. Doenças endócrinas nutricionais e metabólicas': 'IV. Doenças endócrinas, nutricionais e metabólicas',
    'XIII.Doenças sist osteomuscular e tec conjuntivo': 'XIII. Doenças do sistema osteomuscular e tecido conjuntivo',
    'XVI. Algumas afec originadas no período perinatal': 'XVI. Algumas afecções originadas no período perinatal',
    'XVII.Malf cong deformid e anomalias cromossômicas': 'XVII. Malformações congênitas, deformidades e anomalias cromossômicas',
    'XVIII.Sint sinais e achad anorm ex clín e laborat': 'XVIII. Sintomas, sinais e achados anormais em exames clínicos e laboratoriais',
    'XIX. Lesões enven e alg out conseq causas externas': 'XIX. Lesões, envenenamentos e algumas outras consequências de causas externas'
}

# Aplicar o rename na coluna específica
df_cid10['Capítulo CID-10'] = df_cid10['Capítulo CID-10'].replace(rename_chapters)

# Dicionário de substituições para df_lista10
rename_chapters_lista = {
    '01 Algumas doenças infecciosas e parasitárias': 'I. Algumas doenças infecciosas e parasitárias',
    '02 Neoplasias (tumores)': 'II. Neoplasias (tumores)',
    '03 Doenças sangue órgãos hemat e transt imunitár': 'III. Doenças do sangue, órgãos hematopoéticos e transtornos imunitários',
    '04 Doenças endócrinas nutricionais e metabólicas': 'IV. Doenças endócrinas, nutricionais e metabólicas',
    '05 Transtornos mentais e comportamentais': 'V. Transtornos mentais e comportamentais',
    '06 Doenças do sistema nervoso': 'VI. Doenças do sistema nervoso',
    '07 Doenças do olho e anexos': 'VII. Doenças do olho e anexos',
    '08 Doenças do ouvido e da apófise mastóide': 'VIII. Doenças do ouvido e da apófise mastóide',
    '09 Doenças do aparelho circulatório': 'IX. Doenças do aparelho circulatório',
    '10 Doenças do aparelho respiratório': 'X. Doenças do aparelho respiratório',
    '11 Doenças do aparelho digestivo': 'XI. Doenças do aparelho digestivo',
    '12 Doenças da pele e do tecido subcutâneo': 'XII. Doenças da pele e do tecido subcutâneo',
    '13 Doenças sist osteomuscular e tec conjuntivo': 'XIII. Doenças do sistema osteomuscular e tecido conjuntivo',
    '14 Doenças do aparelho geniturinário': 'XIV. Doenças do aparelho geniturinário',
    '15 Gravidez parto e puerpério': 'XV. Gravidez, parto e puerpério',
    '16 Algumas afec originadas no período perinatal': 'XVI. Algumas afecções originadas no período perinatal',
    '17 Malf cong deformid e anomalias cromossômicas': 'XVII. Malformações congênitas, deformidades e anomalias cromossômicas',
    '18 Sint sinais e achad anorm ex clín e laborat': 'XVIII. Sintomas, sinais e achados anormais em exames clínicos e laboratoriais',
    '19 Lesões enven e alg out conseq causas externas': 'XIX. Lesões, envenenamentos e algumas outras consequências de causas externas',
    '20 Causas externas de morbidade e mortalidade': 'XX. Causas externas de morbidade e mortalidade',
    '21 Contatos com serviços de saúde': 'XXI. Contatos com serviços de saúde'
}

# Aplicar o rename no df_lista10
df_lista10['Lista Morb  CID-10'] = df_lista10['Lista Morb  CID-10'].replace(rename_chapters_lista)

# Adiciona categorização ao df_lista10
df_lista10['main_category'] = get_parent_categories(df_lista10)
df_lista10['category_level'] = df_lista10['Lista Morb  CID-10'].apply(get_category_level)

# Converte colunas numéricas do df_lista10
for col in df_lista10.columns:
    if col not in ['Lista Morb  CID-10', 'main_category', 'category_level']:
        df_lista10[col] = df_lista10[col].apply(convert_to_numeric)

# Converte colunas numéricas do df_cid10
for col in df_cid10.columns[1:]:
    df_cid10[col] = df_cid10[col].apply(convert_to_numeric)

# Título principal
#st.title("Internações em Araranguá")
st.write(""" # Internações Hospitalares em Araranguá """)
st.write("""
Este painel apresenta dados históricos sobre internações hospitalares no município de Araranguá, Santa Catarina. 
Os dados estão organizados conforme a Classificação 
Internacional de Doenças (CID-10), que é o padrão internacional para classificação de doenças e problemas relacionados à saúde.

O CID-10 organiza as condições de saúde em capítulos temáticos - por exemplo, doenças do sistema circulatório, respiratório, 
lesões e causas externas, gravidez e parto, entre outros. 
Esses dados são fundamentais para identificar as principais demandas de saúde da população e auxiliar gestores no planejamento de recursos e ações preventivas.
""")

# Sidebar para seleção da visualização
st.sidebar.title("Internações")
visualization = st.sidebar.radio(
    "Escolha a visualização:",
    ["Ao longo do tempo", 
     "Por ano", 
     "Por capítulo CID ao longo do tempo",
     "Por capítulo CID por ano",
     "Principais causas de internação por ano"]
)

if visualization == "Ao longo do tempo":
    st.write("""
    ## Internações ao longo do tempo

    Esta visualização permite acompanhar as tendências das internações ao longo dos anos.
    Você pode selecionar múltiplas causas para comparação e ajustar o período de análise usando os controles abaixo.
    Por padrão, são exibidas as cinco causas com maior número total de internações no período.
    """)
    
    anos = [col for col in df_cid10.columns if col.isdigit()]
    ano_inicio, ano_fim = st.slider('Selecione o período:', 
                                   min_value=int(anos[0]), 
                                   max_value=int(anos[-1]), 
                                   value=(int(anos[0]), int(anos[-1])))
    
    # Calcular total de internações por causa
    df_cid10['total_internacoes'] = df_cid10[anos].sum(axis=1)
    
    # Pegar as 5 causas com mais internações
    top_5_causes = df_cid10.nlargest(5, 'total_internacoes')['Capítulo CID-10'].tolist()
    
    causas = st.multiselect(
        'Selecione as causas de internação:', 
        options=df_cid10['Capítulo CID-10'].tolist(),
        default=top_5_causes
    )
    
    anos_selecionados = [str(ano) for ano in range(ano_inicio, ano_fim + 1)]
    df_plot = df_cid10[df_cid10['Capítulo CID-10'].isin(causas)].melt(
        id_vars=['Capítulo CID-10'],
        value_vars=anos_selecionados,
        var_name='Ano',
        value_name='Internações'
    )
    
    fig = px.line(df_plot, 
              x='Ano', 
              y='Internações', 
              color='Capítulo CID-10',
              markers=True)

    fig.update_layout(
    height=600,
    legend=dict(
        orientation="h",  # Legenda horizontal
        yanchor="bottom",
        y=1.1,  # Posiciona a legenda um pouco acima do gráfico
        xanchor="center",
        x=0.5
    )
)
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
# Visualização 2: Por ano
elif visualization == "Por ano":
    st.write("""
    ## Internações por Ano

    Esta visualização apresenta a distribuição completa das internações para o ano selecionado.
    As causas são ordenadas pelo número de internações, permitindo identificar rapidamente
    as principais demandas de internação hospitalar no período escolhido.
    """)
    
    anos = [col for col in df_cid10.columns if col.isdigit()]
    ano_selecionado = st.selectbox('Selecione o ano:', 
                                  anos,
                                  index=len(anos)-1)
    
    df_barras = pd.DataFrame({
        'Doença': df_cid10['Capítulo CID-10'],
        'Internações': df_cid10[ano_selecionado]
    }).sort_values('Internações', ascending=True)
    
    fig = px.bar(df_barras, 
                 x='Internações',
                 y='Doença',
                 orientation='h')
    
    fig.update_layout(height=800)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Internações", f"{int(df_barras['Internações'].sum()):,}")

# Visualização 3: Por categoria ao longo do tempo
elif visualization == "Por capítulo CID ao longo do tempo":
    st.write("""
    ## Detalhamento das causas de internação por Capítulo CID-10 ao longo do tempo

    Esta visualização permite analisar em detalhe as causas específicas de internação dentro de cada capítulo do CID-10 ao longo do tempo.

    Selecione um capítulo do CID-10 para visualizar a evolução temporal dos diferentes diagnósticos ao longo dos anos.
    Por padrão, são exibidas as cinco causas com maior número de internações.
    """)
    
    main_categories = df_lista10[df_lista10['category_level'] == 'main_category']['Lista Morb  CID-10'].tolist()
    selected_category = st.selectbox('Selecione o capítulo CID:', main_categories)
    
    # Pegar todas as subcategorias da categoria selecionada
    df_category = df_lista10[
        (df_lista10['main_category'] == selected_category) & 
        (df_lista10['category_level'] == 'subcategory')
    ]
    
    # Calcular o total de internações por subcategoria
    df_category['total_internacoes'] = df_category[[col for col in df_category.columns if col.isdigit()]].sum(axis=1)
    
    # Pegar as 5 subcategorias com mais internações
    top_5_subcategories = df_category.nlargest(5, 'total_internacoes')['Lista Morb  CID-10'].apply(clean_disease_name).tolist()
    
    # Criar multiselect com as top 5 pré-selecionadas
    all_subcategories = df_category['Lista Morb  CID-10'].apply(clean_disease_name).tolist()
    selected_subcategories = st.multiselect(
        'Selecione as causas de internação:',
        options=all_subcategories,
        default=top_5_subcategories
    )
    
    anos = [col for col in df_lista10.columns if col.isdigit()]
    ano_inicio, ano_fim = st.slider('Selecione o período:', 
                                   min_value=int(anos[0]), 
                                   max_value=int(anos[-1]), 
                                   value=(int(anos[0]), int(anos[-1])))
    
    anos_selecionados = [str(ano) for ano in range(ano_inicio, ano_fim + 1)]
    
    # Filtrar apenas as subcategorias selecionadas
    df_category_filtered = df_category[df_category['Lista Morb  CID-10'].apply(clean_disease_name).isin(selected_subcategories)]
    
    df_plot = df_category_filtered.melt(
        id_vars=['Lista Morb  CID-10'],
        value_vars=anos_selecionados,
        var_name='Ano',
        value_name='Internações'
    )
    
    df_plot['Lista Morb  CID-10'] = df_plot['Lista Morb  CID-10'].apply(clean_disease_name)
    
    fig = px.line(df_plot,
                  x='Ano',
                  y='Internações',
                  color='Lista Morb  CID-10',
                  markers=True)
    
    fig.update_layout(
        height=600,
        legend_title="Subcategorias"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Visualização 4: Por categoria por ano
elif visualization == "Por capítulo CID por ano":
    st.write("""
    ## Detalhamento das causas de internação por Capítulo CID-10 - Por Ano

    Esta visualização detalha a distribuição das causas específicas de internação dentro de um capítulo do CID-10 para o ano selecionado.
    Selecione um ano e um capítulo do CID-10 para identificar quais foram os principais motivos de internação naquele período.
    """)
    
    main_categories = df_lista10[df_lista10['category_level'] == 'main_category']['Lista Morb  CID-10'].tolist()
    selected_category = st.selectbox('Selecione o capítulo CID', main_categories)
    
    anos = [col for col in df_lista10.columns if col.isdigit()]
    ano_selecionado = st.selectbox('Selecione o ano:', 
                                  anos,
                                  index=len(anos)-1)
    
    df_category = df_lista10[
        (df_lista10['main_category'] == selected_category) & 
        (df_lista10['category_level'] == 'subcategory')
    ]
    
    df_barras = pd.DataFrame({
        'Doença': df_category['Lista Morb  CID-10'].apply(clean_disease_name),
        'Internações': df_category[ano_selecionado]
    }).sort_values('Internações', ascending=True)
    
    fig = px.bar(df_barras,
                 x='Internações',
                 y='Doença',
                 orientation='h')
    
    fig.update_layout(
        height=max(400, len(df_barras) * 30),
        margin=dict(l=0),
        yaxis_title='',
        yaxis={'tickmode': 'linear'}
    )
    
    fig.update_yaxes(
        tickfont=dict(size=12),
        automargin=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Internações", f"{int(df_barras['Internações'].sum()):,}")
    with col2:
        st.metric("Maior Causa", df_barras.iloc[-1]['Doença'])

# Visualização 5: Top 5 Doenças por Ano
else:
    st.write("""
    ## Principais causas de internação por ano

    Esta visualização compara as cinco principais causas de internação ao longo dos anos selecionados.
    O gráfico permite identificar mudanças nos padrões de internação e tendências temporais das causas mais frequentes.
    """)
    
    anos = [col for col in df_cid10.columns if col.isdigit()]
    ano_inicio, ano_fim = st.slider('Selecione o período:', 
                                   min_value=int(anos[0]), 
                                   max_value=int(anos[-1]), 
                                   value=(int(anos[-1])-4, int(anos[-1])))
    
    anos_selecionados = [str(ano) for ano in range(ano_inicio, ano_fim + 1)]
    df_top5 = get_top_5_diseases_by_year(df_cid10)
    df_top5_filtered = df_top5[df_top5['Ano'].isin(anos_selecionados)]
    
    # Criar gráfico de barras agrupadas
    fig = px.bar(df_top5_filtered,
                 x='Ano',
                 y='Internações',
                 color='Doença',
                 barmode='group',
                 #title='Principais causas de internação por ano'
                 )
    
    fig.update_layout(
        height=600,
        xaxis_title="Ano",
        yaxis_title="Número de Internações",
        legend_title="Capítulos CID ",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.write("""
Fonte dos dados: 
- [Morbidade Hospitalar do SUS](http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/nibr.def)
""")
    
