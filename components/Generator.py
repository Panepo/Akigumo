import numpy as np

# sine wave generator
def SineGenerator(frequency: int, fs: int, duration: int, channel = -1):
  t = np.linspace(0, duration, int(fs * duration), endpoint=False)
  signal = 0.5 * np.sin(2 * np.pi * frequency * t)

  # Stereo signal
  if (channel == 0):
    stereo_signal = np.zeros((len(signal), 2))
    stereo_signal[:, 0] = signal  # Left channel
    stereo_signal[:, 1] = 0  # Right channel (muted)
    return stereo_signal
  elif (channel == 1):
    stereo_signal = np.zeros((len(signal), 2))
    stereo_signal[:, 0] = 0  # Left channel (muted)
    stereo_signal[:, 1] = signal  # Right channel (muted)
    return stereo_signal
  else:
    return signal

