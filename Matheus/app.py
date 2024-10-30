import streamlit as st
import plotly.express as px
import pandas as pd

path = "indicadores_saneamento.csv"
data = pd.read_csv(path)
data = data.drop(columns=["grupo", "subgrupo"])

# sidebar
st.sidebar.title("Saneamento em Araranguá")
st.sidebar.markdown(
    "Dados sobre saneamento básico e saúde pública em Araranguá, SC."
)
visualizacao = st.sidebar.radio(
    "Escolha a visualização",
    [
        "Cobertura de Abastecimento de Água",
        "Cobertura de Coleta de Esgoto",
        "Internações",
        "Óbitos",
    ],
)

anos_disponiveis = sorted(data["ano"].unique())
anos_selecionados = (min(anos_disponiveis), max(anos_disponiveis))
water_access = data[
    (data["indicador"] == "População com acesso à água")

]
water_no_access = data[
    (data["indicador"] == "População sem acesso à água")

]

sewage_access = data[
    (data["indicador"] == "População com coleta de esgoto")

]
sewage_no_access = data[
    (data["indicador"] == "População sem coleta de esgoto")

]

sewage_treated = data[
    (data["indicador"] == "Esgoto tratado")
]
sewage_collected = data[
    (data["indicador"] == "Esgoto coletado")
]

school_delay_with_sanitation = data[
    (data["indicador"] == "Atraso escolar dos jovens com saneamento")

]
school_delay_without_sanitation = data[
    (data["indicador"] == "Atraso escolar dos jovens sem saneamento")

]

if visualizacao == "Cobertura de Abastecimento de Água":
    st.title("Cobertura de Abastecimento de Água")
    st.write(
        "Esse painel apresenta a cobertura de abastecimento de água em Araranguá, SC. O acesso à água potável é um direito humano fundamental e um determinante essencial da saúde. A cobertura de abastecimento de água reflete a capacidade de uma comunidade de fornecer água limpa e segura a seus habitantes. Quando as pessoas não têm acesso a água tratada, aumentam os riscos de doenças transmitidas pela água, como diarreia e infecções gastrointestinais, que podem ser fatais, especialmente para crianças e populações vulneráveis. Além disso, a escassez de água pode levar à desidratação, afetando a saúde geral e a capacidade de enfrentar doenças. Melhorar a cobertura de abastecimento de água é, portanto, vital para garantir que todos tenham acesso a condições sanitárias adequadas, prevenindo surtos de doenças e promovendo um ambiente mais saudável. Aumentar a infraestrutura hídrica é uma prioridade para a saúde pública e a prosperidade das comunidades."
    )
    year_range = st.slider("Ano", data["ano"].min(), data["ano"].max(), (data["ano"].min(), data["ano"].max()), 1)
    combined_data_water = pd.concat([water_access, water_no_access])
    combined_data_water = combined_data_water[combined_data_water["ano"].between(year_range[0], year_range[1])]

    fig = px.bar(
        combined_data_water,
        x="ano",
        y="valor",
        color="indicador",
        labels={"ano": "Ano", "valor": "População", "indicador": "Indicador"},
        title="Cobertura de Abastecimento de Água ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="População (em milhares)",
        legend_title="Indicador",
        template="plotly_white",
    )

    fig.update_xaxes(tickmode='linear')
    st.plotly_chart(fig)

elif visualizacao == "Cobertura de Coleta de Esgoto":
    st.title("Cobertura de Coleta de Esgoto")
    st.write(
        "Esse painel apresenta a cobertura de coleta de esgoto em Araranguá, SC. O acesso a um sistema de esgoto eficiente é essencial para a saúde pública e o bem-estar das comunidades. A coleta de esgoto adequada ajuda a prevenir a contaminação do solo e da água, reduzindo a propagação de doenças infecciosas e melhorando a qualidade de vida. Quando o esgoto não é tratado, ele pode poluir o meio ambiente, causando danos à saúde e ao ecossistema. A falta de coleta de esgoto também pode levar a problemas de saneamento, como inundações e mau cheiro, afetando a qualidade de vida das pessoas. Investir em infraestrutura de esgoto é, portanto, uma prioridade para garantir a saúde pública e a sustentabilidade ambiental. A expansão da cobertura de coleta de esgoto é essencial para proteger a saúde das comunidades e promover um ambiente mais limpo e saudável."
    )
    year_range = st.slider("Ano", data["ano"].min(), data["ano"].max(), (data["ano"].min(), data["ano"].max()), 1)
    combined_data_sewage = pd.concat([sewage_access, sewage_no_access])
    combined_data_sewage = combined_data_sewage[combined_data_sewage["ano"].between(year_range[0], year_range[1])]

    fig = px.line(
        combined_data_sewage,
        x="ano",
        y="valor",
        color="indicador",
        labels={"ano": "Ano", "valor": "População", "indicador": "Indicador"},
        markers=True,
        title="Cobertura de Coleta de Esgoto ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="População (em milhares)",
        legend_title="Indicador",
        template="plotly_dark",
    )

    fig.update_xaxes(tickmode='linear')
    st.plotly_chart(fig)


