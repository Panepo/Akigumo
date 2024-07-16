import numpy as np
from scipy.signal import hilbert

# Pulse Code modulation (PCM) encoding binary
def PCMencode(binary_array: list[int], fs: int, fm: int):
    signal = np.array(binary_array)
    return np.repeat(signal, fs // fm)

# Pulse Code modulation (PCM) decoding binary
def PCMdecode(signal, fs: int, fm: int):
    signal = signal[::fs // fm]
    return [int(bit) for bit in signal]

# Pulse Code modulation (PCM) encoding string
def PCMencodeString(string: str, fs: int, fm: int):
    binary_string = ''.join(format(ord(char), '08b') for char in string)
    signal = np.array([int(bit) for bit in binary_string])
    signal = np.repeat(signal, fs // fm)
    return signal

# Pulse Code modulation (PCM) decoding string
def PCMdecodeString(string: str, fs: int, fm: int):
    string = string[::fs // fm]
    binary_string = ''.join(str(int(bit)) for bit in string)
    return ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))

# Frequency modulation (FM) encoding
def FMencode(message, time, fc, fs, kf):
  integral_of_message = np.cumsum(message) / fs
  return np.cos(2 * np.pi * fc * time + 2 * np.pi * kf * integral_of_message)

# Frequency modulation (FM) decoding
def FMdecode(encode_message, fs, kf):
  analytic_signal = hilbert(encode_message)
  instantaneous_phase = np.unwrap(np.angle(analytic_signal))
  decoded_message = np.diff(instantaneous_phase) * fs / (2 * np.pi * kf)
  return decoded_message
