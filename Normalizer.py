import numpy as np

def normalize(input):
  normal = (input - np.min(input)) / (np.max(input) - np.min(input))
  return np.where(normal > 0.5, 1, 0)
