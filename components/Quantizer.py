import numpy as np

def AmplitudeQuantizer(input, high: int, low: int):
  cutoff = (high - low) // 2
  return np.where(input > cutoff, high, low)

