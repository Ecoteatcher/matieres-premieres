import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Matières premières", layout="centered")

st.title("📈 Corrélation entre matières premières")
st.caption("Choisissez deux matières premières pour comparer l'évolution de leurs cours.")

# ---------------------------------------------------------------
# Chargement des données (les CSV doivent être dans le même dossier
# que ce fichier app.py)
# ---------------------------------------------------------------

@st.cache_data
def charger_donnees():
    cacao = pd.read_csv('cacao.csv', sep=";", index_col='Date', parse_dates=True)
    cuivre = pd.read_csv('cuivre.csv', sep=";", index_col='Date', parse_dates=True)
    ble = pd.read_csv('ble.csv', sep=";", index_col='Date', parse_dates=True)
    petrole = pd.read_csv('petrole.csv', sep=";", index_col='Date', parse_dates=True)

    cles = ('a', 'b', 'c', 'd')
    valeurs = (cacao, cuivre, ble, petrole)
    dico = {k: v for k, v in zip(cles, valeurs)}

    matiere = ('cacao', 'cuivre', 'blé', 'pétrole')
    inventaire = {k: v for k, v in zip(cles, matiere)}

    return dico, inventaire


try:
    dico, inventaire = charger_donnees()
except FileNotFoundError as e:
    st.error(
        f"Fichier introuvable : {e.filename}. "
        "Vérifie que cacao.csv, cuivre.csv, ble.csv et petrole.csv "
        "sont bien présents à côté de app.py."
    )
    st.stop()

# ---------------------------------------------------------------
# Interface : deux menus déroulants à la place des input()
# ---------------------------------------------------------------

options = {f"{k} - {v}": k for k, v in inventaire.items()}

col1, col2 = st.columns(2)
with col1:
    choix_a = st.selectbox("Première matière première", options.keys())
with col2:
    choix_b = st.selectbox("Deuxième matière première", options.keys(), index=1)

a = options[choix_a]
b = options[choix_b]

if a == b:
    st.warning("Choisis deux matières premières différentes.")
    st.stop()

matprem = pd.merge(dico[a], dico[b], on='Date', how='inner')

if matprem.empty:
    st.warning("Aucune date commune entre ces deux jeux de données.")
    st.stop()

matprem = matprem.rename(
    columns={"Clôture_x": inventaire[a], "Clôture_y": inventaire[b]}
)

st.subheader(f"Évolution des cours du {inventaire[a]} et du {inventaire[b]}")

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
matprem[[inventaire[a], inventaire[b]]].plot(subplots=True, ax=axes)
fig.suptitle(f"Evolution des cours du {inventaire[a]} et du {inventaire[b]}")

st.pyplot(fig)

with st.expander("Voir les données utilisées"):
    st.dataframe(matprem[[inventaire[a], inventaire[b]]])
