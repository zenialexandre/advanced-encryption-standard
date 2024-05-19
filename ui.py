import PySimpleGUI as psg
from constants import FILE_PATH, OUTPUT_FILE_NAME, CIPHER_KEY, OK, CANCEL, CHOSE_FILE_TIYPE

'''
    This GUI returns a tuple of two 'str' and a 'list[str]'.
    [file_path, output_file_name, cipher_key_splitted].
'''
def generate_program_gui() -> tuple[str, str, list[str]]:
    psg.theme('DarkTeal2')
    window_layout: list[list] = [
        [psg.T('')],
        [psg.Text('Choose the file to be uploaded: '), psg.Input(), psg.FileBrowse(key=FILE_PATH)],
        [psg.T('')],
        [psg.Text('Choose the type of file: '), psg.Combo(['-', 'Text', 'Binary'], default_value='-', key=CHOSE_FILE_TIYPE)],
        [psg.T('')],
        [psg.Text('The name of the output file: '), psg.Input(key=OUTPUT_FILE_NAME)],
        [psg.T('')],
        [psg.Text('Example of cipher key: 20,1,94,33,199,0,48,9,31,94,112,40,59,30,100,248')],
        [psg.Text('The cipher key to be used: '), psg.Input(key=CIPHER_KEY)],
        [psg.T('')],
        [psg.Button(OK), psg.Button(CANCEL)],
        [psg.T('')],
        [psg.StatusBar('', size=(20, 1), text_color='red', key='status')]
    ]
    window: psg.Window = psg.Window('Advanced Encryption Standard', window_layout)
    prompt: any = window['status'].update
    input_list: list = [
        key for key, value in window.key_dict.items() if isinstance(value, psg.Input)
    ]

    while (True):
        event, values = window.read()

        if (event == psg.WIN_CLOSED or event == CANCEL):
            break
        elif (event == OK):
            if (all(map(str.strip, [values[key] for key in input_list]))):
                cipher_key_splitted: list[str] = values[CIPHER_KEY].split(',')
                file_type = values[CHOSE_FILE_TIYPE]

                if(file_type == '-'):
                    prompt('Please choose the file type')
                else:
                    if (len(cipher_key_splitted) == 16):
                        return values[FILE_PATH], values[OUTPUT_FILE_NAME], cipher_key_splitted, file_type
                    else:
                        prompt('The cipher key must have 16 bytes.')
            else:
                prompt('Please, fill in the necessary fields.')

    window.close()
