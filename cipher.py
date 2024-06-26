import numpy as np
from os import path
from binascii import hexlify
from constants import UTF_8
from utils import \
    get_static_s_box, \
    apply_subword_or_subbytes, \
    get_static_l_table, \
    get_static_e_table

'''
    Block mode of operation: ECB;
    Block filling schema: PKCS#7;
'''

EXTRA_BLOCK: list[list[str]] = [
    ['16', '16', '16', '16'],
    ['16', '16', '16', '16'],
    ['16', '16', '16', '16'],
    ['16', '16', '16', '16']
]

MULTIPLICATION_MATRIX: list[list[int]] = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

def ciphering_process(
    input_file_path: str,
    output_file_path: str,
    key_schedule: list[list[str]]
) -> None:
    final_ciphered_result: list[str] = []
    input_file_path_data = read_file_data(input_file_path)
    data_slices: list[list[str]] = get_data_slices_to_iterate(input_file_path_data)

    for data_slice in data_slices:
        data_slice_copy: list[str] = np.copy(data_slice).tolist()
        entrance_state_matrix: list[list[str]] = []
        exit_state_matrix: list[list[str]] = []

        if (len(data_slice_copy) < 16):
            data_slice_copy = apply_block_filling_schema(data_slice_copy, 16)

        entrance_state_matrix = make_state_matrix_by_slice([char for char in data_slice_copy])

        exit_state_matrix = execute_process_by_rounds(
            key_schedule,
            entrance_state_matrix,
            exit_state_matrix
        )
        final_ciphered_result.append([word for word in exit_state_matrix])

    if (len(data_slices[-1]) == 16):
        extra_exit_state_matrix: list[list[str]] = []

        extra_exit_state_matrix = execute_process_by_rounds(
            key_schedule,
            EXTRA_BLOCK,
            extra_exit_state_matrix
        )
        final_ciphered_result.append([word for word in extra_exit_state_matrix])

    write_ciphered_result(output_file_path, final_ciphered_result)

def read_file_data(
    input_file_path: str
) -> any:
    with open(input_file_path, 'rb') as data:
        data: bytes = data.read()
        bytes_array: list[bytes] = []

        for byte in data:
            if (str(byte).isdigit()):
                bytes_array.append(hexlify(np.uint8(byte)).decode(UTF_8))
            else:
                bytes_array.append(str(byte))

        return bytes_array

def get_data_slices_to_iterate(
    input_file_path_data: str
) -> list[list[str]]:
    data_slices: list[list[str]] = []

    for index in range(0, len(input_file_path_data), 16):
        data_slices.append(input_file_path_data[index:index + 16])

    return data_slices

def apply_block_filling_schema(
    data_slice: list[str],
    default_block_size: int
) -> str:
    if (default_block_size >= 1 and default_block_size <= 255):
        number_of_missing_bytes: int = default_block_size - len(data_slice)

        for _ in range(number_of_missing_bytes):
            data_slice.append(str(number_of_missing_bytes))

        return data_slice
    else:
        raise Exception("PKCS#7 only accepts blocks from 1 to 255 bytes.")

def make_state_matrix_by_slice(
    data_slice: list[str]
) -> list[list[str]]:
    data_slice_copy: list[str] = data_slice.copy()
    state_matrix: list[list[str]] = []

    for _ in range(4):
        state_matrix_row: list[str] = []

        for byte_index, byte in enumerate(data_slice_copy):
            if (byte_index < 4):
                state_matrix_row.append(byte)
            elif (byte_index >= 4):
                break

        state_matrix.append(state_matrix_row)

        for byte in state_matrix_row:
            data_slice_copy.remove(byte)

    return state_matrix

