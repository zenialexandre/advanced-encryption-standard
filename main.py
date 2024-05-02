from program_gui import generate_program_gui
from generate_keys import expand_keys
from encrypt_data import ciphering_process
from constants import CONTENT
import os
import shutil

def main() -> None:
    (file_path, output_file_name, cipher_key_splitted) = generate_program_gui()
    upload_inputted_file(file_path)
    start_ciphering_process(
        output_file_name,
        expand_keys(cipher_key_splitted)
    )

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

def start_ciphering_process(
    output_file_name: str,
    key_schedule: list[list[str]]
) -> None:
    ciphering_process(
        output_file_name,
        key_schedule
    )

if (__name__ == '__main__'):
    main()
