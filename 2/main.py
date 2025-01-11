numero_teste = input("Qual número deseja verificar se é da sequência de Fibonacci? ")
numero_teste = int(numero_teste)

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
def verifica_fibonacci(numero_teste):
    i = 0
    while fibonacci(i) < numero_teste:
        i += 1
    if fibonacci(i) == numero_teste:
        return True
    else:
        return False
    
if verifica_fibonacci(numero_teste):
    print(f"O número {numero_teste} está na sequência de Fibonacci.")
else:
    print(f"O número {numero_teste} não está na sequência de Fibonacci.")

#Bom, agora vou explicar o código que eu fiz,
#Basicamente a função fibonacci é uma função recursiva que retorna o n-ésimo número da sequência de Fibonacci.
#Exemplo: Recebe o número 6 e retorna o número 8, pois o número 8 é o 6º número da sequência de Fibonacci.
#A função verifica_fibonacci recebe um número e verifica se ele está na sequência de Fibonacci.
#Daí ele chama a função fibonacci enquanto for menor que o número que o algoritmo recebeu.
#Depois ele verifica se o número que a função fibonacci retornou é igual ao número que o algoritmo recebeu.
#Se for, ele retorna True, senão ele retorna False.
#Depois só uso pra printar a resposta ao usuário!