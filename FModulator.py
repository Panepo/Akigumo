import numpy as np
from scipy.signal import hilbert

# Frequency modulation (FM) encoding
def FMencode(message, time, carrier_frequency, sample_frequency, freqency_sensitivity):
  integral_of_message = np.cumsum(message) / sample_frequency
  return np.cos(2 * np.pi * carrier_frequency * time + 2 * np.pi * freqency_sensitivity * integral_of_message)

# Frequency modulation (FM) decoding
def FMdecode(encode_message, sample_frequency, freqency_sensitivity):
  analytic_signal = hilbert(encode_message)
  instantaneous_phase = np.unwrap(np.angle(analytic_signal))
  decoded_message = np.diff(instantaneous_phase) * sample_frequency / (2 * np.pi * freqency_sensitivity)
  return decoded_message
