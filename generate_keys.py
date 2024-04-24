import numpy as np

def expand_keys(key_arr):
    state_matrix = make_state_matrix()

    pass

def make_state_matrix(key_arr):
    state_matrix = []

    for line in range(0, 16, 4):
        state_matrix.append(key_arr[line:line+4])

    return state_matrix
    
def generate_round_keys(state_matrix):
    round_keys = []
