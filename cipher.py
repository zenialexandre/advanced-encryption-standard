from binascii import hexlify
from utils import make_state_matrix, get_converted_to_hexadecimal

'''
    Block mode of operation: ECB;
    Block filling schema: PKCS#7;
'''

def ciphering_process(
    input_file_path: str,
    output_file_path: str,
    key_schedule: list[list[str]]
) -> None:
    input_file_path_data_str: str = ''
    ciphered_file_data: str = ''
    final_result: list[list[list[str]]] = []

    with open(input_file_path, 'rb') as data:
        input_file_path_data: bytes = data.read()

    input_file_path_data_str = input_file_path_data.decode().strip()

    for data_slice in iterate_by_data_slices(input_file_path_data_str):
        entrance_state_matrix: list[list[str]] = []
        exit_state_matrix: list[list[str]] = []

        if (len(data_slice) < 16):
            data_slice = apply_block_filling_schema(data_slice, 16)
        
        entrance_state_matrix = get_converted_to_hexadecimal(
            make_state_matrix([char for char in data_slice])
        )
    
        exit_state_matrix = execute_process_by_rounds(
            key_schedule,
            entrance_state_matrix,
            exit_state_matrix
        )
        final_result.extend([row for row in exit_state_matrix])

    ciphered_file_data = get_ciphered_data_from_matrix(final_result)

    #with open(output_file_path, 'wb') as data:
    #    data.write(ciphered_file_data)

def iterate_by_data_slices(
    input_file_path_data_str: str
):
    for index in range(0, len(input_file_path_data_str), 16):
        yield input_file_path_data_str[index:index + 16]

def apply_block_filling_schema(
    data_slice: str,
    default_block_size: int
) -> str:
    if (default_block_size >= 1 and default_block_size <= 255):
        number_of_missing_bytes: int = default_block_size - len(data_slice)

        for _ in range(number_of_missing_bytes):
            data_slice += str(number_of_missing_bytes)

        return data_slice
    else:
        raise Exception("PKCS#7 only accepts blocks from 1 to 255 bytes.")

def execute_process_by_rounds(
    key_schedule: list[list[str]],
    entrance_state_matrix: list[list[str]],
    exit_state_matrix: list[list[str]]
) -> list[list[str]]:
    for index in range(10):
        # Faz o genericao.

        if (index + 1 == 10):
            # Faz o especifico da ultima rodada.
            continue
        else:
            #Faz o especifico da rodada 1 ate a 9.
            continue

    return exit_state_matrix

def get_ciphered_data_from_matrix(
    final_result: list[str]
) -> str:
    ciphered_file_data: str = ''

    for block in final_result:
        for byte in block:
            ciphered_file_data += byte

    return ciphered_file_data
