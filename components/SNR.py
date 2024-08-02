import numpy as np
from scipy.io import wavfile
from math import log10, sqrt

def SNR(original, received):
  signal_power = np.mean(original ** 2)
  noise_power = np.mean((original - received) ** 2)
  snr = 10 * np.log10(signal_power / noise_power)
  return snr

def PSNR(original, compressed):
  mse = np.mean((original - compressed) ** 2)
  if mse == 0:  # MSE is zero means no noise is present in the signal.
      return 100
  max_pixel = np.max(original)
  psnr = 20 * log10(max_pixel / sqrt(mse))
  return psnr
