﻿"""Auswertegerüst für den Versuch F1.

Dieses Python-Skript ist ein Grundgerüst für die Auswertung des Versuches

       Lineare Systemtheorie und Messung von Übertragungsfunktionen

des Fortgeschrittenenpraktikums im Studiengang B-AMP. Dieses Skript muss für
die einzelnen Teilversuche entsprechend angepasst werden, so dass Sie die
Aufgaben, die in der Versuchsanleitung angegeben sind, bearbeiten können.

Insbesondere sollten Sie die theoretischen Kurven für die
Übertragungsfunktionen noch zusätzlich darstellen.

© Oliver Natt, Nürnberg, August 2021.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import Tektronix


# #############################################################################
# #############################################################################
#
#      Teil 1: Bestimmung und Darstellung der Übertragungsfunktion H
#
# #############################################################################
# #############################################################################


# Lies die Eingangsdaten ein. Hier bitte den richtigen Pfadnamen einsetzen,
# oder eine Routine schreiben, die das interaktiv einließt.
data1 = Tektronix.Dict('ALL0011')
input1 = data1['CH1']
output1 = data1['CH2']

# Wir gehen davon aus, dass beide Datensätze die gleiche Zeitskala verwenden:
time = input1.x

# Führe die Fourier-Transformation durch.
input_fft = np.fft.fft(input1.y, norm='forward')
output_fft = np.fft.fft(output1.y, norm='forward')

# Bestimme die zugehörigen Frequenzen.
freq = np.fft.fftfreq(input_fft.size, d=time[1]-time[0])

# Sortiere die Frequenzen in aufsteigender Reihenfolge.
freq = np.fft.fftshift(freq)
input_fft = np.fft.fftshift(input_fft)
output_fft = np.fft.fftshift(output_fft)

# Erzeuge eine Figure und zwei Axes für den Plot im Zeit- und Frequenzbereich.
fig1 = plt.figure('Messung 1', figsize=(10, 5))
fig1.set_tight_layout(True)
fig1.suptitle('Ein- und Ausgangssignal der Messung zur '
              'Bestimmung der Übertragungsfunktion')
ax1_links, ax1_rechts = fig1.subplots(1, 2)

ax1_links.set_title('Zeitbereich')
ax1_links.set_xlabel('t [s]')
ax1_links.set_ylabel('U [V]')
ax1_links.grid()
ax1_links.plot(time, input1.y, label='input')
ax1_links.plot(time, output1.y, label='output')
ax1_links.legend()

ax1_rechts.set_title('Frequenzbereich')
ax1_rechts.set_xlabel('f [Hz]')
ax1_rechts.set_ylabel('U [V]')
ax1_rechts.set_xlim(-5, 5)
ax1_rechts.grid()
ax1_rechts.plot(freq, np.abs(input_fft), label='input')
ax1_rechts.plot(freq, np.abs(output_fft), label='output')
ax1_rechts.legend()

# Berechne die Übertragungsfunktion
H = output_fft / input_fft

# Um die Übertragsgungsfunktion nachzuberarbeiten, erzeugen wir zunächst eine
# Kopie des Arrays.
H_mod = H.copy()

# Für zu große Frequenzen liefert die experimentell bestimmte
# Übertragungsfunktion keine guten Werte mehr (warum?). Wir setzen die
# Übertragungsfunktion für Frequenzen, die größer als eine vorgegebene
# Abschneidefrequenz sind, auf Null.
# Spielen Sie mit der Abschneidefrequenz etwas herum und beobachten Sie,
# was dabei mit der Vorhersage des Ausgangssignals passiert.
H_mod[np.abs(freq) > 10] = 0

# Alternativ kann man auch alle Teile der Übertragungsfunktion auf Null
# setzen, bei der das Eingangssignal unterhalb einer gewissen Schwelle liegt.
# Spielen Sie auch hiermit einmal herum.
# Der folgende Beispielcode setzt alle Werte der Übertragungsfunktion auf
# Null, bei der das Eingangssignal weniger als 5 % seiner maximalen Amplitude
# hat.
H_mod[np.abs(input_fft) < 0.05 * np.max(np.abs(input_fft))] = 0

# Erzeuge eine Figure und zwei Axes für den Plot der Übertragungsfunktion.
fig2 = plt.figure('Übertragungsfunktion', figsize=(10, 5))
fig2.set_tight_layout(True)
fig2.suptitle('Übertragungsfunktion')

# Erzeuge vier Axes. Diese teilen sich jeweils eine Axsenskalierung.
#     links:  Ungefilterte Übertragungsfunktion
#     rechts: Gefilterte Übertragungsfunktion
#     oben:   Betrag
#     unten:  Phase
ax2 = fig2.subplots(2, 2, sharex=True)
ax2[0, 0].sharey(ax2[0, 1])
ax2[1, 0].sharey(ax2[1, 1])
ax2[0, 0].set_xlim(-5, 5)
ax2[0, 1].set_xlim(-5, 5)
ax2[0, 0].set_ylim(0, 2)
ax2[0, 0].set_title('ungefiltert')
ax2[0, 1].set_title('modifiziert')
ax2[1, 0].set_xlabel('f [Hz]')
ax2[1, 1].set_xlabel('f [Hz]')
ax2[0, 0].set_ylabel('|H|')
ax2[1, 0].set_ylabel('arg(H) [rad]')
for ax in ax2.flat:
    ax.grid()

# Plotte den Betrag und den Phasenwinkel der Übertragungsfunktion.
# Konventiongemäß wird bei Übertragungsfunktionen der Winkel mit einem
ax2[0, 0].plot(freq, np.abs(H))
ax2[1, 0].plot(freq, -np.angle(H))
ax2[0, 1].plot(freq, np.abs(H_mod))
ax2[1, 1].plot(freq, -np.angle(H_mod))


# #############################################################################
# #############################################################################
#
#      Teil 2: Vorhersage der Systemantwort mit Hilfe der
#              Übertragungsfunktion
#
# #############################################################################
# #############################################################################

# Lies die Eingangsdaten ein. Hier bitte den richtigen Pfadnamen einsetzen,
# oder eine Routine schreiben, die das interaktiv einließt.
data2 = Tektronix.Dict('ALL0011')
input2 = data2['CH1']
output2 = data2['CH2']

# Wir gehen davon aus, dass beide Kanäle die gleiche Zeitbasis verwenden:
time2 = input2.x

# Führe die Fourier-Transformation durch und sortiere die Frequenzen in
# aufsteigender Reihenfolge.
input2_fft = np.fft.fft(input2.y, norm='forward')
freq2 = np.fft.fftfreq(input2_fft.size, d=time2[1]-time2[0])
freq2 = np.fft.fftshift(freq2)
input2_fft = np.fft.fftshift(input2_fft)

# Wir berechnen nun das theoretische Ausgangssignal, das aufgrund des
# gegebenen Eingangssignals und der berechneten Übertragungsfunktion zu
# erwarten ist. Da die beiden Messungen im allgemeinen mit unterschiedlichen
# Zeitbasen erfolgt haben, müssen wir die Übertragungsfunktion zunächst
# auf die neuen Frequenzen interpolieren. Wir verwenden für die Vorhersage
# die nachbearbeitete Übertragungsfunktion H_filt.
H_interp = np.interp(freq2, freq, H_mod)
output2_theo_fft = input2_fft * H_interp

# Mache die Sortierung der Frequenzkomponenten wieder rückgängig und führe
# die inverse Fourier-Transformation durch.
output2_theo_fft = np.fft.ifftshift(output2_theo_fft)
output2_theo = np.fft.ifft(output2_theo_fft, norm='forward')

# Erzeuge eine Figure und zwei Axes für das Eingangssignal, sowie das
# gemessene und berechnete Ausgangssignal.
fig3 = plt.figure('Vorhersage des Ausgangssignals')
fig3.set_tight_layout(True)
ax3_oben, ax3_unten = fig3.subplots(2, 1, sharex=True)

ax3_oben.set_title('Eingangssignal der zweiten Messung.')
ax3_oben.set_ylabel('U [V]')
ax3_oben.grid()
ax3_oben.plot(time2, input2.y)

ax3_unten.set_title('Ausgangssignal der zweiten Messung.')
ax3_unten.set_xlabel('t [s]')
ax3_unten.set_ylabel('U [V]')
ax3_unten.grid()
ax3_unten.plot(time2, output2.y, label='gemessen')
ax3_unten.plot(time2, np.real(output2_theo), label='berechnet')
ax3_unten.legend()

# Zeige alle Grafiken an.
plt.show()
