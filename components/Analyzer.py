import numpy as np
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

def AnalyzeSignal(signal, fs: int):
  # Compute the FFT
  N = len(signal)
  yf = fft(signal)
  xf = fftfreq(N, 1/fs)[:N//2]

  # Compute the Power Spectral Density (PSD)
  psd = 2.0/N * np.abs(yf[:N//2])

  # Find the peaks in the PSD
  peaks, _ = find_peaks(psd)

  # Get the peak frequencies and their power
  peak_freqs = xf[peaks]
  peak_powers = psd[peaks]

  # Sort peaks by power
  sorted_indices = np.argsort(peak_powers)[::-1]
  peak_freqs = peak_freqs[sorted_indices]
  peak_powers = peak_powers[sorted_indices]

  return peak_freqs, peak_powers
