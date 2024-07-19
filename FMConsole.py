import numpy as np
import matplotlib.pyplot as plt
from components.Modulator import PCMencode, PCMdecode, FMencode, FMdecode
from components.Normalizer import normalize
from components.Quantizer import AmplitudeQuantizer, TimeQuantizer
from components.Filter import butter_bandpass

# Define the parameters
fs: int = 44100  # Sampling frequency
fc: int = 20000  # Carrier frequency
fm: int = 10     # Modulating frequency
kf: int = 50     # Frequency sensitivity
length = 10      # Length of bit send

input = np.random.randint(2, size=length)
duration = len(input) / fm
message = PCMencode(input, fs, fm)
t = np.arange(0, len(message)) / fs
encode_message = FMencode(message, t, fc, fs, kf)

filtered_signal = butter_bandpass(encode_message, 19000, 21000, fs)
decoded_signal = FMdecode(encode_message, fs, kf)
normalized_signal = normalize(decoded_signal)
quantized_signal = AmplitudeQuantizer(normalized_signal, 1, 0)
quantized_signal2 = TimeQuantizer(quantized_signal, 1, 0, fs // fm)
output = PCMdecode(quantized_signal2 > 0, fs, fm)

# Print the input and output strings
print(f"Input string: {input}")
print(f"Output string: {output}")

# Plot the results
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(t, message)
plt.title('Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 2)
plt.plot(t, encode_message)
plt.title('FM Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 3)
plt.plot(t[1:], decoded_signal)
plt.title('Decoded Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 4)
plt.plot(t[1:], quantized_signal2)
plt.title('Normalized Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
