import numpy as np
from binascii import hexlify

'''
    Block mode of operation: ECB;
    Block filling schema: PKCS#7;
'''

def ciphering_process(
    input_file_path: str,
    output_file_path: str,
    key_schedule: list[list[str]]
) -> None:
    with open(input_file_path, 'rb') as data:
        input_file_path_data: bytes = data.read()

    state_matrices: dict = get_state_matrices_on_demand(
        input_file_path_data
    )

    print(state_matrices)

def get_state_matrices_on_demand(
    input_file_path_data: bytes
) -> dict:
    state_matrices: list[list[list[str]]] = []
    data_byte_counter: int = 0

    while True:
        state_matrix: list[list[str]] = []

        if (len(input_file_path_data) > 0):
            for row in range(0, 16, 4):
                state_matrix.append(hexlify(input_file_path_data[row: row + 4]).decode())
                input_file_path_data = input_file_path_data[data_byte_counter]
                data_byte_counter += 1
                state_matrices.append(state_matrix)
        else:
            break

    return { index: value for index, value in enumerate(state_matrix) }
