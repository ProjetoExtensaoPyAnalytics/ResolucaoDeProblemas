import streamlit as st
import pandas as pd
import plotly.express as px

#agrupar as apresentações de medicamentos em categorias
def agrupar_apresentacao(apresentacao):
    apresentacao = apresentacao.lower()  #converter p minusculas
    if "comprimido" in apresentacao:
        return "Comprimido"
    elif "solução oral" in apresentacao:
        return "Solução Oral"
    elif "suspensão oral" in apresentacao:
        return "Suspensão Oral"
    elif "xarope" in apresentacao:
        return "Xarope"
    elif "cápsula" in apresentacao:
        return "Cápsula"
    elif "injeção" in apresentacao or "injetável" in apresentacao:
        return "Injeção"
    elif "creme" in apresentacao:
        return "Creme"
    elif "gel" in apresentacao:
        return "Gel"
    elif "pomada" in apresentacao:
        return "Pomada"
    elif "loção" in apresentacao:
        return "Loção"
    elif "aerossol" in apresentacao or "inalação" in apresentacao:
        return "Aerossol"
    elif "xampu" in apresentacao:
        return "Xampu"
    elif "pó para solução" in apresentacao:
        return "Pó para Solução"
    elif "pasta" in apresentacao:
        return "Pasta"
    else:
        return "Outros"

def exibir():
    path = "Planilha-REMUME.xlsx"
    df = pd.read_excel(path)

    #menu para navegar
    st.sidebar.title("Medicamentos em Araranguá")
    visualizacao = st.sidebar.radio(
        "Visualizações disponíveis:",
        ["Disponibilidade de Medicamentos", "Apresentações de Medicamentos", "Distribuição por Unidade de Saúde", "Classes de Medicamentos"]
    )

    if visualizacao == "Disponibilidade de Medicamentos":
        st.title("Disponibilidade de Medicamentos")
        st.markdown("""<div style="background-color:#D6F3E9; padding:15px; border-radius:8px;">
                        <p style="font-size:14px; color:#555555;">Esta funcionalidade permite verificar se um medicamento específico está disponível na rede de saúde do município. 
                        Ao buscar o medicamento desejado, o sistema retornará os locais onde ele pode ser encontrado, proporcionando uma busca rápida e facilitada para os cidadãos.</p>
                        </div>""", unsafe_allow_html=True)

        medicamento_input = st.text_input("Digite o nome do medicamento:")
        #verificar se o medicamento esta presente no dataset
        if medicamento_input:
            normalized_input = medicamento_input.lower()
            filtered_df = df[df['Medicamento'].str.lower().str.contains(normalized_input)]

            if not filtered_df.empty:
                st.success(f"✅ O medicamento '{medicamento_input}' está disponível.")
                local_de_acesso = filtered_df['Local de acesso'].unique()
                st.write("Disponível nos locais:")
                st.markdown(", ".join(f"`{loc}`" for loc in local_de_acesso))
            else:
                st.warning(f"⚠️ O medicamento '{medicamento_input}' não está disponível.")

#aba de medicamentos por apresentacao
    elif visualizacao == "Apresentações de Medicamentos":
        st.title("Apresentações de Medicamentos")
        st.markdown("""<div style="background-color:#D6F3E9; padding:15px; border-radius:8px;">
                        <p style="font-size:14px; color:#555555;">Esta visualização mostra as diferentes apresentações dos medicamentos disponíveis na rede de saúde, 
                        agrupadas em categorias como comprimidos, xaropes, injeções, entre outras. Compreender a distribuição das formas de apresentação auxilia no planejamento e no atendimento às necessidades específicas dos pacientes.</p>
                        </div>""", unsafe_allow_html=True)

        if not df.empty:
            df['Apresentação Agrupada'] = df['Apresentação'].apply(agrupar_apresentacao)
            presentation_count = df['Apresentação Agrupada'].value_counts()

            presentation_fig = px.bar(
                x=presentation_count.index,
                y=presentation_count.values,
                labels={'x': 'Apresentação Agrupada', 'y': 'Quantidade de Medicamentos'},
                title="Medicamentos por Apresentação Agrupada",
                color=presentation_count.index,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(presentation_fig)

#aba de distribuicao por US
    elif visualizacao == "Distribuição por Unidade de Saúde":
        st.title("Distribuição por Unidade de Saúde")
        st.markdown("""<div style="background-color:#D6F3E9; padding:15px; border-radius:8px;">
                        <p style="font-size:14px; color:#555555;">Esta visualização apresenta o número de medicamentos disponíveis em cada unidade de saúde, como Farmácia Bom Pastor e UBSs. 
                        A análise desses dados permite uma visão mais clara da oferta de medicamentos por local, ajudando a identificar onde há maior ou menor disponibilidade de medicamentos.</p>
                        </div>""", unsafe_allow_html=True)

        if not df.empty:
            farmacia_count = df[df['Local de acesso'].str.contains("Farmácia Bom Pastor", case=False, na=False)].shape[0]
            ubs_count = df[df['Local de acesso'].str.contains("UBS", case=False, na=False)].shape[0]

            bar_fig = px.bar(
                x=["Farmácia Bom Pastor", "UBS"], 
                y=[farmacia_count, ubs_count],
                labels={'x': 'Unidade de Saúde', 'y': 'Quantidade de Medicamentos'},
                title="Número de Medicamentos por Unidade de Saúde",
                color=["Farmácia Bom Pastor", "UBS"],
                color_discrete_sequence=["lightgreen", "lightblue"]
            )
            st.plotly_chart(bar_fig)

#aba de medicamentos por classe
    elif visualizacao == "Classes de Medicamentos":
        st.title("Distribuição por Classe de Medicamentos")
        st.markdown(
            "Esta visualização exibe a distribuição dos medicamentos de acordo com suas classes terapêuticas. "
            "Essa categorização facilita a compreensão sobre a variedade de medicamentos disponíveis, permitindo identificar quais classes estão mais representadas na rede de saúde."
        )
        st.markdown("""
            <div style="background-color:#FFEBCC; padding:10px; border-radius:5px; border: 1px solid #FFA500;">
                <p style="font-size:14px; color:#FFA500; margin: 0;">💡 Para melhor visualização, clique nas setas à direita para ver em tela cheia.</p>
            </div>
        """, unsafe_allow_html=True)

        if not df.empty:
            class_distribution = df['Classe'].value_counts()

            pie_fig = px.pie(
                class_distribution, 
                values=class_distribution.values, 
                names=class_distribution.index,
                title="Distribuição de Medicamentos por Classe",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            st.plotly_chart(pie_fig)


    st.markdown("---")
    st.markdown("Dados obtidos a partir do [REMUME](http://saude.ararangua.sc.gov.br:81/site/images/arquivos/REMUME.pdf). Projeto desenvolvido por [PyAnalytics](https://www.linkedin.com/company/pyanalytics/posts/?feedView=all)")
