import numpy as np

# Pulse width modulation (PWM) encoding binary
def PWMencode(binary_array, sample_frequency, modulating_frequency):
    signal = np.array(binary_array)
    return np.repeat(signal, sample_frequency // modulating_frequency)

# Pulse width modulation (PWM) decoding binary
def PWMdecode(signal, sample_frequency, modulating_frequency):
    signal = signal[::sample_frequency // modulating_frequency]
    return [int(bit) for bit in signal]

# Pulse width modulation (PWM) encoding string
def PWMencodeString(string, sample_frequency, modulating_frequency):
    binary_string = ''.join(format(ord(char), '08b') for char in string)
    signal = np.array([int(bit) for bit in binary_string])
    signal = np.repeat(signal, sample_frequency // modulating_frequency)
    return signal

# Pulse width modulation (PWM) decoding string
def PWMdecodeString(signal, sample_frequency, modulating_frequency):
    signal = signal[::sample_frequency // modulating_frequency]
    binary_string = ''.join(str(int(bit)) for bit in signal)
    return ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
