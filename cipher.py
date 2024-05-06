import os
import numpy as np
from binascii import hexlify
from constants import CONTENT

def ciphering_process(
    input_file_path: str,
    output_file_path: str,
    key_schedule: list[list[str]]
) -> None:
    # O processo comeca pegando o valor do arquivo...
    with open(input_file_path, 'rb') as data:
        input_file_path_data: bytes = data.read()

    print(input_file_path_data)

    # Depois, a gente salva no arquivo de saida
    print(output_file_path)
    #with open(output_file_path, 'wb') as data:
        #data.write(input_file_path_data)
