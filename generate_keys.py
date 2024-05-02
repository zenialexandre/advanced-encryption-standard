import numpy as np
from binascii import hexlify

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
) -> any:
    state_matrix: list = make_state_matrix(cipher_key_splitted)
    key_schedule: list[list[str]] = get_generated_key_schedule(state_matrix)

    for round_key in key_schedule:
        print(round_key)

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

def get_static_s_box() -> list[list[str]]:
    static_s_box: list[list[int]] = [
        [0xA, 0,     1,    2,   3,    4,    5,    6,    7,    8,    9,   0xa,  0xb,  0xc,  0xd,  0xe,  0xf],
        [0, 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [1, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [2, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [3, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [4, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xA0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [5, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [6, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [7, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [8, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [9, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xa, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xb, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xF4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xc, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0xd, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9d],
        [0xe, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0xf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    ]
    return [[hexlify(bytes([byte])).decode() for byte in row] for row in static_s_box]

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
        directly_previous_word: list[str] = round_key[-1 + index]

        for byte_index, byte in enumerate(directly_previous_word):
            xor_result: int = int(byte, 16) ^ int(equivalent_position_last_round_key_word[byte_index], 16)
            missing_word.append(hexlify(np.uint8(xor_result)).decode())

        round_key.append(missing_word)

    return round_key
