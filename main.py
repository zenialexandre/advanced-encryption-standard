from program_gui import generate_program_gui
from generate_keys import expand_keys
from constants import CONTENT
import os
import shutil

(file_path, output_file_name, cipher_key_splitted) = generate_program_gui()

def upload_inputted_file(
    file_path: str
) -> None:
    if (os.path.exists(file_path)):
        file_name: str = os.path.basename(file_path)

        if (os.path.exists(f'{CONTENT}/{file_name}')):
            print('This file is already uploaded!')
            return

        destionation_path: str = os.path.join(CONTENT, file_name)
        shutil.copy(file_path, destionation_path)

upload_inputted_file(file_path)
expand_keys(cipher_key_splitted)
