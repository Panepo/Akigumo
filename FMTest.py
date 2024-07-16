import pyaudio
import numpy as np
import threading
import random
import sys
from components.Modulator import PCMencode, PCMdecode, FMencode, FMdecode

# Define the parameters
fs: int = 44100  # Sampling frequency
fc: int = 1000   # Carrier frequency
fm: int = 10     # Modulating frequency
kf: int = 50     # Frequency sensitivity
length = 10      # Length of bit send
tests = 10       # Number of tests

def main():
  passes = 0

  # Initialize PyAudio
  p = pyaudio.PyAudio()

  # Begin tests
  for num in range(0, tests):
    input = np.random.randint(2, size=length)
    duration = len(input) / fm
    message = PCMencode(input, fs, fm)
    t = np.arange(0, len(message)) / fs
    encode_message = FMencode(message, t, fc, fs, kf)

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

    decoded_message = FMdecode(signal, fs, kf)
    output = PCMdecode(decoded_message > 0, fs, fm)

    equals = 0
    for i in range(0, length):
      if (input[i] == output[i]):
        equals = equals + 1

    # Print the input and output strings
    print(f"Input string: {input} Output string: {output} {equals} bit match")

    if (equals >= 9):
      passes = passes + 1

  p.terminate()
  print(f"Total {tests} tests with {passes} pass")
  return passes

if __name__ == "__main__":
  passes = main()
  if (passes <= 6):
    input(f"Test FAILED")
    sys.exit(1)
  else:
    print(f"Test PASSED")
    sys.exit(0)