def execute_process_by_rounds(
    key_schedule: list[list[str]],
    entrance_state_matrix: list[list[str]],
    exit_state_matrix: list[list[str]]
) -> list[list[str]]:
    s_box: list[list[str]] = get_static_s_box()

    exit_state_matrix = apply_round_key_xor(
        entrance_state_matrix,
        key_schedule[0]
    )

    for index in range(10):
        if (index < 9):
            exit_state_matrix = apply_subword_or_subbytes(
                s_box,
                exit_state_matrix
            )
            exit_state_matrix = apply_shift_rows(exit_state_matrix)
            exit_state_matrix = apply_mix_columns(exit_state_matrix)
            exit_state_matrix = apply_round_key_xor(
                exit_state_matrix,
                key_schedule[index + 1]
            )
        elif (index == 9):
            exit_state_matrix = apply_subword_or_subbytes(
                s_box,
                exit_state_matrix
            )
            exit_state_matrix = apply_shift_rows(exit_state_matrix)
            exit_state_matrix = apply_round_key_xor(
                exit_state_matrix,
                key_schedule[index + 1]
            )

    return exit_state_matrix

def apply_round_key_xor(
    entrance_state_matrix: list[list[str]],
    round_key: list[list[str]]
) -> list[list[str]]:
    for index, word in enumerate(entrance_state_matrix):
        for byte_index, byte in enumerate(word):
            xor_result: int = int(byte, 16) ^ int(round_key[index][byte_index], 16)
            word[byte_index] = hexlify(np.uint8(xor_result)).decode(UTF_8)

    return entrance_state_matrix

def apply_shift_rows(
    exit_state_matrix: list[list[str]]
) -> list[list[str]]:
    iteration_counter: int = 0

    for row in range(len(exit_state_matrix)):
        if (iteration_counter == 1):
            break
        iteration_counter += 1

        for column in range(len(exit_state_matrix[row])):
            if ( \
                (row == 0 and column == 0) or \
                (row == 1 and column == 1) or \
                (row == 2 and column == 2) or \
                (row == 3 and column == 3) \
            ):
                pass
            else:
                if (column == 1):
                    first_value: str = exit_state_matrix[0][column]
                    second_value: str = exit_state_matrix[1][column]
                    third_value: str = exit_state_matrix[2][column]
                    fourth_value: str = exit_state_matrix[3][column]

                    exit_state_matrix[0][column] = second_value
                    exit_state_matrix[1][column] = third_value
                    exit_state_matrix[2][column] = fourth_value
                    exit_state_matrix[3][column] = first_value
                elif (column == 2):
                    first_value: str = exit_state_matrix[0][column]
                    second_value: str = exit_state_matrix[1][column]
                    third_value: str = exit_state_matrix[2][column]
                    fourth_value: str = exit_state_matrix[3][column]

                    exit_state_matrix[0][column] = third_value
                    exit_state_matrix[1][column] = fourth_value
                    exit_state_matrix[2][column] = first_value
                    exit_state_matrix[3][column] = second_value
                elif (column == 3):
                    first_value: str = exit_state_matrix[0][column]
                    second_value: str = exit_state_matrix[1][column]
                    third_value: str = exit_state_matrix[2][column]
                    fourth_value: str = exit_state_matrix[3][column]

                    exit_state_matrix[0][column] = fourth_value
                    exit_state_matrix[1][column] = first_value
                    exit_state_matrix[2][column] = second_value
                    exit_state_matrix[3][column] = third_value

    return exit_state_matrix

def apply_mix_columns(
    exit_state_matrix: list[list[str]]
) -> list[list[str]]:
    shift_rows_matrix: list[list[str]] = np.copy(exit_state_matrix)
    l_table: list[list[str]] = get_static_l_table()
    e_table: list[list[str]] = get_static_e_table()

    for index, word in enumerate(exit_state_matrix):
        word_from_shift_rows: list[str] = shift_rows_matrix[index]

        for byte_index, byte in enumerate(word):
            multiplication_matrix_by_byte: list[int] = MULTIPLICATION_MATRIX[byte_index]

            word[byte_index] = get_calculated_byte_from_mix_columns(
                l_table,
                e_table,
                byte,
                word_from_shift_rows,
                multiplication_matrix_by_byte
            )

    return exit_state_matrix

