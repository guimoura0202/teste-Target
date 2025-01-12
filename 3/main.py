#Referência: https://www.askpython.com/python-modules/xmltodict-module
#Pedi a uma ia generativa gerar o xml e o json de exemplos para serem usadas, testei com um mês só e com vários meses
#Fiz o código de forma que o algoritmo analise e se tiver vários meses, o usuário escolha qual mês deseja analisar
#agora vou te explicar o código que fiz
#A função upload_file() é responsável por abrir a janela de seleção de arquivo e carregar o arquivo selecionado. 
#A função analyze_data() é responsável por analisar os dados carregados.
# #Se houver mais de um mês disponível, o usuário é solicitado a escolher um mês para análise.
#A função analyze_month_data() é responsável por analisar os dados de um mês específico.
#Os valores diários são usados para calcular o menor valor, o maior valor, a média e os dias com faturamento acima da média.
#O código foi testado com um arquivo JSON e um arquivo XML contendo dados de faturamento mensal.
#Eu não entendo muito de xml então fiz o codigo baseado no xml que a ia generativa gerou e na biblioteca xmltodict, que foi a que encontrei
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import xmltodict
import xml.parsers.expat

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("XML files", "*.xml")])
    if file_path:
        print(f"Arquivo selecionado: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                if file_path.endswith('.json'):
                    data = json.load(file)
                    file_type = 'json'
                elif file_path.endswith('.xml'):
                    data = xmltodict.parse(file.read())
                    file_type = 'xml'
                else:
                    messagebox.showerror("Erro", "Formato de arquivo não suportado.")
                    return
        except json.JSONDecodeError as e:
            messagebox.showerror("Erro de JSON", f"Erro ao analisar o JSON: {e}")
            return
        except xml.parsers.expat.ExpatError as e:
            messagebox.showerror("Erro de XML", f"Erro ao analisar o XML na linha {e.lineno}, coluna {e.offset}: {e}")
            return
        analyze_data(data, file_type)

def analyze_data(data, file_type):
    months = []
    faturamentos = []
    if file_type == 'json':
        if isinstance(data, dict):
            months = list(data.keys())
        else:
            messagebox.showerror("Erro", "Formato de dados JSON inválido.")
            return
    elif file_type == 'xml':
        faturamento_mensal = data.get('faturamentoMensal', {})
        mes = faturamento_mensal.get('mes')
        ano = faturamento_mensal.get('ano')
        faturamento = faturamento_mensal.get('faturamento')

        # Garantir que mes, ano e faturamento sejam listas
        if isinstance(mes, list):
            months = mes
        elif isinstance(mes, str):
            months = [mes]
        else:
            messagebox.showerror("Erro", "Nenhum mês encontrado no XML.")
            return

        if isinstance(faturamento, list):
            faturamentos = faturamento
        elif isinstance(faturamento, dict):
            faturamentos = [faturamento]
        else:
            messagebox.showerror("Erro", "Nenhum faturamento encontrado no XML.")
            return
    else:
        messagebox.showerror("Erro", "Tipo de arquivo desconhecido.")
        return

    if len(months) > 1:
        print("Os meses disponíveis no arquivo são:")
        for i, month in enumerate(months, 1):
            print(f"{i}. {month}")
        try:
            month_index = int(input("Digite o número do mês que deseja analisar: ")) - 1
            if 0 <= month_index < len(months):
                selected_month = months[month_index]
                print(f"Analisando dados do mês: {selected_month}")
                analyze_month_data(data, file_type, selected_month, month_index, faturamentos)
            else:
                messagebox.showerror("Erro", "Número de mês inválido.")
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Por favor, insira um número.")
    elif len(months) == 1:
        selected_month = months[0]
        print(f"O arquivo contém dados de apenas um mês: {selected_month}")
        analyze_month_data(data, file_type, selected_month, 0, faturamentos)
    else:
        messagebox.showerror("Erro", "Nenhum mês encontrado para análise.")

def analyze_month_data(data, file_type, selected_month, month_index, faturamentos):
    if file_type == 'json':
        month_data = data[selected_month]
        daily_values = {day: valor for day, valor in month_data.items() if isinstance(valor, (int, float)) and valor > 0}
    elif file_type == 'xml':
        faturamento = faturamentos[month_index]
        dias = faturamento.get('dia', [])
        if not isinstance(dias, list):
            dias = [dias]
        daily_values = {dia['data']: float(dia.get('valor', 0)) for dia in dias if float(dia.get('valor', 0)) > 0}
    else:
        messagebox.showerror("Erro", "Tipo de arquivo desconhecido.")
        return

    if not daily_values:
        print("Nenhum valor de faturamento encontrado para análise.")
        return

    min_day, min_value = min(daily_values.items(), key=lambda x: x[1])
    max_day, max_value = max(daily_values.items(), key=lambda x: x[1])
    average_value = sum(daily_values.values()) / len(daily_values)
    days_above_average = [day for day, value in daily_values.items() if value > average_value]

    print(f"Menor valor de faturamento em um dia do mês: {min_value} (Dia: {min_day})")
    print(f"Maior valor de faturamento em um dia do mês: {max_value} (Dia: {max_day})")
    print(f"Número de dias com faturamento acima da média mensal: {len(days_above_average)}")
    print("Dias com faturamento acima da média mensal:")
    for day in days_above_average:
        print(f"Dia: {day}, Valor: {daily_values[day]}")

def main():
    print("Faça upload do arquivo do seu faturamento mensal em formato JSON ou XML.")
    root = tk.Tk()
    root.withdraw()
    upload_file()

if __name__ == "__main__":
    main()
