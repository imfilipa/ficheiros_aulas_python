import csv  # Importa o módulo csv, que permite ler e escrever ficheiros CSV (ficheiros com dados separados por delimitadores).

with open("Produtos.csv", "r") as ficheiro:  # Abre o ficheiro Produtos.csv em modo de leitura ("r") e atribui-lhe o nome ficheiro.
    ficheiro_csv = csv.reader(ficheiro, delimiter=",")  # Cria um leitor CSV que lê o conteúdo do ficheiro e separa os valores sempre que encontra umavírgula.
    for linha in ficheiro_csv:  # Percorre o ficheiro linha a linha, atribuindo cada linha lida à variável linha.
        print(linha)  # Apresenta no ecrã os valores da linha atual, normalmente sob a forma de uma lista Python.
