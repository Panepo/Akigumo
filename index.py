import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import threading
from FModulator import FMencode, FMdecode
from PWModulator import PWMencode, PWMdecode
from Normalizer import normalize

# Define the parameters
fs: int = 1000  # Sampling frequency
fc: int = 100   # Carrier frequency
fm: int = 10    # Modulating frequency
kf: int = 50    # Frequency sensitivity
input: list[int] = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
duration: int = len(input) * fm / fc

message = PWMencode(input, fs, fm)
t = np.arange(0, len(message)) / fs
encode_message = FMencode(message, t, fc, fs, kf)

def play_sound():
    sd.play(encode_message, fs)
    sd.wait()

def record_sound(duration, result_container):
    print("Recording...")
    recorded_audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Recording finished")
    result_container.append(recorded_audio)

recorded_audio_container = []
play_thread = threading.Thread(target=play_sound)
record_thread = threading.Thread(target=record_sound, args=(duration, recorded_audio_container))

# Start the threads
play_thread.start()
record_thread.start()

# Wait for both threads to finish
play_thread.join()
record_thread.join()

# Process the recorded audio as needed
recorded_audio = np.zeros_like(t)
for i in range(len(recorded_audio_container[0])):
  recorded_audio[i] = recorded_audio_container[0][i]

decoded_message = FMdecode(recorded_audio, fs, kf)
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
plt.plot(t, recorded_audio)
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
