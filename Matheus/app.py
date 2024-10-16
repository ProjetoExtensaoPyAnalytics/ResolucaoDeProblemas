import streamlit as st
import plotly.express as px
import pandas as pd

path = "indicadores_saneamento.csv"
data = pd.read_csv(path)
data = data.drop(columns=["grupo", "subgrupo"])

st.sidebar.title("Saneamento em Araranguá")
visualizacao = st.sidebar.radio(
    "Escolha a visualização",
    [
        "Cobertura de Abastecimento de Água",
        "Cobertura de Coleta de Esgoto",
        "Consumo de Água",
        "Impactos Educacionais",
        "Custo do Saneamento",
    ],
)

anos_disponiveis = sorted(data["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos", anos_disponiveis, anos_disponiveis
)

water_access = data[
    (data["indicador"] == "População com acesso à água")
    & (data["ano"].isin(anos_selecionados))
]
water_no_access = data[
    (data["indicador"] == "População sem acesso à água")
    & (data["ano"].isin(anos_selecionados))
]

sewage_access = data[
    (data["indicador"] == "População com coleta de esgoto")
    & (data["ano"].isin(anos_selecionados))
]
sewage_no_access = data[
    (data["indicador"] == "População sem coleta de esgoto")
    & (data["ano"].isin(anos_selecionados))
]

sewage_treated = data[
    (data["indicador"] == "Esgoto tratado") & (data["ano"].isin(anos_selecionados))
]
sewage_collected = data[
    (data["indicador"] == "Esgoto coletado") & (data["ano"].isin(anos_selecionados))
]

school_delay_with_sanitation = data[
    (data["indicador"] == "Atraso escolar dos jovens com saneamento")
    & (data["ano"].isin(anos_selecionados))
]
school_delay_without_sanitation = data[
    (data["indicador"] == "Atraso escolar dos jovens sem saneamento")
    & (data["ano"].isin(anos_selecionados))
]

if visualizacao == "Cobertura de Abastecimento de Água":
    st.title("Cobertura de Abastecimento de Água")
    st.write(
        "Esta visualização mostra a cobertura de abastecimento de água ao longo dos anos, apresentando a população com e sem acesso à água. Compreender esses dados é fundamental para identificar áreas que necessitam de melhorias na infraestrutura hídrica e para garantir que todos tenham acesso a um recurso essencial."
    )
    combined_data_water = pd.concat([water_access, water_no_access])

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

    st.plotly_chart(fig)

elif visualizacao == "Cobertura de Coleta de Esgoto":
    st.title("Cobertura de Coleta de Esgoto")
    st.write(
        "Esta visualização exibe a evolução da cobertura de coleta de esgoto ao longo dos anos. Os dados mostram tanto a população com acesso à coleta de esgoto quanto aqueles que ainda não têm esse serviço. Essa informação é crucial para monitorar os avanços no saneamento e para planejar ações que melhorem a saúde pública."
    )

    combined_data_sewage = pd.concat([sewage_access, sewage_no_access])

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

    st.plotly_chart(fig)

elif visualizacao == "Impactos Educacionais":
    st.title("Impactos Educacionais")
    st.write(
        "Nesta visualização, analisa-se o impacto do saneamento no atraso escolar dos jovens. Compara-se os dados de atraso escolar entre jovens com e sem acesso a serviços de saneamento. Essa análise destaca a importância do saneamento na educação e no desenvolvimento social, demonstrando como a infraestrutura adequada pode influenciar positivamente a vida dos estudantes."
    )

    df_school_delay = pd.DataFrame(
        {
            "Ano": anos_disponiveis,
            "Com Saneamento": school_delay_with_sanitation["valor"].values,
            "Sem Saneamento": school_delay_without_sanitation["valor"].values,
        }
    )

    df_school_delay = df_school_delay.melt(
        id_vars="Ano",
        value_vars=["Com Saneamento", "Sem Saneamento"],
        var_name="Condição de Saneamento",
        value_name="Atraso Escolar",
    )

    fig = px.bar(
        df_school_delay,
        x="Ano",
        y="Atraso Escolar",
        color="Condição de Saneamento",
        barmode="group",
        labels={
            "Ano": "Ano",
            "Atraso Escolar": "Atraso Escolar (%)",
            "Condição de Saneamento": "Condição de Saneamento",
        },
        title="Indicadores de Atraso Escolar dos Jovens com e sem Saneamento ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Atraso Escolar (%)",
        legend_title="Condição de Saneamento",
        template="plotly_white",
    )

    st.plotly_chart(fig)
    options = [
        "Matemática",
        "Redação",
        "Linguagens e Códigos",
        "Ciências Humanas",
        "Ciências da Natureza",
        "Média",
    ]
    selected_option = st.selectbox(
        "Selecione a nota média no ENEM que deseja visualizar", options
    )
    correct_option = [
        "Nota em matemática no ENEM",
        "Nota na redação no ENEM",
        "Nota em linguagens e códigos no ENEM",
        "Nota em ciências humanas no ENEM",
        "Nota em ciências da natureza no ENEM",
        "Nota média no ENEM",
    ]
    selected_option = correct_option[options.index(selected_option)]

    without_sanitation = data[
        (data["indicador"] == f"{selected_option} - sem banheiro")
        & (data["ano"].isin(anos_selecionados))
    ]
    with_sanitation = data[
        (data["indicador"] == f"{selected_option} - com banheiro")
        & (data["ano"].isin(anos_selecionados))
    ]
    df_enem = pd.concat([without_sanitation, with_sanitation])

    fig = px.bar(
        df_enem,
        x="ano",
        y="valor",
        color="indicador",
        barmode="group",
        labels={"ano": "Ano", "valor": "Nota Média", "indicador": "Indicador"},
        title=f"{selected_option} de alunos com e sem saneamento ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Nota Média",
        legend_title="Indicador",
        template="plotly_white",
    )

    st.plotly_chart(fig)


elif visualizacao == "Custo do Saneamento":
    st.title("Custo do Saneamento")
    st.write(
        "Aqui, apresenta-se os custos associados aos serviços de saneamento ao longo dos anos, incluindo tarifas de água e serviços relacionados. Esta análise é importante para avaliar a viabilidade econômica do saneamento e a capacidade da população de arcar com esses custos, além de informar futuras políticas tarifárias."
    )

    df_cost = data[data["indicador"] == "Custo com os serviços de saneamento"]
    fig = px.line(
        df_cost,
        x="ano",
        y="valor",
        labels={"ano": "Ano", "valor": "Custo (em reais)"},
        title="Custo com os serviços de saneamento ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano", yaxis_title="Custo (em reais)", template="plotly_dark"
    )

    st.plotly_chart(fig)

    df_tariff = data[
        data["indicador"].isin(["Tarifa de água", "Tarifa dos serviços de saneamento"])
    ]

    fig = px.line(
        df_tariff,
        x="ano",
        y="valor",
        color="indicador",
        labels={"ano": "Ano", "valor": "Tarifa (em reais)", "indicador": "Indicador"},
        title="Tarifas de água e dos serviços de saneamento ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Tarifa (em reais)",
        legend_title="Indicador",
        template="plotly_white",
    )

    st.plotly_chart(fig)

elif visualizacao == "Consumo de Água":
    st.title("Consumo de Água")
    st.write(
        "Nesta visualização, analisa-se o consumo de água ao longo dos anos, mostrando a quantidade de água consumida pela população. Compreender esses dados é fundamental para avaliar a demanda por água e para planejar a gestão dos recursos hídricos. Além disso, o consumo per capita de água é um indicador importante para monitorar a eficiência no uso da água e a sustentabilidade ambiental."
    )

    # Selecionar per capita ou não
    per_capita = st.checkbox("Consumo per capita de água", value=True)
    indicador = "Consumo per capita de água" if per_capita else "Consumo de água"

    df_water_consumption = data[data["indicador"] == indicador]

    fig = px.line(
        df_water_consumption,
        x="ano",
        y="valor",
        labels={"ano": "Ano", "valor": "Consumo de Água (em litros)"},
        title="Consumo de água ao longo dos anos",
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Consumo de Água (em litros)",
        template="plotly_white",
    )

    st.plotly_chart(fig)
