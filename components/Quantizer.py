import numpy as np

def AmplitudeQuantizer(signal, highcut: int, lowcut: int):
  cutoff = (highcut - lowcut) / 2
  return np.where(signal > cutoff, highcut, lowcut)

def TimeQuantizer(signal, highcut: int, lowcut: int, period: int):
  num_periods = len(signal) // period
  result = np.zeros_like(signal)

  cutoff = (highcut - lowcut) / 2

  for i in range(num_periods):
    start_idx = i * period
    end_idx = start_idx + period
    avg = np.mean(signal[start_idx:end_idx])
    if avg > cutoff:
        result[start_idx:end_idx] = highcut
    else:
        result[start_idx:end_idx] = lowcut

  return result