def get_calculated_byte_from_mix_columns(
    l_table: list[list[str]],
    e_table: list[list[str]],
    byte: str,
    word_from_shift_rows: list[str],
    multiplication_matrix_by_byte: list[int]      
) -> str:
    mix_columns_formula: list[int] = []

    for byte_index, byte in enumerate(word_from_shift_rows):
        multiplication_matrix_element: int = multiplication_matrix_by_byte[byte_index]

        if (byte == '00' or multiplication_matrix_element == 0x00):
            mix_columns_formula.append(hex(0))
        elif (byte == '01' or multiplication_matrix_element == 0x01):
            if (byte == '01'):
                mix_columns_formula.append(hex(multiplication_matrix_element))
            elif (multiplication_matrix_element == 0x01):
                mix_columns_formula.append(byte)
        else:
            (galois_first_value, galois_second_value) = get_values_from_l_table(
                l_table,
                byte,
                multiplication_matrix_element
            )
            galois_multiplication_result: int = int(hex(int(galois_first_value, 16) + int(galois_second_value, 16)), 16)

            if (galois_multiplication_result > 0xff):
                galois_multiplication_result -= 0xff

            mix_columns_formula.append(get_value_from_e_table(e_table, galois_multiplication_result))

    mix_columns_formula_first_value: int = mix_columns_formula[0]
    mix_columns_formula_second_value: int = mix_columns_formula[1]
    mix_columns_formula_third_value: int = mix_columns_formula[2]
    mix_columns_formula_fourth_value: int = mix_columns_formula[3]

    mix_columns_formula_result: int = \
        int(mix_columns_formula_first_value, 16) \
        ^ int(mix_columns_formula_second_value, 16) \
        ^ int(mix_columns_formula_third_value, 16) \
        ^ int(mix_columns_formula_fourth_value, 16)

    return hexlify(np.uint8(mix_columns_formula_result)).decode(UTF_8)

def get_values_from_l_table(
    l_table: list[list[str]],
    byte: str,
    multiplication_matrix_element: int
) -> tuple[str, str]:
    multiplication_matrix_element_str: str = hexlify(np.uint8(multiplication_matrix_element)).decode(UTF_8)
    l_table_row_for_byte: str = byte[:1]
    l_table_column_for_byte: str = byte[1:]
    l_table_row_for_multiplication_matrix_element: str = multiplication_matrix_element_str[:1]
    l_table_column_for_multiplication_matrix_element: str = multiplication_matrix_element_str[1:]

    return (
        l_table[int(l_table_row_for_byte, 16) + 1][int(l_table_column_for_byte, 16) + 1],
        l_table[int(l_table_row_for_multiplication_matrix_element, 16) + 1] \
            [int(l_table_column_for_multiplication_matrix_element, 16) + 1]
    )

def get_value_from_e_table(
    e_table: list[list[str]],
    galois_multiplication_result: int
) -> str:
    galois_multiplication_result_str = hexlify(np.uint8(galois_multiplication_result)).decode(UTF_8)
    e_table_row: str = galois_multiplication_result_str[:1]
    e_table_column: str = galois_multiplication_result_str[1:]

    return e_table[int(e_table_row, 16) + 1][int(e_table_column, 16) + 1]

def write_ciphered_result(
    output_file_path: str,
    final_ciphered_result: list[list[str]]
) -> None:
    if (path.exists(output_file_path)):
        with open(output_file_path, 'w') as _:
            pass

    with open(output_file_path, 'ab') as data:
        for exit_state_matrix in final_ciphered_result:
            for word in exit_state_matrix:
                for byte in word:
                    data.write(int(byte, 16).to_bytes())
