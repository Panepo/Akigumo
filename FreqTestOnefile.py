import pyaudio
import numpy as np
import threading
import random
import sys
import math
from scipy.signal import butter, lfilter, find_peaks
from scipy.fft import fft, fftfreq
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import traceback

def configLoader(file_path):
    parameters = {}
    try:
      with open(file_path, 'r') as file:
          for line in file:
              if line.strip() and not line.strip().startswith('#'):
                key, value = line.strip().split(' = ')
                parameters[key] = value
      return parameters
    except FileNotFoundError:
      raise FileNotFoundError
    except ValueError:
      raise ValueError

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

  # Power critria
  power_critria_scale = int(parameters['power_critria_scale'])
  power_critria_const = int(parameters['power_critria_const'])

except FileNotFoundError:
  input(f"Error: The config file does not exist.")
  sys.exit(1)
except ValueError:
  input(f"Error: The value in config file has something wrong.")
  sys.exit(1)
except Exception as e:
  # Print the full traceback
  traceback.print_exc()
  input("Error: The config file has something wrong.")
  sys.exit(1)

try:
  # Get default audio device
  speakers = AudioUtilities.GetSpeakers()
  speakerInterface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
  volumeSpeaker = speakerInterface.QueryInterface(IAudioEndpointVolume)
  volumeSpeaker.SetMute(False, None)
  volumeSpeaker.SetMasterVolumeLevelScalar(1.0, None)

  microphones = AudioUtilities.GetMicrophone()
  micInterface = microphones.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
  volumeMic = micInterface.QueryInterface(IAudioEndpointVolume)
  _, max_volume, _ = volumeMic.GetVolumeRange()
  volumeMic.SetMute(False, None)
  if (max_volume >= 25):
    volumeMic.SetMasterVolumeLevel(25, None)
  else:
    volumeMic.SetMasterVolumeLevelScalar(1.0, None)
except IOError:
  input("No default audio device available.")
  sys.exit(1)
except Exception as e:
  # Print the full traceback
  traceback.print_exc()
  input("Error: Audio devices has something wrong.")
  sys.exit(1)

# sine wave generator
def SineGenerator(power: float, frequency: int, fs: int, duration: int):
  t = np.linspace(0, duration, int(fs * duration), endpoint=False)
  signal = power * np.sin(2 * np.pi * frequency * t)
  return signal

def AnalyzeSignal(signal, fs: int):
  # Compute the FFT
  N = len(signal)
  yf = fft(signal)
  xf = fftfreq(N, 1/fs)[:N//2]

  # Compute the Power Spectral Density (PSD)
  psd = 2.0/N * np.abs(yf[:N//2])

  # Find the peaks in the PSD
  peaks, _ = find_peaks(psd)

  # Get the peak frequencies and their power
  peak_freqs = xf[peaks]
  peak_powers = psd[peaks]

  # Sort peaks by power
  sorted_indices = np.argsort(peak_powers)[::-1]
  peak_freqs = peak_freqs[sorted_indices]
  peak_powers = peak_powers[sorted_indices]

  return peak_freqs, peak_powers

def butter_bandpass(data, lowcut: int, highcut: int, fs: int, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def main():
  leftPass = 0 # Number of pass left tests
  rightPass = 0 # Number of pass right tests

  # Initialize PyAudio
  p = pyaudio.PyAudio()

  # Get ambient noise
  print("Get ambient noise...")
  receiver = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
  frames = []

  for _ in range(0, int(fs / 1024 * duration * 5)):
    data = receiver.read(1024)
    frames.append(np.frombuffer(data, dtype=np.int16))

  receiver.stop_stream()
  receiver.close()

  # Convert frames to numpy array
  received_signal = np.hstack(frames)

  # Assign a band pass filter
  filterd_signal = butter_bandpass(received_signal, freq_min, freq_max, fs)

  # Decode the signal and get critria
  peak_freqs, peak_powers = AnalyzeSignal(filterd_signal, fs)
  power_critria = math.floor((peak_powers[0]) * power_critria_scale) + power_critria_const

  # Begin tests
  for num in range(0, tests):
    freq = random.randint(freq_min, freq_max)  # Frequency of the signal 1
    sine = SineGenerator(1, freq, fs, duration)

    # Create a stereo signal
    stereo_signal = np.zeros((len(sine), 2))
    if (num < tests / 2):
      stereo_signal[:, 0] = sine  # Left channel
      stereo_signal[:, 1] = 0  # Right channel (muted)
    else:
      stereo_signal[:, 0] = 0  # Left channel (muted)
      stereo_signal[:, 1] = sine  # Right channel

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
    peak_freqs, peak_powers = AnalyzeSignal(filterd_signal, fs)

    print("=============================================")
    if (num < tests / 2):
      print(f"Left signal frequency: {freq} Hz, power critria: {power_critria}")
    else:
      print(f"Right signal frequency: {freq} Hz, power critria: {power_critria}")

    if (peak_freqs[0] <= freq + freq_critria and peak_freqs[0] >= freq - freq_critria):
      if (peak_powers[0] >= power_critria):
        print(f"Detected Peak Frequency: {math.floor(peak_freqs[0])} Hz, Power: {math.floor(peak_powers[0])} PASS")
        if (num < tests / 2):
          leftPass = leftPass + 1
        else:
          rightPass = rightPass + 1
      else:
        print(f"Detected Peak Frequency: {math.floor(peak_freqs[0])} Hz, Power: {math.floor(peak_powers[0])}")
    else:
      print(f"Detected Peak Frequency: {math.floor(peak_freqs[0])} Hz, Power: {math.floor(peak_powers[0])}")

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

