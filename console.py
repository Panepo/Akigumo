import numpy as np
import matplotlib.pyplot as plt
from FModulator import FMencode, FMdecode
from PWModulator import PWMencode, PWMdecode
from Normalizer import normalize
from Noiser import noise

# Define the parameters
fs: int = 1000  # Sampling frequency
fc: int = 100   # Carrier frequency
fm: int = 10    # Modulating frequency
kf: int = 50    # Frequency sensitivity
input: list[int] = [1, 0, 1, 1, 0, 0, 1, 0]
noise_strength: float = 0.05
shift_strength: int = 8

message = PWMencode(input, fs, fm)
t = np.arange(0, len(message)) / fs
encode_message = FMencode(message, t, fc, fs, kf)
noised_message = noise(encode_message, noise_strength, shift_strength)
decoded_message = FMdecode(noised_message, fs, kf)
normalized_message = normalize(decoded_message, int(fs / fm))
output = PWMdecode(normalized_message > 0, fs, fm)

# Print the input and output strings
print(f"Input string: {input}")
print(f"Output string: {output}")

# Plot the results
plt.figure(figsize=(12, 8))

plt.subplot(5, 1, 1)
plt.plot(t, message)
plt.title('Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(5, 1, 2)
plt.plot(t, encode_message)
plt.title('FM Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(5, 1, 3)
plt.plot(t, noised_message)
plt.title('Noised Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(5, 1, 4)
plt.plot(t[1:], decoded_message)
plt.title('Decoded Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(5, 1, 5)
plt.plot(t[1:], normalized_message)
plt.title('Normalized Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
