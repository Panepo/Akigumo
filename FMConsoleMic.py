import pyaudio
import threading
import numpy as np
import matplotlib.pyplot as plt
from components.Modulator import PCMencode, PCMdecode, FMencode, FMdecode
from components.Normalizer import normalize
from components.Quantizer import AmplitudeQuantizer
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

# Initialize PyAudio
p = pyaudio.PyAudio()

transmitter = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
receiver = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
frames = []

def play_sound():
  transmitter.write(encode_message.astype(np.float32).tobytes())
  transmitter.stop_stream()
  transmitter.close()

def record_sound():
  for _ in range(0, int(fs / 1024 * duration)):
      data = receiver.read(1024)
      frames.append(np.frombuffer(data, dtype=np.int16))

  receiver.stop_stream()
  receiver.close()

play_thread = threading.Thread(target=play_sound)
record_thread = threading.Thread(target=record_sound)

# Start the threads
play_thread.start()
record_thread.start()

# Wait for both threads to finish
play_thread.join()
record_thread.join()

# Convert frames to numpy array
signal = np.hstack(frames)

filtered_signal = butter_bandpass(signal, 19000, 21000, fs)
decoded_signal = FMdecode(filtered_signal, fs, kf)
normalized_signal = normalize(decoded_signal)
quantized_signal = AmplitudeQuantizer(normalized_signal, 1, 0)
output = PCMdecode(quantized_signal > 0, fs, fm)

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
plt.plot(t[69:], decoded_signal)
plt.title('Decoded Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 4)
plt.plot(t[69:], quantized_signal)
plt.title('Normalized Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
