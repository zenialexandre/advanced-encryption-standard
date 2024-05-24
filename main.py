# Alexandre Zeni, Bruno Gabriel de Sousa and Leonardo Oliani Fernandes

from ui import generate_program_gui
from keys import expand_keys
from cipher import ciphering_process
from constants import CONTENT
import os
import shutil

def main() -> None:
    (file_path, output_file_name, cipher_key_splitted) = generate_program_gui()
    input_file_path: str = upload_inputted_file(file_path)
    start_ciphering_process(
        input_file_path,
        output_file_name,
        expand_keys(cipher_key_splitted)
    )

def upload_inputted_file(
    file_path: str
) -> str:
    if (os.path.exists(file_path)):
        file_name: str = os.path.basename(file_path)
        destionation_path: str = os.path.join(CONTENT, file_name)

        if (os.path.exists(destionation_path)):
            print('This file is already uploaded!')
            return destionation_path

        shutil.copy(file_path, destionation_path)
        return destionation_path

def start_ciphering_process(
    input_file_path: str,
    output_file_name: str,
    key_schedule: list[list[str]]
) -> None:
    ciphering_process(
        input_file_path,
        os.path.join(CONTENT, f'{output_file_name}.bin'),
        key_schedule
    )

if (__name__ == '__main__'):
    main()
