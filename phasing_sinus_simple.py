import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Fonction pour générer un signal sinusoïdal
def generer_signal_sinusoidal(frequence, duree, taux_echantillonnage=44100):
    t = np.linspace(0, duree, int(taux_echantillonnage * duree), endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * frequence * t)  # Amplitude réduite à 0.5 pour éviter la saturation
    return signal, taux_echantillonnage

# Fonction pour créer un signal déphasé et le sommer avec le signal original
def somme_dephasee(donnees_audio, decalage):
    if decalage <= 0 or decalage >= len(donnees_audio):
        print("Erreur: Le décalage est trop grand ou invalide.")
        return donnees_audio
    
    # Créer un signal déphasé
    signal_dephase = np.zeros_like(donnees_audio)
    signal_dephase[decalage:] = donnees_audio[:-decalage]

    # Somme des deux signaux
    signal_somme = donnees_audio + signal_dephase

    '''
    # Normalisation pour éviter les saturations
    max_val = np.max(np.abs(signal_somme))
    if max_val > 0:
        signal_somme = signal_somme / max_val
    '''
        
    return signal_somme

# Fonction pour afficher un oscillographe
def afficher_oscillographe(donnees_audio, taux_echantillonnage):
    plt.figure(figsize=(12, 6))
    temps = np.linspace(0, len(donnees_audio) / taux_echantillonnage, num=len(donnees_audio))
    plt.plot(temps, donnees_audio, label='Signal')
    plt.xlabel('Temps (secondes)')
    plt.ylabel('Amplitude')
    plt.title('Oscillographe du signal')
    plt.grid()
    plt.show()

# Fonction pour lire l'audio
def lire_audio(donnees_audio, taux_echantillonnage):
    print("Lecture de l'audio...")
    sd.play(donnees_audio, taux_echantillonnage)
    sd.wait()
    print("Lecture terminée.")

# Paramètres du signal
frequence = 440  # Fréquence de la sinusoïde (Hz)
duree = float(input("Entrez la durée du signal en secondes : "))  # Durée du signal (s)
decalage = int(input("Entrez le décalage en échantillons pour le déphasage : "))  # Décalage pour le déphasage

# Générer et traiter le signal
signal, taux_echantillonnage = generer_signal_sinusoidal(frequence, duree)
afficher_oscillographe(signal, taux_echantillonnage)

# Appliquer le déphasage et la somme
signal_traite = somme_dephasee(signal, decalage)
afficher_oscillographe(signal_traite, taux_echantillonnage)

# Lire le signal traité
lire_audio(signal_traite, taux_echantillonnage)
