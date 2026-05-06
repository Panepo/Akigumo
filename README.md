# Akigumo

A speaker and microphone hardware validation tool. It plays sine wave tones through the speaker and records them via the microphone, then analyzes the received signal to verify both audio devices are functioning correctly.

## How It Works

1. **Transmit** — generates a sine wave at a random frequency within a configured range and plays it through the speaker (left or right channel independently).
2. **Receive** — simultaneously records audio from the microphone.
3. **Analyze** — applies a band-pass filter to the recorded signal and performs FFT analysis to detect whether the correct frequency was received at sufficient power.
4. **Pass / Fail** — each test is evaluated against configurable frequency and power thresholds. Results are aggregated across all tests and channels.

An ambient noise baseline is measured before testing begins to calibrate the power threshold dynamically.

## Entry Points

| Script | Description |
|---|---|
| `FreqTest.py` | Single test run — plays tones on left and right channels, reports pass/fail per channel. |
| `FreqTestOne.py` | Single test run, simplified single-file version. |
| `FreqTestGroup.py` | Scheduled repeated test runs using `schedule`. Runs the full test suite at a fixed interval and reports cumulative group pass rate. |
| `FreqTestGroupOne.py` | Group test, simplified single-file version. |
| `FMTest.py` | FM-modulated data transmission test over real audio hardware (speaker → microphone). |
| `FMConsole.py` | FM modulation/demodulation simulation with waveform plots (no hardware, console only). |
| `FMConsoleMic.py` | FM modulation over real hardware with waveform plots. |

## Configuration

All tunable parameters live in `FreqTest.ini`:

```ini
# Number of tests per channel
tests = 5
critria = 3          # Minimum passes required
group = 1000         # Number of group iterations (FreqTestGroup only)

# Frequency range for generated tones (Hz)
freq_min = 18000
freq_max = 22000

# Test duration in seconds
duration = 0.5

# Pass criteria
freq_critria = 10              # Allowed frequency error (Hz)
power_critria_scale = 2        # Ambient power multiplier for threshold
power_critria_const = 10       # Constant added to power threshold
```

## Components

| Module | Responsibility |
|---|---|
| `components/Generator.py` | Sine wave generation |
| `components/Analyzer.py` | FFT-based frequency and power analysis |
| `components/Filter.py` | Butterworth band-pass / high-pass filters |
| `components/Device.py` | PyAudio stream management, Windows volume control via pycaw |
| `components/Loader.py` | INI config file loader |
| `components/Modulator.py` | PCM encoding/decoding, FM modulation/demodulation |
| `components/Normalizer.py` | Signal normalization |
| `components/Quantizer.py` | Amplitude and time quantization |
| `components/SNR.py` | Signal-to-noise ratio utilities |

## Requirements

- Python 3.x
- Windows (pycaw is used for volume control)

Install dependencies:

```bash
pip install -r requirements.txt
```

Key dependencies: `pyaudio`, `numpy`, `scipy`, `matplotlib`, `pycaw`, `altgraph`, `cffi`, `schedule`.

## Usage

```bash
# Run a single frequency sweep test
python FreqTest.py

# Run repeated group tests on a schedule
python FreqTestGroup.py

# Run FM data transmission test over hardware
python FMTest.py
```

> **Note:** The scripts automatically set speaker volume to 100% and microphone gain to an appropriate level before testing. Run with appropriate permissions if volume control fails.
