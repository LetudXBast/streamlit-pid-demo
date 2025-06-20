import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# --- Configuration Streamlit ---
st.set_page_config(page_title="Devine la fonction", layout="centered")

st.title("🎯 Devine la fonction cachée")

# --- Étape 1 : définir la fonction cible ---
x = sp.Symbol('x')
target_expr = x**2 - 3
target_func = sp.lambdify(x, target_expr, 'numpy')

# --- Étape 2 : champ de saisie utilisateur ---
user_input = st.text_input("Propose une fonction en x :", value="x**2")

# --- Étape 3 : tracer les courbes ---
x_vals = np.linspace(-10, 10, 500)
try:
    user_expr = sp.sympify(user_input)
    user_func = sp.lambdify(x, user_expr, 'numpy')

    y_target = target_func(x_vals)
    y_user = user_func(x_vals)

    # --- Calcul d'un écart (score) ---
    score = np.mean(np.abs(y_target - y_user))

    # --- Affichage ---
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_target, label="Fonction cible", linewidth=2)
    ax.plot(x_vals, y_user, label="Ta fonction", linestyle="--")
    ax.legend()
    ax.set_title("Comparaison des courbes")

    st.pyplot(fig)

    if score < 0.1:
        st.success("🎉 Bravo, tu as trouvé la bonne fonction !")
    elif score < 1:
        st.info("🧐 Pas mal ! Tu t'en approches.")
    else:
        st.warning("❌ Trop d'écart. Essaie encore.")

    st.write(f"Écart moyen entre les courbes : {score:.3f}")

except Exception as e:
    st.error(f"Erreur dans la fonction saisie : {e}")
