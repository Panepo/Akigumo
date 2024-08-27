import pyaudio
import numpy as np
import threading
import queue
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import traceback

def setDevice(setMute: bool):
  try:
    # Get default audio device
    speakers = AudioUtilities.GetSpeakers()
    speakerInterface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeSpeaker = speakerInterface.QueryInterface(IAudioEndpointVolume)
    if (setMute): volumeSpeaker.SetMute(False, None)
    volumeSpeaker.SetMasterVolumeLevelScalar(1.0, None)

    microphones = AudioUtilities.GetMicrophone()
    micInterface = microphones.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeMic = micInterface.QueryInterface(IAudioEndpointVolume)
    _, max_volume, _ = volumeMic.GetVolumeRange()
    if (setMute): volumeMic.SetMute(False, None)

    if (max_volume >= 25):
      volumeMic.SetMasterVolumeLevel(25, None)
    else:
      volumeMic.SetMasterVolumeLevelScalar(1.0, None)
  except IOError:
    input("No default audio device available.")
  except Exception as e:
    # Print the full traceback
    traceback.print_exc()
    input("Error: Audio devices has something wrong.")

def setMute():
  try:
    # Get default audio device
    speakers = AudioUtilities.GetSpeakers()
    speakerInterface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeSpeaker = speakerInterface.QueryInterface(IAudioEndpointVolume)
    volumeSpeaker.SetMute(True, None)

  except IOError:
    input("No default audio device available.")
  except Exception as e:
    # Print the full traceback
    traceback.print_exc()
    input("Error: Audio devices has something wrong.")

def setTotalMute():
  try:
    # Get default audio device
    speakers = AudioUtilities.GetSpeakers()
    speakerInterface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeSpeaker = speakerInterface.QueryInterface(IAudioEndpointVolume)
    volumeSpeaker.SetMute(True, None)
    volumeSpeaker.SetMasterVolumeLevelScalar(0.0, None)

  except IOError:
    input("No default audio device available.")
  except Exception as e:
    # Print the full traceback
    traceback.print_exc()
    input("Error: Audio devices has something wrong.")

def ListenSound(p, fs, duration):
  receiver = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
  frames = []

  for _ in range(0, int(fs / 1024 * duration * 5)):
    data = receiver.read(1024)
    frames.append(np.frombuffer(data, dtype=np.int16))

  receiver.stop_stream()
  receiver.close()

  # Convert frames to numpy array
  received_signal = np.hstack(frames)
  return received_signal

def PlaySound(p, fs, signal):
  transmitter = p.open(format=pyaudio.paFloat32, channels=2, rate=fs, output=True)
  transmitter.write(signal.astype(np.float32).tobytes())
  transmitter.stop_stream()
  transmitter.close()

def ListenSoundThread(q, p, fs, duration):
  receiver = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
  frames = []

  for _ in range(0, int(fs / 1024 * duration * 5)):
    data = receiver.read(1024)
    frames.append(np.frombuffer(data, dtype=np.int16))

  receiver.stop_stream()
  receiver.close()

  # Convert frames to numpy array
  received_signal = np.hstack(frames)
  q.put(received_signal)

def PlayAndListenSound(p, fs, signal, duration):
  q = queue.Queue()
  play_thread = threading.Thread(target=PlaySound, args=(p, fs, signal))
  record_thread = threading.Thread(target=ListenSoundThread, args=(q, p, fs, duration))

  # Start the threads
  play_thread.start()
  record_thread.start()

  # Wait for both threads to finish
  play_thread.join()
  record_thread.join()

  return q.get()
