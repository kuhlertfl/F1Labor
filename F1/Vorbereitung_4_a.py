import numpy as np 
import matplotlib.pyplot as plt

# Parameter
a = 1       # Höhe des Rechtecksignals
delta_t = 0.1   # Dauer des Rechtecksignals
sample_rate = 1000  # Abtastrate in Hz
T = 1       # Gesamtdauer des Signals in Sekunden
N = int(T * sample_rate)  # Anzahl der Samples

# Zeitachse
t = np.linspace(-T/2, T/2, N, endpoint=False)

# Rechtecksignal erzeugen
signal = a * (np.abs(t) <= delta_t / 2)

# Fourier-Transformation
frequenzen = np.fft.fftfreq(N, 1/sample_rate)
signal_fft = np.fft.fft(signal)

# Plot
plt.figure(figsize=(12, 6))

# Originalsignal
plt.subplot(121)
plt.plot(t, signal, label="Rechtecksignal")
plt.title("Zeitdomäne")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
plt.grid(True)

# Amplitudenspektrum
plt.subplot(122)
plt.stem(frequenzen, np.abs(signal_fft), linefmt='b-', markerfmt='bo', basefmt='r-')
plt.title("Frequenzdomäne")
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.xlim(-50, 50)  # Freq

plt.show()
import sympy as sp

# Symbolische Variablen definieren
t, f = sp.symbols('t f', real=True)
delta_t, a = sp.symbols('delta_t a', positive=True, real=True)

# Rechtecksignal definieren
x_t = a * sp.Piecewise((1, sp.Abs(t) <= delta_t / 2), (0, True))

# Fourier-Transformation berechnen
X_f = sp.fourier_transform(x_t, t, f)

# Ergebnis ausgeben
X_f.simplify()  # Simplify das Ergebnis, um es klarer zu machen
print(X_f)

