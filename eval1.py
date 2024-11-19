import numpy as ____________18
import matplotlib.pyplot as _______17
# Paramètres communs
fs = 48000  # Fréquence d'échantillonnage en Hz
duration = _____ 1 # Durée   pour une obtenir au moins une période complète de tous les signaux
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
# Fonction pour générer une sinusoïde avec une fréquence et une phase spécifiée
def generate_sine_wave(frequency, phase_degree, sampling_rate, duration):
    phase_radians = ________________ 2
    return np.sin(___________________________ 3)
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
    y = generate_sine_wave(_____________4)
    sum_of_sinusoids _________5
# Affichage de la somme des sinusoïdes
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, ___________6, color='red')
plt.title("Somme des sinusoïdes")
plt.xlabel("_________7")
plt.ylabel("_________8")
plt.grid(True)
# Application de la ________________9
N = ________________10
fft_result = np.fft.fft(______________11)
____________12 = np.abs(fft_result)[:N // 2]  # Prendre la moitié du spectre (symétrie)
____________13 = np.fft.fftfreq(N, 1/fs)[:N // 2]
# Affichage du _____________________14
plt.subplot(2, 1, 2)
plt.plot(frequencies, fft_magnitude, color='purple')
plt.title("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
plt.xlabel("___________15")
plt.ylabel("___________16")
plt.grid(True)
plt.tight_layout()
plt.show()