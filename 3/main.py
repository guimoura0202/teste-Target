#Referência: https://www.askpython.com/python-modules/xmltodict-module
#Fiz o código de forma que o algoritmo analise e se tiver vários meses, o usuário escolha qual mês deseja analisar
#agora vou te explicar o código que fiz
#A função upload_file() é responsável por abrir a janela de seleção de arquivo e carregar o arquivo selecionado. 
#A função analyze_data() é responsável por analisar os dados carregados.
# #Se houver mais de um mês disponível, o usuário é solicitado a escolher um mês para análise.
#A função analyze_month_data() é responsável por analisar os dados de um mês específico.
#Os valores diários são usados para calcular o menor valor, o maior valor, a média e os dias com faturamento acima da média.
#O código foi testado com um arquivo JSON e um arquivo XML contendo dados de faturamento mensal.
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
                    xml_content = file.read()
                    xml_with_root = f"<root>{xml_content}</root>"
                    data = xmltodict.parse(xml_with_root)
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
    daily_values = {}
    
    if file_type == 'json':
        if isinstance(data, list):
            for entry in data:
                dia = entry.get('dia')
                valor = entry.get('valor', 0)
                if isinstance(dia, int) and isinstance(valor, (int, float)) and valor > 0:
                    daily_values[dia] = valor
        else:
            messagebox.showerror("Erro", "Formato de dados JSON inválido.")
            return
    elif file_type == 'xml':
        rows = data.get('root', {}).get('row', [])
        if isinstance(rows, dict): 
            rows = [rows]
        for row in rows:
            dia = row.get('dia')
            valor = row.get('valor', 0)
            try:
                dia = int(dia)
                valor = float(valor)
                if valor > 0:
                    daily_values[dia] = valor
            except (ValueError, TypeError):
                continue
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