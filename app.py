import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Démo PID simple")

# Curseurs
Kp = st.slider("Gain proportionnel Kp", 0.0, 10.0, 2.0)
setpoint = st.number_input("Consigne", value=1.0)

# Simulation d’un système de 1er ordre
t = np.linspace(0, 20, 200)
y = setpoint * (1 - np.exp(-Kp * t / 10))  # réponse simplifiée

# Tracé
fig, ax = plt.subplots()
ax.plot(t, y, label="Sortie")
ax.axhline(setpoint, color='gray', linestyle='--', label="Consigne")
ax.set_xlabel("Temps")
ax.set_ylabel("Sortie y(t)")
ax.legend()
st.pyplot(fig)
