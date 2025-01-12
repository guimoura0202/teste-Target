#A função reverte recebe uma string como parâmetro e retorna a string invertida.
#A variável palavra_revertida é inicializada como uma string vazia.
#O loop for itera sobre cada caractere da palavra.
#A cada iteração, o caractere é concatenado ao início da palavra_revertida.
#Por fim, a palavra revertida é retornada.

def reverte(palavra):
    palavra_revertida = ""
    for char in palavra:
        palavra_revertida = char + palavra_revertida
    return palavra_revertida

palavra = input("Digite uma palavra: ")
print("Palavra invertida:", reverte(palavra))