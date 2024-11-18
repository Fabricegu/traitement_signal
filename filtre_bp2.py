import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin

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

# Conception du filtre FIR passe-bas d'ordre 2 avec scipy
cutoff_freq = 200  # Fréquence de coupure en Hz
num_taps = 10  # Ordre du filtre + 1
nyquist = fs / 2
normalized_cutoff = cutoff_freq / nyquist

# Calcul des coefficients du filtre FIR
coefficients = firwin(num_taps, normalized_cutoff)

# Affichage des coefficients du filtre FIR
print("Coefficients du filtre FIR passe-bas :", coefficients)

# Application manuelle du filtrage par convolution discrète
def apply_fir_filter(signal, coefficients):
    filtered_signal = np.zeros_like(signal)
    # Convolution manuelle
    for n in range(len(signal)):
        # Calcul de la somme pondérée des échantillons précédents
        for k in range(len(coefficients)):
            if n - k >= 0:  # Vérification pour ne pas sortir des limites du tableau
                filtered_signal[n] += coefficients[k] * signal[n - k]
    return filtered_signal

# Appliquer le filtre au signal
filtered_signal = apply_fir_filter(sum_of_sinusoids, coefficients)

# Affichage des signaux
plt.figure(figsize=(12, 8))

# Affichage du signal original
plt.subplot(3, 1, 1)
plt.plot(t, sum_of_sinusoids, color='red')
plt.title("Somme des sinusoïdes (Signal original)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)

# Affichage du signal filtré
plt.subplot(3, 1, 2)
plt.plot(t, filtered_signal, color='blue')
plt.title("Signal filtré par le filtre passe-bas d'ordre 2 (convolution manuelle)")
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
