import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random

# --- Configuration Streamlit ---
st.set_page_config(page_title="Devine la fonction", layout="centered")
st.title("🎯 Devine la fonction cachée")


with st.expander("ℹ️ Comment proposer une fonction ?", expanded=False):
    st.markdown("""
    Voici quelques règles pour écrire correctement une fonction :

    - Utilise `x` comme variable.
    - Les opérations doivent suivre la syntaxe Python :
        - Multiplication : `*` → exemple : `3*x`
        - Puissance : `**` → exemple : `x**2` pour \(x^2\)
        - Division : `/` → exemple : `1/x`
        - Parenthèses : `()` pour grouper les expressions
    - Fonctions usuelles disponibles :
        - `sin(x)` : sinus
        - `cos(x)` : cosinus
        - `exp(x)` : exponentielle \(e^x\)
        - `log(x)` : logarithme népérien
        - `sqrt(x)` : racine carrée
        - `abs(x)` : valeur absolue
    - ⚠️ Évite d’écrire `e^x`, préfère `exp(x)`
    - Exemple valide : `exp(-x**2) + sin(x)`

    Essaie de proposer une fonction continue et définie sur \[-6 ; 6\].
    """)


# --- Définition des fonctions cibles disponibles ---
x = sp.Symbol('x')
functions_list = [
    x,
    x**2 - 3,
    -x**2 + 2*x + 1,
    x**3 - x,
    abs(x),
    x**2 + sp.sin(x),
    sp.sin(x),
    sp.cos(x) + 1,
    sp.sqrt(abs(x)),
    sp.exp(-x**2),
    x * sp.exp(-x**2),
    sp.sin(x**2),
    sp.log(x**2 + 1),
    x**2 * sp.cos(x),
    sp.cos(x) / (x + 0.01)  # évite 1/0 (pseudo-discontinue)
]

# --- Initialisation de la fonction cible dans la session ---
if "target_expr" not in st.session_state or st.button("🔄 Nouvelle fonction"):
    st.session_state["target_expr"] = random.choice(functions_list)

# --- Fonction cible courante ---
target_expr = st.session_state["target_expr"]
target_func = sp.lambdify(x, target_expr, 'numpy')

# --- Saisie utilisateur ---
user_input = st.text_input("Propose une fonction en x :", value="x")

# --- Tracé des courbes ---
x_vals = np.linspace(-6, 6, 500)
try:
    user_expr = sp.sympify(user_input)
    user_func = sp.lambdify(x, user_expr, 'numpy')

    y_target = target_func(x_vals)
    y_user = user_func(x_vals)

    # Calcul de l'écart
    score = np.mean(np.abs(y_target - y_user))

    # Graphique
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y_target, label="Fonction cible", color='blue', linewidth=2)
    ax.plot(x_vals, y_user, label="Ta fonction", color='red', linestyle='--', linewidth=2)
    ax.grid(True, which='both', linestyle=':', linewidth=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_xlim(-6, 6)
    ax.set_title("Comparaison des courbes")
    ax.legend()
    st.pyplot(fig)

    # Feedback
    if score < 0.1:
        st.success("🎉 Bravo, tu as trouvé la bonne fonction !")
    elif score < 1:
        st.info("🧐 Tu t'en rapproches.")
    else:
        st.warning("❌ Essaie encore.")

    st.write(f"Écart moyen entre les courbes : {score:.3f}")

except Exception as e:
    st.error(f"Erreur dans la fonction saisie : {e}")