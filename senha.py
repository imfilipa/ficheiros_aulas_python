import PySimpleGUI as sg
text = sg.popup_get_text('Escreva a tua senha', password_char='*')
sg.popup(f'palavra passe:{text}')