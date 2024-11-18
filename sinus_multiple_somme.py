import numpy as np
import matplotlib.pyplot as plt

# Paramètres communs
fs = 48000  # Fréquence d'échantillonnage en Hz
duration = 0.02  # Durée de la sinusoïde en secondes (par exemple, 10 ms)
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Fonction pour générer une sinusoïde avec une fréquence et une phase spécifiée
def generate_sine_wave(frequency, phase_degree, sampling_rate, duration):
    phase_radians = np.deg2rad(phase_degree)
    return np.sin(2 * np.pi * frequency * t + phase_radians)

# Caractéristiques des sinusoïdes
sinusoids = [(120,0),
    (260, 45),
    (1080, 10),
    (4120, 0),
    (440, 90),
    (2080, 30)
]

# Initialisation de la somme des sinusoïdes
sum_of_sinusoids = np.zeros_like(t)

# Tracé des sinusoïdes individuelles
plt.figure(figsize=(12, 12))

for i, (freq, phase) in enumerate(sinusoids, 1):
    y = generate_sine_wave(freq, phase, fs, duration)
    sum_of_sinusoids += y
    plt.subplot(7, 1, i)
    plt.plot(t, y)
    plt.title(f"Sinusoïde à {freq} Hz avec une phase de {phase}°")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

# Tracé de la somme des sinusoïdes
plt.subplot(6, 1, 6)
plt.plot(t, sum_of_sinusoids, color='red')
plt.title("Somme des sinusoïdes")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()
