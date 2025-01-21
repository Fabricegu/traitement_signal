import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

def plot_bode(b, a, fs=1.0):
    """
    Trace le diagramme de Bode d'un filtre numérique.

    Paramètres :
    - b : coefficients du numérateur du filtre.
    - a : coefficients du dénominateur du filtre.
    - fs : fréquence d'échantillonnage en Hz (par défaut 1.0).
    """
    # Calcul de la réponse en fréquence
    w, h = freqz(b, a, worN=8000)

    # Conversion des pulsations en fréquence (Hz)
    freqs = w * fs / (2 * np.pi)

    # Calcul du gain en décibels et de la phase
    magnitude = 20 * np.log10(abs(h))
    phase = np.angle(h, deg=True)

    # Tracé du diagramme de Bode
    plt.figure(figsize=(12, 8))

    # Magnitude
    plt.subplot(2, 1, 1)
    plt.plot(freqs, magnitude)
    plt.title("Diagramme de Bode")
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Gain (dB)")
    plt.grid(which="both", linestyle="--", linewidth=0.5)

    # Phase
    plt.subplot(2, 1, 2)
    plt.plot(freqs, phase)
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Phase (degrés)")
    plt.grid(which="both", linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.show()

def recurrence_example():
    """
    Exemple de calcul d'un signal de sortie avec une équation de récurrence
    à partir des coefficients d'un filtre numérique.
    """
    # Coefficients du filtre
    b = [0.2, 0.4, 0.2]  # Numérateur
    a = [1.0, -0.5, 0.25]  # Dénominateur

    # Signal d'entrée : impulsion
    x = [1, 0, 0, 0, 0, 0, 0, 0]  # Exemple d'impulsion
    y = [0] * len(x)  # Initialisation du signal de sortie

    # Calcul du signal de sortie avec l'équation de récurrence
    for n in range(len(x)):
        # Partie liée à l'entrée
        y[n] += sum(b[k] * x[n - k] for k in range(len(b)) if n - k >= 0)
        # Partie liée à la rétroaction
        y[n] -= sum(a[k] * y[n - k] for k in range(1, len(a)) if n - k >= 0)

    # Affichage des résultats
    print("Signal d'entrée x:", x)
    print("Signal de sortie y:", y)

    # Tracé des signaux
    plt.figure(figsize=(10, 6))
    plt.stem(range(len(x)), x, linefmt='b-', markerfmt='bo', basefmt=" ", label="Entrée x[n]", use_line_collection=True)
    plt.stem(range(len(y)), y, linefmt='r-', markerfmt='ro', basefmt=" ", label="Sortie y[n]", use_line_collection=True)
    plt.title("Signal d'entrée et de sortie")
    plt.xlabel("n")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

# Exemple : diagramme de Bode pour un filtre passe-bas
b = [0.2, 0.2, 0.2, 0.2, 0.2]  # Numérateur
a = [1.0]  # Dénominateur
fs = 1000  # Fréquence d'échantillonnage en Hz

plot_bode(b, a, fs)

# Exemple d'équation de récurrence
recurrence_example()
