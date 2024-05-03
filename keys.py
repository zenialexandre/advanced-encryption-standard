import numpy as np
from binascii import hexlify
from utils import get_static_s_box

'''
    REMINDER: The Words of the RoundKeys are oriented as rows.
    [[word], [word], [word], [word]]
'''

ROUND_CONSTANT_TABLE: dict = {
    1: 0x01,
    2: 0x02,
    3: 0x04,
    4: 0x08,
    5: 0x10,
    6: 0x20,
    7: 0x40,
    8: 0x80,
    9: 0x1b,
    10: 0x36
}

def expand_keys(
    cipher_key_splitted: list[str]
) -> list[list[str]]:
    state_matrix: list = make_state_matrix(cipher_key_splitted)
    return get_generated_key_schedule(state_matrix)

def make_state_matrix(
    cipher_key_splitted: list[str]
) -> list[list[str]]:
    state_matrix: list[list[str]] = []

    for row in range(0, 16, 4):
        state_matrix.append(cipher_key_splitted[row: row + 4])

    return state_matrix

def get_generated_key_schedule(
    state_matrix: list[list[str]]
) -> list[list[str]]:
    state_matrix_as_hexadecimal: list[list[str]] = get_converted_to_hexadecimal(state_matrix)
    key_schedule: list[list[str]] = []
    s_box: list[list[str]] = get_static_s_box()

    key_schedule.append(state_matrix_as_hexadecimal)

    for index in range(10):
        key_schedule.append(get_round_key(index + 1, key_schedule, s_box))

    return key_schedule

def get_converted_to_hexadecimal(
    round_key: list[list[str]]
) -> list[list[str]]:
    return [[hexlify(np.uint8(byte)).decode() for byte in word] for word in round_key]

def get_round_key(
    index: int,
    key_schedule: list[list[str]],
    s_box: list[list[str]]
) -> list[list[str]]:
    first_word_last_round_key: list[str] = key_schedule[-1][-4]
    round_key: list[list[str]] = []
    round_constant: list[str] = get_generated_round_constant(index)

    # Modifying the first word of the round_key:
    round_key.append(key_schedule[-1][-1])
    round_key = apply_rotword(round_key)
    round_key = apply_subword(s_box, round_key)
    round_key = apply_generic_first_word_xor(round_key, round_constant)
    round_key = apply_generic_first_word_xor(round_key, first_word_last_round_key)

    # Getting the other words of the round_key
    round_key = get_round_key_missing_words_by_xor(key_schedule, round_key)

    return round_key

def apply_rotword(
    round_key: list[list[str]]
) -> list[list[str]]:
    for index, word in enumerate(round_key):
        round_key[index] = np.roll(word, -1).tolist()

    return round_key

def apply_subword(
    s_box: list[list[str]],
    round_key: list[list[str]]
) -> list[str]:
    for index, word in enumerate(round_key):
        for byte_index, byte in enumerate(word):
            byte_as_str: str = hexlify(bytes.fromhex(byte)).decode();
            s_box_row: str = byte_as_str[:1];
            s_box_column: str = byte_as_str[1:];

            word[byte_index] = s_box[int(s_box_row, 16) + 1][int(s_box_column, 16) + 1]
        
        round_key[index] = word

    return round_key

def get_generated_round_constant(
    index: int
) -> list[str]:
    round_constant: list[str] = []
    round_constant.append(hexlify(np.uint8(ROUND_CONSTANT_TABLE[index])).decode())
    for _ in range(3): round_constant.append(hexlify(np.uint8(0)).decode())

    return round_constant

def apply_generic_first_word_xor(
    round_key: list[list[str]],
    generic_word: list[str]
) -> list[list[str]]:
    for word in round_key:
        for byte_index, byte in enumerate(word):
            xor_result: int = int(byte, 16) ^ int(generic_word[byte_index], 16)
            word[byte_index] = hexlify(np.uint8(xor_result)).decode()

    return round_key

def get_round_key_missing_words_by_xor(
    key_schedule: list[list[str]],
    round_key: list[list[str]]
) -> list[list[str]]:
    for index in range(3):
        missing_word: list[str] = []
        equivalent_position_last_round_key_word: list[str] = key_schedule[-1][-4 + index]
        directly_previous_word: list[str] = round_key[-1]

        for byte_index, byte in enumerate(directly_previous_word):
            xor_result: int = int(byte, 16) ^ int(equivalent_position_last_round_key_word[byte_index], 16)
            missing_word.append(hexlify(np.uint8(xor_result)).decode())

        round_key.append(missing_word)

    return round_key
