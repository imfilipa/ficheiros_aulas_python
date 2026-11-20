#Tarefa "if/else" aula 4/11

numeros = [10,15,20,25,30,35]

numero_digitado = int(input("Digite um numero: "))

if numero_digitado in numeros:
    print(f"O número {numero_digitado} está na lista")

else:
    print(f"O número {numero_digitado} não está na lista")