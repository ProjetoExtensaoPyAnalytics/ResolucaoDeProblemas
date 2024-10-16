import json
import csv
from selenium import webdriver
import time


def get_chart_data(lg, ls, li):
    select_option("l-g", lg)
    time.sleep(2)  # Aguardar o carregamento
    select_option("l-s", ls)
    time.sleep(2)  # Aguardar o carregamento
    select_option("l-i", li)
    time.sleep(2)  # Aguardar o carregamento do gráfico

    chart_data = driver.execute_script(
        """
        let series = Highcharts.charts[0].series[0].data;
        return series.map(point => ({
            label: point.category,  // Rótulo (ex: ano)
            value: point.y          // Valor
        }));
    """
    )
    return chart_data


def select_option(select_id, option_text):
    driver.execute_script(
        f"""
        let select = document.getElementById('{select_id}');
        Array.from(select.options).forEach(option => {{
            if (option.text === "{option_text}") {{
                select.value = option.value;
                select.dispatchEvent(new Event('change'));
            }}
        }});
    """
    )


# Carregar os dados do JSON
with open("indicadores.json", "r", encoding="utf-8") as f:
    indicadores_data = json.load(f)

driver = webdriver.Chrome()
driver.get("https://www.painelsaneamento.org.br/localidade/evolucao?id=420140")

# Lista para armazenar os dados do gráfico
chart_results = []

for indicador in indicadores_data:
    lg = indicador["l-g"]
    ls = indicador["l-s"]
    li = indicador["l-i"]

    print(f"Obtendo dados para: {lg} - {ls} - {li}")
    try:
        dados_grafico = get_chart_data(lg, ls, li)
        print(f"  Dados do gráfico: {dados_grafico}")
        # Adicionar os dados ao resultado
        for dado in dados_grafico:
            chart_results.append(
                {
                    "grupo": lg,
                    "subgrupo": ls,
                    "indicador": li,
                    "ano": dado["label"],
                    "valor": dado["value"],
                }
            )
    except Exception as e:
        print(f"  Erro ao obter dados do gráfico para {lg} - {ls} - {li}: {e}")
        pass


# Salvar os resultados em um arquivo CSV
with open("chart_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["grupo", "subgrupo", "indicador", "ano", "valor"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Escreve o cabeçalho
    for result in chart_results:
        writer.writerow(result)  # Escreve cada linha de dados

print("Dados dos gráficos salvos com sucesso em 'chart_results.csv'")

driver.quit()
