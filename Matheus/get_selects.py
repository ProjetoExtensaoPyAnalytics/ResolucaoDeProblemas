import json
import time
from selenium import webdriver

# Configura o WebDriver (pode ser qualquer navegador)
driver = webdriver.Chrome()

# Navegar para a URL
driver.get("https://www.painelsaneamento.org.br/localidade/evolucao?id=420140")


# Função para obter as opções de um select via JavaScript
def get_select_options(select_id):
    return driver.execute_script(
        f"""
        let select = document.getElementById('{select_id}');
        let options = Array.from(select.options).map(option => option.text);
        return options;
    """
    )


# Função para selecionar uma opção do select via JavaScript
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


# Lista para armazenar os dados
indicadores_data = []

# Capturar todas as opções de 'l-g' (grupo)
lg_options = get_select_options("l-g")

# Iterar sobre cada 'l-g' e capturar 'l-s' (subgrupos)
for lg in lg_options:
    print(f"Selecionando l-g: {lg}")
    select_option("l-g", lg)
    time.sleep(2)  # Aguardar o carregamento do l-s

    ls_options = get_select_options("l-s")

    # Iterar sobre cada 'l-s' e capturar 'l-i' (indicadores)
    for ls in ls_options:
        print(f"  Selecionando l-s: {ls}")
        select_option("l-s", ls)
        time.sleep(2)  # Aguardar o carregamento dos l-i

        li_options = get_select_options("l-i")

        # Armazenar os dados capturados
        for li in li_options:
            print(f"    Indicador (l-i): {li}")
            if (
                "Selecione" not in lg
                and "Selecione" not in ls
                and "Selecione" not in li
            ):
                indicadores_data.append({"l-g": lg, "l-s": ls, "l-i": li})

# Salvar em arquivo JSON
with open("indicadores.json", "w", encoding="utf-8") as f:
    json.dump(indicadores_data, f, ensure_ascii=False, indent=4)

print("Indicadores salvos com sucesso em 'indicadores.json'")

# Fechar o driver no final
driver.quit()
