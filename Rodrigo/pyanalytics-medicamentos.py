import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file):
    df = pd.read_excel(file)
    return df

uploaded_file = st.sidebar.file_uploader("Envie o arquivo de medicamentos (.xlsx)", type="xlsx")

if uploaded_file:
    df = load_data(uploaded_file)

    st.title("Consulta de Medicamentos - Prefeitura de Araranguá")
    st.markdown("---")

    pagina = st.sidebar.radio(
        "Navegue pelas páginas:",
        ["Início", "Disponibilidade de Medicamentos", "Análise de Dados"]
    )

    if pagina == "Início":
        st.header("Bem-vindo ao Sistema de Consulta de Medicamentos")
        st.markdown(
            """
            Esta aplicação permite que você consulte a **disponibilidade de medicamentos** oferecidos pela Prefeitura de Araranguá.
            
            ### Funcionalidades:
            - Verifique se um determinado medicamento está disponível no sistema de saúde local.
            - Use o menu à esquerda para navegar entre as páginas:
                - **Disponibilidade de Medicamentos**: Para consultar se um medicamento específico está disponível.
                - **Análise de Dados**: Para ver gráficos de análise dos medicamentos.
            """
        )
        
        st.markdown(
            """
            <div style='text-align: center;'>
                <img src='https://www.ararangua.sc.gov.br/img/logo.png' width='150'/>
            </div>
            """, 
            unsafe_allow_html=True
        )

    elif pagina == "Disponibilidade de Medicamentos":
        st.header("Verifique a Disponibilidade do Medicamento")
        medicamento_input = st.text_input("Digite o nome do medicamento:")
        
        if medicamento_input:
            normalized_input = medicamento_input.lower()
            filtered_df = df[df['Medicamento'].str.lower().str.contains(normalized_input)]

            if not filtered_df.empty:
                st.success(f"O medicamento '{medicamento_input}' está disponível.")
                local_de_acesso = filtered_df['Local de acesso'].unique()
                st.write(f"O medicamento está disponível nos seguintes locais de acesso: {', '.join(local_de_acesso)}")
            else:
                st.warning(f"O medicamento '{medicamento_input}' não está disponível.")

    elif pagina == "Análise de Dados":
        st.header("Análise de Dados dos Medicamentos por Unidade de Saúde")

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

            class_distribution = df['Classe'].value_counts()

            pie_fig = px.pie(
                class_distribution, 
                values=class_distribution.values, 
                names=class_distribution.index,
                title="Distribuição de Medicamentos por Classe",
                color_discrete_sequence=px.colors.qualitative.Set1,
                height=1000, 
                width=1000   
            )
            st.plotly_chart(pie_fig)

            presentation_count = df['Apresentação'].value_counts()
            presentation_fig = px.bar(
                x=presentation_count.index,
                y=presentation_count.values,
                labels={'x': 'Apresentação', 'y': 'Quantidade de Medicamentos'},
                title="Medicamentos por Apresentação",
                color=presentation_count.index,
                color_discrete_sequence=px.colors.qualitative.Set2,
                height=1000, 
                width=1000  
            )
            st.plotly_chart(presentation_fig)

            access_summary = df['Local de acesso'].value_counts().reset_index()
            access_summary.columns = ['Local de Acesso', 'Quantidade de Medicamentos']
            st.subheader("Quantidade de Medicamentos por Local de Acesso")
            st.table(access_summary)

            unique_classes = df['Classe'].unique()
            selected_class = st.selectbox("Selecione uma Classe de Medicamento:", unique_classes)

            filtered_meds = df[df['Classe'] == selected_class]

            if not filtered_meds.empty:
                st.subheader(f"Medicamentos da Classe: {selected_class}")
                st.write(filtered_meds[['Medicamento', 'Apresentação', 'Local de acesso']])

                med_count_fig = px.bar(
                    filtered_meds, 
                    x='Medicamento', 
                    title=f"Medicamentos da Classe: {selected_class}",
                    labels={'Medicamento': 'Medicamento'},
                    color='Apresentação',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(med_count_fig)
            else:
                st.warning("Não há medicamentos disponíveis para a classe selecionada.")

            bubble_fig = px.scatter(
                class_distribution.reset_index(),
                x='index',
                y=class_distribution.values,
                size=class_distribution.values,
                color='index',
                labels={'x': 'Classe', 'y': 'Quantidade de Medicamentos'},
                title="Distribuição de Medicamentos por Classe (Gráfico de Bolhas)",
                size_max=60,
                color_discrete_sequence=px.colors.qualitative.Set3,
                height=1000, 
                width=1000   
            )
            st.plotly_chart(bubble_fig)

st.markdown("---")
st.markdown("Desenvolvido por [PyAnalytics](https://www.linkedin.com/company/pyanalytics/posts/?feedView=all)")
