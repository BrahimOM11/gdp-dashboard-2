import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from fpdf import FPDF

# Titre de l'application
st.title('Analyse Statistique Descriptive')

# 1. Importation de données
st.subheader('1. Importer un fichier CSV')
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Aperçu des données :")
    st.write(data.head())

    # 2. Calculs de statistiques descriptives
    st.subheader('2. Statistiques Descriptives')
    if st.checkbox('Afficher les statistiques descriptives'):
        st.write(data.describe())

    # 3. Visualisations interactives
    st.subheader('3. Visualisations interactives')

    col_names = data.columns.tolist()
    col_choice = st.selectbox('Choisissez une colonne à analyser', col_names)

    if st.checkbox('Afficher un histogramme'):
        fig, ax = plt.subplots()
        sns.histplot(data[col_choice], kde=True, ax=ax)
        st.pyplot(fig)

    if st.checkbox('Afficher une boîte à moustaches'):
        fig, ax = plt.subplots()
        sns.boxplot(x=data[col_choice], ax=ax)
        st.pyplot(fig)

    # 4. Analyse de la distribution
    st.subheader('4. Analyse de la distribution')
    k2, p = stats.normaltest(data[col_choice].dropna())  # Tester si la colonne est normalement distribuée
    if p < 0.05:
        st.write("La distribution n'est pas normale (p-valeur < 0.05)")
    else:
        st.write("La distribution est normale (p-valeur >= 0.05)")

    # 5. Identification des outliers
    st.subheader('5. Identification des outliers')
    if st.checkbox('Afficher les outliers'):
        fig, ax = plt.subplots()
        sns.boxplot(x=data[col_choice], ax=ax)
        st.pyplot(fig)
        Q1 = data[col_choice].quantile(0.25)
        Q3 = data[col_choice].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[col_choice] < (Q1 - 1.5 * IQR)) | (data[col_choice] > (Q3 + 1.5 * IQR))]
        st.write("Outliers détectés :")
        st.write(outliers)

    # 6. Téléchargement du rapport
    st.subheader('6. Télécharger le rapport')

    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport Statistique", ln=True)

        # Ajout des statistiques descriptives
        pdf.cell(200, 10, txt="Statistiques Descriptives:", ln=True)
        for col in data.describe().columns:
            stats = data.describe()[col]
            pdf.cell(200, 10, txt=f"{col}: {stats}", ln=True)
        
        pdf.output("rapport_statistique.pdf")

    if st.button('Générer le rapport'):
        generate_pdf()
        st.write("Rapport généré avec succès !")

    st.download_button(
        label="Télécharger le rapport",
        data=open("rapport_statistique.pdf", "rb"),
        file_name="rapport_statistique.pdf",
        mime="application/pdf"
    )
