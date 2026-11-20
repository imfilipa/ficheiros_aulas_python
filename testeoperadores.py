def mediafinal ():
    a = int(input ("escreva a primeira nota"))
    b = int(input ("escreva a segunda nota"))
    c = int(input ("escreva a terceira nota"))

    media = (a+ b + c) / 3
    print(media)

    if media < 9:
        print(f"Infelizmente você está reprovado")
    else:
        print(f"parabéns você está aprovado")
mediafinal()