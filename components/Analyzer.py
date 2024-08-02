import numpy as np

def AnalyzeFrequency(signal, fs: int):
  fft_result = np.fft.fft(signal)
  freqs = np.fft.fftfreq(len(fft_result), 1/fs)
  magnitudes = np.abs(fft_result)
  return freqs, magnitudes
