import PySimpleGUI as sg

sg.theme('LightGrey5')

layout = [
    [sg.Text('', key='-text-Title', font=("Arial", 20))],
    [sg.Text('Nome:', key='-text-Nome', font=("Arial", 14)), sg.InputText(), sg.Button('Ok', font=("Arial", 16), key='-button-ok')],
    [sg.Image(r'img/bus-magic-school-bus.gif', key='-image')],
    [sg.Text('Text Body', visible=False, key='-text-body', font=("Arial", 16))],
    [sg.Button('  3  ', font=("Arial", 16), key='-button-resp1' , visible=False), sg.Button('  4  ', font=("Arial", 16), key='-button-resp2', visible=False ),
     sg.Button('  5  ', font=("Arial", 16), key='-button-resp3' ,visible=False), sg.Button('  6  ', font=("Arial", 16), key='-button-resp4' , visible=False)],
    [sg.Button('Next', font=("Arial", 16), key='-button-Next1', visible=False)],
    [sg.Text('Clica entregar quando terminares', visible=False, key='-text-End', font=("Arial", 16))],
    [sg.Button('Entregar', font=("Arial", 16),visible=False ,key='-button-entregar')]
]

window = sg.Window('', layout, finalize=True )