if visualizacao == "Internações":
    st.title("Internações Hospitalares")
    st.write(
        "Esse painel apresenta as internações hospitalares em Araranguá, SC. As internações hospitalares são um indicador importante da saúde da população e refletem a necessidade de cuidados médicos e hospitalares. A análise das internações por faixa etária e por doenças específicas pode fornecer informações valiosas sobre as condições de saúde da população e as necessidades de atendimento médico. Identificar as faixas etárias mais afetadas por internações hospitalares pode ajudar a priorizar esforços em políticas de saúde e a proteger as populações mais vulneráveis. Além disso, a análise das tendências ao longo do tempo pode revelar mudanças na incidência de doenças e a eficácia das intervenções de saúde pública. A redução das internações hospitalares é um objetivo importante para melhorar a saúde da população e reduzir os custos do sistema de saúde."
    )

    age_range = st.slider("Faixa etária", 0, 99, (0, 99), 1)
    year_range = st.slider("Ano", data["ano"].min(), data["ano"].max(), (data["ano"].min(), data["ano"].max()), 1)
    only_respiratory = st.checkbox("Apenas respiratórias")
    absolute = st.checkbox("Valores absolutos (sem classificação)")


    initial_age = age_range[0]
    final_age = age_range[1]

    string_to_search = "Internações por doenças respiratórias" if only_respiratory else "Internações"
    hospitalizations = data[data["indicador"].str.contains(string_to_search)]

    age_ranges = hospitalizations["indicador"].str.extract(r"(\d+) a (\d+) anos")
    hospitalizations["idade_min"] = pd.to_numeric(age_ranges[0], errors='coerce')
    hospitalizations["idade_max"] = pd.to_numeric(age_ranges[1], errors='coerce')

    hospitalizations = hospitalizations.dropna(subset=["idade_min", "idade_max"])
    hospitalizations = hospitalizations[((hospitalizations["idade_min"] >= initial_age) | (hospitalizations["idade_max"] >= initial_age)) & ((hospitalizations["idade_min"] <= final_age) | (hospitalizations["idade_max"] <= final_age))]

    hospitalizations = hospitalizations.groupby(["ano", "idade_min", "idade_max"])["valor"].sum().reset_index()
    hospitalizations["faixa_etaria"] = hospitalizations.apply(lambda row: f"{int(row['idade_min'])} a {int(row['idade_max'])}", axis=1)
    hospitalizations = hospitalizations[(hospitalizations["ano"] >= year_range[0]) & (hospitalizations["ano"] <= year_range[1])]
    if  absolute:
        hospitalizations = hospitalizations.groupby(["ano"])["valor"].sum().reset_index()
        fig = px.line(hospitalizations, x="ano", y="valor", title="Internações hospitalares")
    else:
        fig = px.line(hospitalizations, x="ano", y="valor", color="faixa_etaria", title="Internações hospitalares por faixa etária")
    fig.update_layout(xaxis_title="Ano", yaxis_title="Internações")
    fig.update_traces(mode="lines+markers")
    fig.update_xaxes(tickmode='linear')
    st.plotly_chart(fig)

if visualizacao == "Óbitos":
    st.title("Óbitos")
    st.write(
        "Esse painel apresenta os óbitos em Araranguá, SC. Os óbitos são um indicador crítico da saúde da população e refletem a incidência de doenças e condições de saúde. A análise dos óbitos por causa específica pode fornecer informações valiosas sobre as principais causas de morte e as tendências de saúde da população. Identificar as causas de óbito mais comuns pode ajudar a priorizar esforços em políticas de saúde e a prevenir mortes evitáveis. Além disso, a análise das tendências ao longo do tempo pode revelar mudanças na incidência de doenças e a eficácia das intervenções de saúde pública. A redução dos óbitos é um objetivo importante para melhorar a saúde da população e prevenir mortes prematuras."
    )
    year_range = st.slider("Ano", data["ano"].min(), data["ano"].max(), (data["ano"].min(), data["ano"].max()), 1)
    types = ["Doenças Respiratórias", "Doenças de Veiculação Hídrica", "Todas"]
    cause = st.selectbox("Causa", types)

    deaths = data[data["indicador"].str.contains("Óbitos")]
    deaths["ano"] = deaths["ano"].astype(int)
    deaths = deaths[deaths["ano"].between(year_range[0], year_range[1])]

    if cause == "Doenças Respiratórias":
        deaths = deaths[deaths["indicador"].str.contains("respiratórias")]
    elif cause == "Doenças de Veiculação Hídrica":
        deaths = deaths[deaths["indicador"].str.contains("hídrica")]

    deaths = deaths.groupby(["ano"])["valor"].sum().reset_index()

    fig = px.line(deaths, x="ano", y="valor", title="Óbitos")
    fig.update_layout(xaxis_title="Ano", yaxis_title="Óbitos")
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig)
