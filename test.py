import numpy as np
import matplotlib.pyplot as plt

# Generate a sample signal
t = np.linspace(0, 1, 1000)  # Time vector
signal = np.sin(2 * np.pi * 5 * t)  # Example signal (sine wave)

# Define the quantization interval
quantization_interval = 0.1

# Quantize the signal
quantized_signal = quantization_interval * np.round(signal / quantization_interval)

# Plot the original and quantized signals
plt.plot(t, signal, label='Original Signal')
plt.plot(t, quantized_signal, label='Quantized Signal', linestyle='--')
plt.legend()
plt.show()
