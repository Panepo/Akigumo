import numpy as np
import matplotlib.pyplot as plt
from FModulator import FMencode, FMdecode
from PWModulator import PWMencode, PWMdecode
from Normalizer import normalize

# Define the parameters
fs = 1000  # Sampling frequency
fc = 100   # Carrier frequency
fm = 10    # Modulating frequency
kf = 50  # Frequency sensitivity
input = [1, 0, 1, 1, 0, 0, 1, 0]

message = PWMencode(input, fs, fm)
t = np.arange(0, len(message)) / fs
encode_message = FMencode(message, t, fc, fs, kf)
decoded_message = FMdecode(encode_message, fs, kf)
normalized_message = normalize(decoded_message)
output = PWMdecode(normalized_message > 0, fs, fm)

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
plt.plot(t[1:], decoded_message)
plt.title('Decoded Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 4)
plt.plot(t[1:], normalized_message)
plt.title('Normalized Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
