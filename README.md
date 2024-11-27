# Portal de Dados de Araranguá

Essa é uma iniciativa do **PyAnalytics**, em especial do grupo **Resolução de Problemas**, que tem como objetivo resolver problemas envolvendo o uso de dados públicos, utilizando **Python** e **bibliotecas de análise de dados**.

O produto final deste projeto consiste em uma aplicação **Streamlit** que apresenta diversas visualizações e análises sobre os **dados públicos de diversos segmentos da cidade de Araranguá**. As informações podem incluir dados públicos sobre **Saúde**, **Educação**, **Patrimônio**, **Receitas e Despesas**, dentre outros, obtidos de portais governamentais. 

A seguir serão apresentados em detalhes os **Objetivos**, **Metodologia** e **Desenvolvimento** do projeto.

Você pode acessar a aplicação clicando [aqui](https://dadosdearu.streamlit.app)

---

## Objetivo do Projeto

O objetivo do projeto é **promover maior disseminação de informações** e apresentar análises relevantes que possam impactar positivamente a sociedade. Isso inclui:
- **População em geral:** facilitar o acesso a informações úteis sobre saúde pública.
- **Entidades interessadas:** auxiliar órgãos governamentais, ONGs e pesquisadores com análises claras e visuais extraídas de dados públicos.

---

## Metodologia

Para a realização deste projeto, utilizamos a metodologia **Scrum**, que permite uma organização eficiente do trabalho em **sprints** com entregas incrementais. Cada membro do grupo foi responsável por desenvolver e implementar uma aba de navegação específica dentro da aplicação.

### Levantamento de dados junto a população de Araranguá
Primeiramente foi desenvolvido um instrumento de coleta de dados com XX questões para identificar o perfil do respondente e os segmentos de dados de maior interesse. (Colocar link para pdf do survey). Na sequência os membros do projeto ficaram responsáveis por coletar os dados juntos a diversos segmentos da sociedade.

### Análise de Resultados
Foram coletadas aproximadamente 100 respostas, cuja análise resultou nos seguintes pontos:
- Somente um pouco mais da metade dos respondentes sabem que dados públicos sobre sua cidade estão disponiveis;
- O grupo de dados de maior interesse dos respondentes foi o de **Saúde**.
- Para mais detalhes acesse (PDF com os resultados)

-- 

## Desenvolvimento
A partir da análise dos resultados optou-se por focar em análises relacionadas aos dados de **Saúde**. Os recortes escolhidos foram **Medicamentos, Vacinas, Óbitos, Internações e Saneamento**. Bases de dados públicas para os recortes foram inicialmente exploradas, resultando em um conjunto de perguntas possíveis de serem respondidas via análise e visualização de dados. 

Os detalhes do desenvolvimento de cada painel, pode ser encontrado na seção [Wiki do repositório](https://github.com/seu-repo/wiki), onde são explicados:
- Os dados utilizados e como foram obtidos e tratados.
- Os métodos de análise aplicados.
- Como os painéis foram estruturados e pensados.
- O impacto esperado para cada painel.

Abaixo você pode acessar a Wiki para ver a documentação específica de cada painel:
1. **[Vacinas](https://github.com/ProjetoExtensaoPyAnalytics/ResolucaoDeProblemas/wiki/Vacinas)**
2. **[Saneamento](https://github.com/ProjetoExtensaoPyAnalytics/ResolucaoDeProblemas/wiki/Saneamento)**
3. **[Internações](https://github.com/ProjetoExtensaoPyAnalytics/ResolucaoDeProblemas/wiki/Internações)**
4. **[Medicamentos](https://github.com/ProjetoExtensaoPyAnalytics/ResolucaoDeProblemas/wiki/Medicamentos)**
5. **[Óbitos](https://github.com/ProjetoExtensaoPyAnalytics/ResolucaoDeProblemas/wiki/Óbitos)**

A aplicação foi desenvolvida utilizando o framework **Streamlit**, uma ferramenta poderosa para criar dashboards e visualizações de dados de forma rápida e eficiente. Durante o desenvolvimento, as seguintes funcionalidades foram implementadas:
- **Interface interativa:** Com abas de navegação claras e organizadas.
- **Gráficos dinâmicos:** Desenvolvidos com bibliotecas como Plotly e Matplotlib.
- **Integração com dados públicos:** Dados obtidos de fontes governamentais foram tratados e integrados diretamente na aplicação.

### Algumas capturas de tela da aplicação:

#### Página Inicial
![Página Inicial](https://github.com/user-attachments/assets/6e62f541-5305-43ee-aef4-0912f5516535)

#### Alguns exemplos das abas
![Aba de Vacinas](https://github.com/user-attachments/assets/c622ca72-491b-4d75-ae37-67ba1a5c9b25)

![Aba de Saneamento](https://github.com/user-attachments/assets/947d5463-2dc6-4460-bac3-c62221937e5a)


### Deploy no Streamlit Cloud
Para facilitar o acesso público, utilizamos o **Streamlit Cloud** para hospedar a aplicação. O processo incluiu:
1. Subir o código-fonte para o **GitHub**.
2. Conectar o repositório ao Streamlit Cloud.
3. Atualizar códigos de cada membro
4. Configurar as dependências no arquivo `requirements.txt`.
5. Publicar o link público da aplicação.

A aplicação pode ser acessada diretamente no [Streamlit Cloud](https://link-para-aplicacao-streamlit).

---


Sinta-se à vontade para explorar o repositório e a aplicação, contribuir com sugestões ou reportar problemas.

**Equipe PyAnalytics**
