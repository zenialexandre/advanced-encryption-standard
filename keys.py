import numpy as np
from binascii import hexlify
from constants import UTF_8
from utils import \
    get_static_s_box, \
    make_state_matrix, \
    get_converted_to_hexadecimal, \
    apply_subword_or_subbytes

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
    state_matrix: list[list[str]] = make_state_matrix(cipher_key_splitted)
    print(state_matrix)
    return get_generated_key_schedule(state_matrix)

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
    round_key = apply_subword_or_subbytes(s_box, round_key)
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

def get_generated_round_constant(
    index: int
) -> list[str]:
    round_constant: list[str] = []
    round_constant.append(hexlify(np.uint8(ROUND_CONSTANT_TABLE[index])).decode(UTF_8))
    for _ in range(3): round_constant.append(hexlify(np.uint8(0)).decode(UTF_8))

    return round_constant

def apply_generic_first_word_xor(
    round_key: list[list[str]],
    generic_word: list[str]
) -> list[list[str]]:
    for word in round_key:
        for byte_index, byte in enumerate(word):
            xor_result: int = int(byte, 16) ^ int(generic_word[byte_index], 16)
            word[byte_index] = hexlify(np.uint8(xor_result)).decode(UTF_8)

    return round_key

def get_round_key_missing_words_by_xor(
    key_schedule: list[list[str]],
    round_key: list[list[str]]
) -> list[list[str]]:
    for index in range(3):
        missing_word: list[str] = []
        equivalent_position_last_round_key_word: list[str] = key_schedule[-1][index + 1]
        directly_previous_word: list[str] = round_key[-1]

        for byte_index, byte in enumerate(directly_previous_word):
            xor_result: int = int(byte, 16) ^ int(equivalent_position_last_round_key_word[byte_index], 16)
            missing_word.append(hexlify(np.uint8(xor_result)).decode(UTF_8))

        round_key.append(missing_word)

    return round_key
