import PySimpleGUI as psg

'''
    This GUI returns a tuple of three 'str'.
    [file_path, output_file_name, cipher_key].
'''

def generate_program_gui() -> tuple[str, str, str]:
    psg.theme('DarkTeal2')
    window_layout: list[list] = [
        [psg.T('')],
        [psg.Text('Choose the file to be uploaded: '), psg.Input(), psg.FileBrowse(key='file_path')],
        [psg.T('')],
        [psg.Text('The name of the output file: '), psg.Input(key='output_file_name')],
        [psg.T('')],
        [psg.Text('The cipher key to be used: '), psg.Input(key='cipher_key')],
        [psg.T('')],
        [psg.Button('Ok'), psg.Button('Cancel')]
    ]
    window: psg.Window = psg.Window('Advanced Encryption Standard', window_layout)

    while (True):
        event, values = window.read()

        if (event == psg.WIN_CLOSED or event == 'Cancel'):
            break
        elif (event == 'Ok'):
            return values['file_path'], values['output_file_name'], values['cipher_key']

    window.close()
