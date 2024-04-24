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
    round_keys = []
