import PySimpleGUI as psg

def generate_program_gui() -> None:
    window_layout: list[list] = [
        [psg.Text('Upload your archive here: '), psg.InputText()],
        [psg.Button('Ok'), psg.Button('Cancel')]
    ]
    window: psg.Window = psg.Window('Advanced Encryption Standard', window_layout)

    while (True):
        event, _ = window.read()

        if (event == psg.WIN_CLOSED or event == 'Cancel'):
            break

    window.close()
