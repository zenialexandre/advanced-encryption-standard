import numpy as np

def expand_keys(cipher_key_splitted: list[str]):
    state_matrix: list = make_state_matrix(cipher_key_splitted)
    print(state_matrix)

def make_state_matrix(cipher_key_splitted) -> list[list[str]]:
    state_matrix: list[list[str]] = []

    for line in range(0, 16, 4):
        state_matrix.append(cipher_key_splitted[line: line + 4])

    return state_matrix

def generate_round_keys(state_matrix):
    round_keys = []
