import numpy as np

def normalize(input, period: int):
  normalized_input = (input - np.min(input)) / (np.max(input) - np.min(input))
  quantized_input = np.where(normalized_input > 0.5, 1, 0)

  num_periods = len(input) // period
  result = np.zeros_like(input)

  for i in range(num_periods):
    start_idx = i * period
    end_idx = start_idx + period
    avg = np.mean(quantized_input[start_idx:end_idx])
    if avg > 0.5:
        result[start_idx:end_idx] = 1
    else:
        result[start_idx:end_idx] = 0

  return result
