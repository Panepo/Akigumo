import numpy as np

def normalize(input):
  return (input - np.min(input)) / (np.max(input) - np.min(input))
