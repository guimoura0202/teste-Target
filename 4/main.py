# O código abaixo calcula a porcentagem de faturamento de cada estado em relação ao faturamento total
# Para isso, primeiro é calculado o faturamento total somando todos os valores do dicionário
# Em seguida, um loop é utilizado para iterar sobre os itens do dicionário e calcular a porcentagem de cada estado em relação ao faturamento total
# O resultado é então impresso na tela com duas casas decimais :)
faturamentos = {
    "SP": 67836.43,
    "RJ": 36678.66,
    "MG": 29229.88,
    "ES": 27165.48,
    "Outros": 19849.53
}
faturamento_total = sum(faturamentos.values())

for estado, valor in faturamentos.items():
    porcentagem = (valor / faturamento_total) * 100
    print(f"{estado}: {porcentagem:.2f}%")