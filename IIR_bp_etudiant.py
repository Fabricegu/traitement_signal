import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin
from scipy.signal import butter, lfilter

# Paramètres du filtre
order = 8  # Ordre du filtre
cutoff_freq = 500  # Fréquence de coupure n

# Paramètres communs
fs = 48000  # Fréquence d'échantillonnage en Hz
duration = 0.1  # Durée du signal en secondes
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

# Calcul des coefficients du filtre passe-bas
b, a = butter(order, cutoff_freq, btype='low', fs=fs)
# Affichage des coefficients du filtre IIR
print("Coefficients du filtre IIR passe-bas :")
print("Numerateur (b) :", b)
print("Denominateur (a) :", a)

# Application du filtrage IIR au signal
def apply_iir_filter_lib(signal, b, a):
    return lfilter(b, a, signal)

# Fonction pour appliquer le filtrage IIR
def apply_iir_filter(signal, b, a):
    y = np.zeros_like(signal)
    for n in range(len(signal)):
        # Calcul de la sortie pour chaque point
        for i in range(len(b)):
            if n - i >= 0:
                y[n] += b[i] * signal[n - i]
        for j in range(1, len(a)):
            if n - j >= 0:
                y[n] -= a[j] * y[n - j]
    return y

# Appliquer le filtre au signal
filtered_signal = apply_iir_filter(sum_of_sinusoids, b, a)
#filtered_signal = apply_iir_filter_lib(sum_of_sinusoids, b, a)

# Affichage des signaux
plt.figure(figsize=(12, 8))

# Affichage du signal original
plt.subplot(4, 1, 1)
plt.plot(t, sum_of_sinusoids, color='red')
plt.title("Somme des sinusoïdes (Signal original)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)

# Affichage du signal filtré
plt.subplot(4, 1, 2)
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

plt.subplot(4, 1, 4)
plt.plot(frequencies_filtered, fft_magnitude_filtered, color='purple')
plt.title("Spectre de fréquence du signal filtré (FFT)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)

# Application de la FFT au signal d'origine pour visualiser le spectre de fréquence
N = len(sum_of_sinusoids)
fft_signal = np.fft.fft(sum_of_sinusoids)
fft_magnitude_signal = np.abs(fft_signal)[:N // 2]
frequencies_signal = np.fft.fftfreq(N, 1/fs)[:N // 2]

plt.subplot(4, 1, 3)
plt.plot(frequencies_signal, fft_magnitude_signal, color='purple')
plt.title("Spectre de fréquence du signal d'origine (FFT)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()
