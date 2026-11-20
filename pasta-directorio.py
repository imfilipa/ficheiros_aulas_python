import PySimpleGUI as sg
path = sg.popup_get_folder('Selecione o ficheiro')
print(path)