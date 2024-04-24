import PySimpleGUI as psg

'''
    This GUI returns the path of the uploaded file.
'''

def generate_program_gui() -> str:
    psg.theme('DarkTeal2')
    window_layout: list[list] = [
        [psg.T('')],
        [psg.Text('Choose the file to be uploaded: '), psg.Input(), psg.FileBrowse(key='file_path')],
        [psg.T('')],
        [psg.Button('Ok'), psg.Button('Cancel')]
    ]
    window: psg.Window = psg.Window('Advanced Encryption Standard', window_layout)

    while (True):
        event, values = window.read()

        if (event == psg.WIN_CLOSED or event == 'Cancel'):
            break
        elif (event == 'Ok'):
            return values['file_path']

    window.close()
