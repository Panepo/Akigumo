import pyaudio
import numpy as np
import threading
import random
import sys
from components.Generator import SineGenerator
from components.Analyzer import AnalyzeFrequency
from components.Filter import butter_bandpass
from components.Loader import configLoader
from components.Device import setDevice
from scipy.signal import find_peaks

# Parameters
fs = 44100  # Sampling rate

try:
  parameters = configLoader('FreqTest.ini')

  # Duration in seconds
  duration = float(parameters['duration'])

  # Generate random frequency
  freq_min = int(parameters['freq_min']) # Minimum frequency
  freq_max = int(parameters['freq_max']) # Maximum frequency

  # Number of tests
  tests = int(parameters['tests']) * 2
  critria = int(parameters['critria'])

  # Frequency critria
  freq_critria = int(parameters['freq_critria'])
except FileNotFoundError:
  input(f"Error: The config file does not exist.")
  sys.exit(1)
except ValueError:
  input(f"Error: The value in config file has something wrong.")
  sys.exit(1)

setDevice()

def main():
  leftPass = 0 # Number of pass left tests
  rightPass = 0 # Number of pass right tests

  # Initialize PyAudio
  p = pyaudio.PyAudio()

  # Begin tests
  for num in range(0, tests):
    frequency = random.randint(freq_min, freq_max)  # Frequency of the signal

    # Create a stereo signal with the right channel muted
    if (num < tests / 2):
      stereo_signal = SineGenerator(frequency, fs, duration, 0) # Left channel and right channel muted
    else:
      stereo_signal = SineGenerator(frequency, fs, duration, 1) # Right channel and left channel muted

    transmitter = p.open(format=pyaudio.paFloat32, channels=2, rate=fs, output=True)
    receiver = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
    frames = []

    def play_sound():
      transmitter.write(stereo_signal.astype(np.float32).tobytes())
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
    received_signal = np.hstack(frames)

    # Assign a band pass filter
    filterd_signal = butter_bandpass(received_signal, freq_min, freq_max, fs)

    # Decode the signal
    freqs, magnitudes = AnalyzeFrequency(filterd_signal, fs)
    sorted_indices = np.argsort(magnitudes)[::-1]
    peak_freq = abs(freqs[sorted_indices[0]])

    print("=============================================")
    if (num < tests / 2):
      print(f"Left signal frequency: {frequency} Hz")
    else:
      print(f"Right signal frequency: {frequency} Hz")

    if (peak_freq <= frequency + freq_critria and peak_freq >= frequency - freq_critria):
      if (num < tests / 2):
        leftPass = leftPass + 1
      else:
        rightPass = rightPass + 1

      print(f"Detected peak frequency: {peak_freq} Hz PASS")
    else:
      print(f"Detected peak frequency: {peak_freq} Hz")

  p.terminate()
  print(f"Total {tests} tests: left channel {leftPass} pass and right channel {rightPass} pass")
  return leftPass, rightPass

if __name__ == "__main__":
  leftPass, rightPass = main()
  if (leftPass >= critria and rightPass >= critria):
    print(f"Test PASSED")
    sys.exit(0)
  else:
    input(f"Test FAILED")
    sys.exit(1)
