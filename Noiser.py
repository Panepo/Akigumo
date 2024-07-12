import numpy as np

def noise(input, noise_strength: float, shift_strength: int):
  noised_input = input + np.random.normal(0, noise_strength, input.shape)
  shift_first = noised_input[:shift_strength]
  shift_last = noised_input[shift_strength:]
  return np.concatenate((shift_first, shift_last), axis=0)
