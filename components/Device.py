from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import traceback

def setDevice():
  try:
    # Get default audio device
    speakers = AudioUtilities.GetSpeakers()
    speakerInterface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeSpeaker = cast(speakerInterface, POINTER(IAudioEndpointVolume))
    #volumeSpeaker.SetMute(False, None)
    volumeSpeaker.SetMasterVolumeLevelScalar(1.0, None)

    microphones = AudioUtilities.GetMicrophone()
    micInterface = microphones.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeMic = cast(micInterface, POINTER(IAudioEndpointVolume))
    volumeMic.SetMute(False, None)
    volumeMic.SetMasterVolumeLevelScalar(1.0, None)
  except IOError:
    input("No default audio device available.")
  except Exception as e:
    # Print the full traceback
    traceback.print_exc()
    input("Error: Audio devices has something wrong.")
