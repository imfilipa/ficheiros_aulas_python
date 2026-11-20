import PySimpleGUI as sg

class TelaPython:
    def __init__(self):
        #Layout
        Layout = [
        [sg.Text('Filipa'),sg.Input()],
        [sg.Text('25'),sg.Input()],
        [sg.Button('Enviar dados ... sem ideias')]
        ]

        #Janela
        janela = sg.Window("Dados da Filipa").layout(Layout)

        #Extrair os dados da Tela
        self.button, self.values = janela.Read()
    
    def Iniciar(self):
        print(self.values)


tela = TelaPython()
tela.Iniciar()
