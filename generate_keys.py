import numpy as np

def expand_keys(
    cipher_key_splitted: list[str]
) -> any:
    state_matrix: list = make_state_matrix(cipher_key_splitted)
    key_schedule: list[list[str]] = get_generated_key_schedule(state_matrix)

def make_state_matrix(
    cipher_key_splitted: list[str]
) -> list[list[str]]:
    state_matrix: list[list[str]] = []

    for line in range(0, 16, 4):
        state_matrix.append(cipher_key_splitted[line: line + 4])

    return state_matrix

def get_generated_key_schedule(
    state_matrix: list[list[str]]
) -> list[list[str]]:
    # Isso deveria estar dentro de um for range(10) = 10 round_keys, cada uma com 4 words
    round_key: list[list[str]] = get_round_key_with_rotated_words(state_matrix)

def get_round_key_with_rotated_words(
    state_matrix: list[list[str]]
) -> list[list[str]]:
    for index, word in enumerate(state_matrix):
        state_matrix[index] = np.roll(word, -1).tolist()

    return state_matrix
