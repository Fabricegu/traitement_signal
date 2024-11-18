import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, firwin

# Paramètres communs
fs = 48000  # Fréquence d'échantillonnage en Hz
duration = 0.05  # Durée du signal en secondes
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Fonction pour générer une sinusoïde avec une fréquence et une phase spécifiée
def generate_sine_wave(frequency, phase_degree, sampling_rate, duration):
    phase_radians = np.deg2rad(phase_degree)
    return np.sin(2 * np.pi * frequency * t + phase_radians)

# Caractéristiques des sinusoïdes (incluant celle de 120 Hz avec phase 0° en début)
sinusoids = [
    (120, 0),
    (260, 45),
    (1080, 10),
    (4120, 0),
    (440, 90),
    (2080, 30)
]

# Initialisation de la somme des sinusoïdes
sum_of_sinusoids = np.zeros_like(t)

# Calcul de la somme des sinusoïdes
for freq, phase in sinusoids:
    y = generate_sine_wave(freq, phase, fs, duration)
    sum_of_sinusoids += y

# Conception du filtre FIR passe-bas d'ordre 2
cutoff_freq = 1000  # Fréquence de coupure du filtre en Hz
num_taps = 3  # Ordre du filtre + 1
fir_coefficients = firwin(num_taps, cutoff_freq, fs=fs, pass_zero=True)

# Application du filtre FIR au signal
filtered_signal = lfilter(fir_coefficients, 1.0, sum_of_sinusoids)

# Affichage du signal original et filtré
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, sum_of_sinusoids, color='red')
plt.title("Somme des sinusoïdes (Signal original)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, filtered_signal, color='blue')
plt.title("Signal filtré par le filtre passe-bas d'ordre 2")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)

# Application de la FFT au signal filtré pour visualiser le spectre de fréquence
N = len(filtered_signal)
fft_filtered = np.fft.fft(filtered_signal)
fft_magnitude_filtered = np.abs(fft_filtered)[:N // 2]
frequencies_filtered = np.fft.fftfreq(N, 1/fs)[:N // 2]

plt.subplot(3, 1, 3)
plt.plot(frequencies_filtered, fft_magnitude_filtered, color='purple')
plt.title("Spectre de fréquence du signal filtré (FFT)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()
