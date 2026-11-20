import PySimpleGUI as sg
for i in range(1000):
    sg.one_line_progress_meter(
        'Progresso',
        i + 1,
        1000,
        'Progresso',
        'Progresso'
    )