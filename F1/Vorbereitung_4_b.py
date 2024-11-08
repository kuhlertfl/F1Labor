import numpy as np
import matplotlib.pyplot as plt

# Parameter definieren
fs = 10000  # Abtastrate (Hz)
T = 1       # Gesamtdauer des Signals (Sekunden)
omega_0 = 2 * np.pi * 50  # Kreisfrequenz der Sinuswelle (50 Hz)
delta_t = 0.1  # Dauer des Rechteckimpulses (Sekunden)

t = np.linspace(0, T, int(T * fs), endpoint=False)  # Zeitachse
sinus = np.sin(omega_0 * t)  # Sinussignal
rectangle = np.where((t >= T/2 - delta_t/2) & (t <= T/2 + delta_t/2), 1, 0)  # Rechteckimpuls zentriert in der Mitte
product = sinus * rectangle  # Produkt aus Sinus und Rechteckimpuls

N = len(t)  # Anzahl der Samples
product_fft = np.fft.fft(product)  # Fourier-Transformation des Produkts
print(product_fft)
print(type(product_fft))
frequencies = np.fft.fftfreq(N, 1/fs)  # Frequenzachse

plt.figure(figsize=(12, 6))

# Zeitdomänenplot
plt.subplot(2, 1, 1)
plt.plot(t, product, label='Sinus * Rechteck')
plt.title('Zeitdomäne')
plt.xlabel('Zeit [s]')
plt.ylabel('Amplitude')
plt.grid(True)

# Frequenzdomänenplot
plt.subplot(2, 1, 2)
plt.plot(frequencies, np.abs(product_fft), label='FFT von Sinus * Rechteck')
plt.title('Frequenzdomäne')
plt.xlabel('Frequenz [Hz]')
plt.ylabel('Amplitude')
plt.xlim(-200, 200)  # Einschränkung der x-Achse für bessere Sichtbarkeit
plt.grid(True)

plt.tight_layout()
plt.show()
