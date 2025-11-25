import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# Nom du fichier de sortie
EXCEL_FILE = "reponses_questionnaire_bloc.xlsx"

st.set_page_config(
    page_title="Questionnaire bloc opératoire",
    layout="wide",
)

#st.sidebar.write("Version questionnaire : A→I complet, échelle 0–5")
# ---------- FOND D'ÉCRAN AVEC IMAGE ----------

def set_background(image_file: str):
    """Image de fond + style (questions grandes, échelle petite, réponses en blanc)."""
    import base64
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    /* ---------- FOND D'ÉCRAN (sélecteurs robustes pour différentes versions de Streamlit) ---------- */
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stAppViewContainer"] > main,
    .stApp, .stApp > main,
    html, body {{
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)),
            url("data:image/png;base64,{data}");
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        background-color: transparent !important;
    }}

    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    /* ---------- TAILLE DU TEXTE GLOBALE ---------- */
    html, body, [data-testid="stAppViewContainer"] * {{
        font-size: 1.05rem;
    }}

    h1 {{
        font-size: 1.7rem !important;
        font-weight: 700 !important;
    }}
    h2, .stMarkdown h2 {{
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }}
    h3, .stMarkdown h3 {{
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }}

    /* ---------- QUESTIONS (LABELS) EN NOIR ET GRANDES ---------- */
    [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] * {{
        color: #111111;
    }}

    /* libellés des widgets (sliders, selectbox, inputs…) */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] > label,
    [data-testid="stWidgetLabel"] > div,
    [data-testid="stSliderLabel"],
    [data-testid="stSliderLabel"] > div {{
        color: #111111 !important;
        font-size: 1.05rem !important;   /* ← taille des questions */
        font-weight: 600 !important;
    }}

    /* questions écrites avec st.markdown */
    .stMarkdown p,
    .stMarkdown li {{
        font-size: 1.05rem !important;
    }}

    /* ---------- TEXTE DE L'ÉCHELLE (PETIT) ---------- */
    .scale-caption {{
        font-size: 0.85rem !important;
        color: #555555 !important;
        margin-top: 0.2rem;
        margin-bottom: 0.5rem;
    }}

    /* ---------- CADRE CLAIR AUTOUR DES WIDGETS ---------- */
    .stTextInput, .stNumberInput, .stTextArea,
    .stSelectbox, .stMultiSelect, .stSlider {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 0.6rem;
        padding: 0.3rem 0.6rem;
    }}

         /* ---------- ZONES DE RÉPONSE (CHAMPS, SELECT, NOMBRE) ---------- */

    /* Carte blanche autour des widgets : on garde comme tu avais */
    .stTextInput, .stNumberInput, .stTextArea,
    .stSelectbox, .stMultiSelect, .stSlider {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 0.6rem;
        padding: 0.3rem 0.6rem;
    }}

    /* CONTENEUR INTERNE QUI EST NOIR PAR DÉFAUT (baseweb) */
    /* → on l’éclaircit fortement */
    div[data-baseweb="input"] > div:first-child,
    div[data-baseweb="textarea"] > div:first-child,
    div[data-baseweb="select"] > div:first-child {{
        background-color: rgba(0, 0, 0, 0.10) !important;  /* gris très clair */
        border-radius: 0.6rem !important;
    }}

    /* Texte réellement saisi (réponses) : en blanc */
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {{
        background-color: transparent !important;  /* on voit la couleur du conteneur ci-dessus */
        color: #000000 !important;
        border: none !important;
    }}

    /* SELECTBOX / MULTISELECT : texte en blanc aussi */
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span {{
        color: #ffffff !important;
    }}

    /* Boutons +/- du st.number_input : même fond éclairci */
    div[data-testid="stNumberInput"] > div > div {{
        background-color: rgba(0, 0, 0, 0.10) !important;
        border-radius: 0.6rem !important;
    }}
    div[data-testid="stNumberInput"] button svg {{
        fill: #000000 !important;
    }}

    /* ---------- RÉPONSES EN BLANC (SLIDERS) ---------- */
    [data-testid="stSliderValue"] > div {{
        color: #000000 !important;
        font-weight: 600;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 0.1rem 0.4rem;
        border-radius: 0.4rem;
        font-size: 1.1rem !important;
    }}

    /* sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: rgba(255, 255, 255, 0.9);
        color: #000000 !important;
    }}
        /* ---------- ZONES DE RÉPONSE : CHAMPS TEXTE / NOMBRE / TEXTAREA ---------- */

    /* Carte blanche autour des widgets (cadre extérieur) */
    .stTextInput,
    .stNumberInput,
    .stTextArea {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 0.6rem;
        padding: 0.3rem 0.6rem;
    }}

    /* TOUS les conteneurs internes des champs → gris très clair */
    .stTextInput div,
    .stNumberInput div,
    .stTextArea div {{
        background-color: rgba(0, 0, 0, 0.08) !important;  
        border-radius: 0.6rem !important;
    }}

    /* Texte saisi : blanc, fond transparent pour laisser voir le conteneur gris clair */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {{
        background-color: transparent !important;
        color: #000000!important; 
        border: none !important; 
    }}
    /* ---------- BOUTON "Envoyer mes réponses" ---------- */
    .stButton > button,
    .stButton > button * {{            /* le texte (span, etc.) */
        color: #ffffff !important;    /* texte blanc */
    }}
    
    /* Optionnel : style du fond du bouton */
    .stButton > button {{
        background-color: #111827 !important;  /* fond sombre */
        border-radius: 0.6rem !important;
        border: 1px solid rgba(0, 0, 0, 0.15) !important;
        padding: 0.4rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 1.0rem !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)



# appeler la fonction une fois (adapter le nom du fichier si besoin)
set_background("background.png")

# ------------------------------------------------------------------
# Slider 0–5 (0 = pas de réponse)
# ------------------------------------------------------------------
LIKERT_OPTIONS = list(range(0, 6))  # 0,1,2,3,4,5


def likert_question(label: str, key: str):
    """
    Question = label du slider (agrandi par CSS).
    Phrase d'échelle en petit en dessous.
    0 = pas de réponse (valeur par défaut).
    """
    # Question à l'intérieur du cadre (label du slider)
    value = st.slider(
        label,
        min_value=0,
        max_value=5,
        value=0,
        key=key,
    )

    # Phrase de signification de l'échelle, en petit
    st.markdown(
        "<span style='font-size:0.8rem; color:#555555;'>"
        #"0 = pas de réponse ; "
        "1 = jamais / pas du tout vrai ; 2 = rarement ; "
        "3 = parfois ; 4 = souvent ; 5 = toujours / tout à fait vrai."
        "</span>",
        unsafe_allow_html=True,
    )

    return value

# ------------------------------------------------------------------
# Titre & intro
# ------------------------------------------------------------------
st.title("Questionnaire de validation des modèles de planification et d’ordonnancement au bloc opératoire")
st.caption("Recherche sur la programmation opératoire et la replanification sous perturbations")

st.markdown(
    "Pour chaque question fermée, choisissez la réponse qui reflète votre pratique réelle."
)

# ------------------------------------------------------------------
# FORMULAIRE
# ------------------------------------------------------------------
with st.form("questionnaire"):

    # ==============================================================
    # Informations répondant
    # ==============================================================
    st.subheader("Informations répondant")

    prenom = st.text_input("Prénom :", key="prenom")
    nom = st.text_input("Nom :", key="nom")

    # ==============================================================
    # A. Informations générales
    # ==============================================================

    st.header("A. Informations générales")

    A1 = st.selectbox(
        "A.1. Votre fonction principale au bloc opératoire :",
        ["Chirurgien", "Anesthésiste", "Cadre de santé", "Responsable de bloc","Direction/gestionnaire" ,"Autre"],
    )
    A1_autre = ""
    if A1 == "Autre":
        A1_autre = st.text_input("Préciser votre fonction :", key="A1_autre")

    A2 = st.text_input("A.2. Spécialité principale (si applicable) :", key="A2")


    A3 = st.selectbox(
        "A.3. Type d’établissement :",
        ["CHU", "CHR/CHRU","CH" ,"Clinique privée", "Autre"],
        key="A3"
    )
    A3_autre = ""
    if A3 == "Autre":
        A3_autre = st.text_input("Préciser le type d’établissement :", key="A3_autre")

    A4 = st.number_input(
        "A.4. Nombre approximatif de salles opératoires (toutes spécialités confondues) :",
        min_value=0, step=1, key="A4"
    )

    A5 = st.number_input(
        "A.5. Nombre moyen d’interventions électives par jour dans votre bloc :",
        min_value=0, step=1, key="A5"
    )

    A6 = st.text_input("A.6. Horaires habituels- Début des programmes:", key="A6")
    A7 = st.text_input("A.7. Horaires habituels- Fin théorique des programmes:", key="A7")
    # ==============================================================
    # B. Organisation de la programmation opératoire
    # ==============================================================

    st.header("B. Organisation de la programmation opératoire (interventions électives)")
    st.subheader("B1. Horizon et processus de planification")

    B1_1 = st.selectbox(
        "B1.1. Le programme opératoire électif est généralement fixé :",
        [
            "Le jour même",
            "La veille",
            "2–3 jours avant",
            "1 semaine avant",
            "Plus d’une semaine avant",
        ],
        key="B1_1",
    )

    B1_2 = st.selectbox(
        "B1.2. Une fois le programme validé, les modifications majeures "
        "(ajout/suppression d’interventions, changement d’ordre) sont :",
        [
            "Très rares",
            "Occurentes mais limitées",
            "Fréquentes",
        ],
        key="B1_2",
    )

    st.markdown("**B1.3. Indiquez votre accord (échelle 1–5) avec les affirmations suivantes :**")

    B1_3_1 = likert_question(
        "B1.3.1 Le programme du lendemain est globalement respecté "
        "(ordre et contenu des interventions).",
        "B1_3_1",
    )
    B1_3_2 = likert_question(
        "B1.3.2 Il existe une procédure formalisée de construction du programme électif.",
        "B1_3_2",
    )
    B1_3_3 = likert_question(
        "B1.3.3 La non-disponibilité prévue de certaines ressources "
        "(chirurgiens, lits de réveil, etc.) est intégrée au moment de la planification.",
        "B1_3_3",
    )

    st.subheader("B2. Règles de priorité et critères de planification")

    st.markdown(
        "B2.4. Lors de la planification des interventions électives, les critères "
        "suivants sont réellement pris en compte (échelle 1–5) :"
    )

    B2_4_1 = likert_question("B2.4.1 Urgence médicale relative (délais recommandés par spécialité).", "B2_4_1")
    B2_4_2 = likert_question("B2.4.2 Durée opératoire estimée.", "B2_4_2")
    B2_4_3 = likert_question("B2.4.3 Disponibilité des chirurgiens.", "B2_4_3")
    B2_4_4 = likert_question("B2.4.4 Disponibilité anesthésistes / IADE.", "B2_4_4")
    B2_4_5 = likert_question("B2.4.5 Disponibilité des lits de réveil / USI / service d’aval.", "B2_4_5")
    B2_4_6 = likert_question("B2.4.6 Besoin spécifique en équipement (robot, imagerie, etc.).", "B2_4_6")
    B2_4_7 = likert_question("B2.4.7 Contraintes patient (âge, comorbidités, transport, travail).", "B2_4_7")
    B2_4_8 = likert_question("B2.4.8 Équité entre chirurgiens / services sur l’accès aux créneaux.", "B2_4_8")

    B2_5 = st.selectbox(
        "B2.5. L’ordre des interventions dans une même salle est plutôt déterminé par :",
        [
            "Des règles explicites (durée, profil patient, contraintes logistiques, etc.)",
            "Des habitudes / accords informels entre équipes",
            "Les préférences des chirurgiens",
            "Autre",
        ],
        key="B2_5",
    )
    B2_5_autre = ""
    if B2_5 == "Autre":
        B2_5_autre = st.text_input("Préciser :", key="B2_5_autre")

    B2_6 = likert_question(
        "B2.6. Il existe des règles non écrites qui influencent l’ordre ou la sélection des "
        "interventions (par ex. « on met les longues en premier », « on termine par les petites »).",
        "B2_6",
    )
    B2_6_exemples = st.text_area(
        "Si oui, pouvez-vous en citer quelques-unes ?",
        key="B2_6_exemples",
    )

    B_commentaires = st.text_area(
        "Commentaires libres sur la programmation élective :",
        key="B_commentaires",
    )

    # ==============================================================
    # C. Ressources critiques : salles, chirurgiens, lits
    # ==============================================================

    st.header("C. Ressources critiques : salles, chirurgiens, lits de réveil")

    st.subheader("C1. Salles opératoires")

    C1_1 = st.selectbox(
        "C1.1. Dans votre pratique, la capacité en salles opératoires est :",
        [
            "Le principal goulot",
            "Fréquemment limitante",
            "Occasionnellement limitante",
            "Rarement un problème",
        ],
        key="C1_1",
    )

    C1_2 = st.selectbox(
        "C1.2. La durée moyenne entre deux interventions (nettoyage, réinstallation) est :",
        ["< 15 min", "15–30 min", "30–45 min", "> 45 min"],
        key="C1_2",
    )

    C1_3 = st.selectbox(
        "C1.3. Cette durée entre deux interventions est :",
        ["Relativement stable", "Très variable selon l’équipe, l’heure, la spécialité, etc."],
        key="C1_3",
    )

    st.subheader("C2. Chirurgiens et équipes")

    C2_4 = likert_question(
        "C2.4. Il est fréquent qu’un même chirurgien soit prévu sur plusieurs salles dans la même journée.",
        "C2_4",
    )

    C2_5 = likert_question(
        "C2.5. Lorsque cela arrive, l’organisation tient compte explicitement de ces conflits "
        "potentiels de présence (pour éviter qu’un chirurgien soit requis simultanément dans deux salles).",
        "C2_5",
    )

    C2_6 = st.selectbox(
        "C2.6. Les changements de chirurgien sur une intervention (remplacement, échange) en cours de journée sont :",
        ["Quasi inexistants", "Occasionnels", "Fréquents"],
        key="C2_6",
    )

    st.subheader("C3. Lits de réveil / SSPI / réanimation")

    C3_7 = likert_question(
        "C3.7. Le manque de lits de réveil / SSPI retarde ou empêche des interventions.",
        "C3_7",
    )

    C3_8 = likert_question(
        "C3.8. Les contraintes de lits d’aval (réanimation, surveillance continue, service) "
        "sont anticipées au moment de la planification du programme électif.",
        "C3_8",
    )

    C3_9 = likert_question(
        "C3.9. Il existe des règles de priorisation pour l’accès aux lits de réveil / lits critiques en cas de pénurie "
        "(par exemple score de gravité, type d’intervention, urgence).",
        "C3_9",
    )
    C3_9_details = st.text_area(
        "Si oui, lesquelles ?",
        key="C3_9_details",
    )

    C_commentaires = st.text_area(
        "Commentaires sur les ressources goulots (salles, chirurgiens, lits) :",
        key="C_commentaires",
    )

    # ==============================================================
    # D. Durées opératoires : estimation et variabilité
    # ==============================================================

    st.header("D. Durées opératoires : estimation et variabilité")

    D1 = st.multiselect(
        "D.1. Les durées opératoires utilisées pour planifier (y compris installation et réveil) sont basées sur :",
        [
            "L’expérience des chirurgiens",
            "Des historiques / statistiques par type d’acte",
            "Des temps « officiels » moyens fournis par le bloc",
            "Des durées calculées/ issues d'un outil informatique",
            "Autre",
        ],
        key="D1",
    )
    D1_autre = ""
    if "Autre" in D1:
        D1_autre = st.text_input("Préciser (autre source) :", key="D1_autre")

    st.markdown("**D.2. Indiquez votre perception (échelle 1–5) :**")

    D2_2_1 = likert_question(
        "D2.2.1 Les durées opératoires réelles sont souvent très différentes des estimations.",
        "D2_2_1",
    )
    D2_2_2 = likert_question(
        "D2.2.2 Les interventions d’une même famille d’actes présentent une forte variabilité de durée.",
        "D2_2_2",
    )
    D2_2_3 = likert_question(
        "D2.2.3 Les temps d’installation et de sortie de salle sont eux-mêmes très variables.",
        "D2_2_3",
    )
    D2_2_4 = likert_question(
        "D2.2.4 Les temps d’installation/ réveil/ transfertsont pris en compte dans la programmation .",
        "D2_2_4",
    )

    D3 = st.selectbox(
        "D.3. Dans votre bloc, actualise-t-on régulièrement les estimations de durée en fonction des données observées ?",
        [
            "Oui, de façon systématique",
            "Oui, mais de façon informelle",
            "Rarement",
            "Jamais",
        ],
        key="D3",
    )

    D4 = st.selectbox(
        "D.4. À partir de quel niveau d’écart de durée (par rapport au prévu) estimez-vous que cela "
        "perturbe fortement le programme ?",
        ["> 15 min", "> 30 min", "> 60 min", "> 90 min"],
        key="D4",
    )
    D5 = st.selectbox(
        "D.5. Lorsque une intervention dépasse largement sa durée prévue, l'ajustement est généralement de :",
        ["Décalage des interventions suivantes dans la même salle", "Déplacement d'interventions vers d'autres salles", "Annulation/report de certaines interventions", "Heures supplémentaires"],
        key="D5",
    )
    D6 = st.selectbox(
        "D.6. Lorsque une intervention dure moins longtemps que prévu, vous:",
        ["Profitez pour commencer plus tôt l'intervention suivante", "Restez souvent avec du temps perdu", "Ajoutez parfois des patients supplémentaires (liste d'attente, patients prêts)"],
        key="D6",
    )

    D_commentaires = st.text_area(
        "Commentaires sur les durées opératoires :",
        key="D_commentaires",
    )

    # ==============================================================
    # E. Gestion des urgences et des imprévus
    # ==============================================================

    st.header("E. Gestion des urgences et des imprévus")
    st.subheader("E1. Arrivée des cas urgents")

    E1_1 = st.selectbox(
        "E1.1. Le flux d’urgences au bloc est :",
        ["Faible", "Modéré", "Important", "Très important"],
        key="E1_1",
    )

    E1_2 = st.selectbox(
        "E1.2. Vous disposez d’une salle dédiée aux urgences :",
        ["Oui en permanence", "Oui à certaines plages horaires", "Non"],
        key="E1_2",
    )
    E1_3 = st.selectbox(
        "E1.3. Existe-t-il des créneaux réservés aux urgences sur certaines salles? :",
        ["Oui", "Non"],
        key="E1_3",
    )

    st.markdown(
        "E1.3. En pratique, lorsque survient une urgence nécessitant une salle "
        "(notez chaque pratique, échelle 1–5) :"
    )

    E1_3_1 = likert_question("E1.3.1 On utilise la salle d’urgence si disponible.", "E1_3_1")
    E1_3_2 = likert_question("E1.3.2 On reporte ou annule une intervention élective prévue.", "E1_3_2")
    E1_3_3 = likert_question("E1.3.3 On crée de l’heure supplémentaire (dépassement de programme).", "E1_3_3")
    E1_3_4 = likert_question("E1.3.4 On décale les interventions suivantes dans la même salle.", "E1_3_4")

    E1_4 = likert_question(
        "E1.4. Il existe des règles explicites pour choisir quelle intervention élective sera décalée / annulée "
        "lorsqu’une urgence arrive.",
        "E1_4",
    )
    E1_4_details = st.text_area(
        "Si oui, lesquelles ?",
        key="E1_4_details",
    )

    st.subheader("E2. Autres perturbations (pannes, absences, patients)")

    st.markdown("E2.5. Fréquence (échelle 1–5) des perturbations suivantes dans votre bloc :")

    E2_5_1 = likert_question(
        "E2.5.1 Annulation de patient le jour J (problème médical, administratif, absence).",
        "E2_5_1",
    )
    E2_5_2 = likert_question("E2.5.2 Retard de patient.", "E2_5_2")
    E2_5_3 = likert_question("E2.5.3 Absence ou retard de chirurgien.", "E2_5_3")
    E2_5_4 = likert_question("E2.5.4 Absence ou retard de personnel paramédical.", "E2_5_4")
    E2_5_5 = likert_question("E2.5.5 Panne / indisponibilité d’un équipement critique.", "E2_5_5")

    E2_6 = st.selectbox(
        "E2.6. Lorsqu’une perturbation majeure survient, la replanification est :",
        [
            "Centralisée (responsable de bloc / régulateur prend la décision)",
            "Décidée principalement par les chirurgiens concernés",
            "Résultat de négociations informelles",
            "Autre",
        ],
        key="E2_6",
    )
    E2_6_autre = ""
    if E2_6 == "Autre":
        E2_6_autre = st.text_input("Préciser :", key="E2_6_autre")

    E2_7 = likert_question(
        "E2.7. La replanification en cours de journée suit des règles (ou algorithmes) de décision clairs "
        "(par exemple « minimiser les retards », « prioriser les cas lourds », etc.).",
        "E2_7",
    )
    E_commentaires = st.text_area(
        "Commentaires sur la gestion des urgences et des imprévus :",
        key="E_commentaires",
    )

    # ==============================================================
    # F. Processus de replanification / réorchestration en temps réel
    # ==============================================================

    st.header("F. Processus de replanification / réorchestration en temps réel")

    st.markdown("F.1. En cours de journée, il vous arrive de (échelle 1–5) :")

    F1_1_1 = likert_question(
        "F1.1.1 Changer l’ordre des interventions dans une même salle.",
        "F1_1_1",
    )
    F1_1_2 = likert_question(
        "F1.1.2 Transférer une intervention d’une salle à une autre.",
        "F1_1_2",
    )
    F1_1_3 = likert_question(
        "F1.1.3 Modifier l’équipe opératoire (chirurgien, IADE, IDE, etc.).",
        "F1_1_3",
    )
    F1_1_4 = likert_question(
        "F1.1.4 Avancer ou retarder une intervention d’une autre journée.",
        "F1_1_4",
    )

    st.markdown(
        "F.2. La décision de replanifier pendant la journée vise principalement à "
        "(échelle 1–5 pour chaque objectif) :"
    )

    F1_2_1 = likert_question("F1.2.1 Éviter les annulations de patients.", "F1_2_1")
    F1_2_2 = likert_question("F1.2.2 Limiter les retards de fin de programme (heures supplémentaires).", "F1_2_2")
    F1_2_3 = likert_question("F1.2.3 Optimiser l’utilisation des salles.", "F1_2_3")
    F1_2_4 = likert_question("F1.2.4 Garantir l’accès au bloc pour les urgences.", "F1_2_4")
    F1_2_5 = likert_question("F1.2.5 Protéger les équipes de jours trop chargés.", "F1_2_5")

    st.markdown("F.3. Estimez (échelle 1–5) :")

    F1_3_1 = likert_question(
        "F1.3.1 Le processus de replanification est plutôt réactif (on s’adapte au fur et à mesure).",
        "F1_3_1",
    )
    F1_3_2 = likert_question(
        "F1.3.2 On dispose d’outils de visualisation en temps réel (tableaux, logiciels) pour suivre l’état du bloc.",
        "F1_3_2",
    )
    F1_3_3 = likert_question(
        "F1.3.3 On pourrait bénéficier d’un outil d’aide à la décision pour proposer des scénarios de replanification.",
        "F1_3_3",
    )

    F_commentaires = st.text_area(
        "Commentaires sur la replanification en temps réel :",
        key="F_commentaires",
    )

    # ==============================================================
    # G. Objectifs, indicateurs et compromis
    # ==============================================================

    st.header("G. Objectifs, indicateurs et compromis")

    st.markdown(
        "G.1. Parmi les objectifs suivants, indiquez ceux qui sont réellement prioritaires dans votre bloc "
        "(échelle 1–5) :"
    )

    G1_1_1 = likert_question("G1.1.1 Taux d’occupation des salles.", "G1_1_1")
    G1_1_2 = likert_question("G1.1.2 Réduction des heures supplémentaires.", "G1_1_2")
    G1_1_3 = likert_question("G1.1.3 Réduction du nombre d’interventions annulées.", "G1_1_3")
    G1_1_4 = likert_question("G1.1.4 Réduction des délais d’attente des patients.", "G1_1_4")
    G1_1_5 = likert_question("G1.1.5 Respect des horaires du personnel.", "G1_1_5")
    G1_1_6 = likert_question("G1.1.6 Équité entre services / chirurgiens.", "G1_1_6")
    G1_1_7 = likert_question("G1.1.7 Qualité / sécurité des soins.", "G1_1_7")

    st.markdown(
        "G.2. Dans les décisions de planification ou replanification, les compromis suivants sont fréquents "
        "(échelle 1–5) :"
    )

    G1_2_1 = likert_question(
        "G1.2.1 Accepter plus d’heures supplémentaires pour éviter d’annuler des patients.",
        "G1_2_1",
    )
    G1_2_2 = likert_question(
        "G1.2.2 Annuler des interventions pour respecter strictement les horaires de fermeture.",
        "G1_2_2",
    )
    G1_2_3 = likert_question(
        "G1.2.3 Limiter la charge d’un chirurgien au détriment de l’utilisation des salles.",
        "G1_2_3",
    )

    G3 = st.selectbox(
        "G.3. Disposez-vous de tableaux de bord ou indicateurs formels de performance du bloc ?",
        [
            "Oui, consultés régulièrement",
            "Oui, mais peu utilisés",
            "Non",
        ],
        key="G3",
    )

    G_commentaires = st.text_area(
        "Commentaires sur les objectifs, indicateurs et compromis :",
        key="G_commentaires",
    )

    # ==============================================================
    # H. Représentation de la réalité par des modèles
    # ==============================================================

    st.header("H. Représentation de la réalité par des modèles")

    st.markdown(
        "Pour les questions suivantes, indiquez dans quelle mesure cela reflète votre réalité quotidienne "
        "(échelle 1–5)."
    )

    H1 = likert_question(
        "H.1. Il est raisonnable de considérer les salles opératoires comme des ressources à capacité limitée, "
        "où une seule intervention peut être réalisée à la fois.",
        "H1",
    )
    H2 = likert_question(
        "H.2. Il est raisonnable de considérer les chirurgiens comme des ressources critiques, qui ne peuvent "
        "pas être présents dans deux salles simultanément.",
        "H2",
    )
    H3 = likert_question(
        "H.3. Les lits de réveil / SSPI peuvent être considérés comme une ressource goulot qui conditionne "
        "l’ordre et le timing des interventions.",
        "H3",
    )
    H4 = likert_question(
        "H.4. Le flux des patients (du préopératoire vers le bloc, puis vers le réveil et les services) peut être "
        "représenté comme une succession d’étapes bien définies (préparation, intervention, réveil, transfert, etc.).",
        "H4",
    )
    H5 = likert_question(
        "H.5. Les règles utilisées (priorités, replanification, gestion des urgences) sont suffisamment stables "
        "dans le temps pour être traduites dans un modèle formel.",
        "H5",
    )
    H6 = likert_question(
        "H.6. Un modèle qui tient compte des ressources goulots (salles, chirurgiens, lits de réveil) et des "
        "variations de durée opératoire pourrait réellement aider à décider du programme et de sa replanification.",
        "H6",
    )
    H7 = likert_question(
        "H.7. Un outil de simulation permettant de tester différents scénarios "
        "(organisation, règles de priorité, ressources supplémentaires, etc.) serait utile pour votre bloc.",
        "H7",
    )

    st.markdown(
        "H.8. Les propositions issues d’un modèle d’aide à la décision seraient acceptables si "
        "(notez chaque item, échelle 1–5) :"
    )

    H1_8_1 = likert_question(
        "H1.8.1 Elles sont transparentes (explication des règles et résultats).",
        "H1_8_1",
    )
    H1_8_2 = likert_question(
        "H1.8.2 Elles tiennent compte des contraintes médicales et humaines.",
        "H1_8_2",
    )
    H1_8_3 = likert_question(
        "H1.8.3 Elles laissent une marge de décision au responsable de bloc / aux chirurgiens.",
        "H1_8_3",
    )

    H_commentaires = st.text_area(
        "Commentaires sur la représentation « modèle vs réalité » :",
        key="H_commentaires",
    )

    # ==============================================================
    # I. Questions ouvertes finales
    # ==============================================================

    st.header("I. Questions ouvertes finales")

    I1 = st.text_area(
        "I.1. Selon vous, quels sont les principaux écarts entre la manière dont le bloc fonctionne en "
        "théorie (procédures écrites) et en pratique (ce qui se passe réellement) ?",
        key="I1",
    )

    I2_1 = st.text_input(
        "I.2.1 Principale source de perturbation (1) :", key="I2_1"
    )
    I2_2 = st.text_input(
        "I.2.2 Principale source de perturbation (2) :", key="I2_2"
    )
    I2_3 = st.text_input(
        "I.2.3 Principale source de perturbation (3) :", key="I2_3"
    )

    I3 = st.text_area(
        "I.3. Si vous aviez un outil idéal d’aide à la décision pour la programmation et la replanification du bloc, "
        "que devrait-il faire en priorité ?",
        key="I3",
    )

    I4 = st.text_area(
        "I.4. Y a-t-il un élément important de votre pratique quotidienne que ce questionnaire n’a pas abordé "
        "et que vous jugez essentiel pour refléter la réalité du bloc ?",
        key="I4",
    )

    # ==============================================================
    # SOUMISSION
    # ==============================================================

    submitted = st.form_submit_button("Envoyer mes réponses")

    if submitted:
        # --- 1) Vérification des questions fermées obligatoires (échelle 1–5) ---
        likert_values = [
            B1_3_1, B1_3_2, B1_3_3,
            B2_4_1, B2_4_2, B2_4_3, B2_4_4, B2_4_5, B2_4_6, B2_4_7, B2_4_8,
            B2_6,
            C2_4, C2_5,
            C3_7, C3_8, C3_9,
            D2_2_1, D2_2_2, D2_2_3,D2_2_4,
            E1_3_1, E1_3_2, E1_3_3,E1_3_4, E1_4,
            E2_5_1, E2_5_2, E2_5_3, E2_5_4, E2_5_5, E2_7,
            F1_1_1, F1_1_2, F1_1_3, F1_1_4,
            F1_2_1, F1_2_2, F1_2_3, F1_2_4, F1_2_5,
            F1_3_1, F1_3_2, F1_3_3,
            G1_1_1, G1_1_2, G1_1_3, G1_1_4, G1_1_5, G1_1_6, G1_1_7,
            G1_2_1, G1_2_2, G1_2_3,
            H1, H2, H3, H4, H5, H6, H7,
            H1_8_1, H1_8_2, H1_8_3,
        ]

        if any(v == 0 for v in likert_values):
            st.error(
                "Certaines questions fermées n'ont pas encore été renseignées "
                "(curseur resté sur 0). "
                "Merci de répondre à toutes les questions à échelle avant d'envoyer."
            )
        elif prenom.strip() == "" or nom.strip() == "":
            st.error("Merci de renseigner votre nom et votre prénom.")
        else:
            # --- 2) Tout est rempli → on enregistre ---

            data = {
                "timestamp": datetime.now().isoformat(),
                "prenom": prenom,
                "nom": nom,

                # A
                "A1_fonction": A1,
                "A1_autre": A1_autre,
                "A2_specialite": A2,
                "A3_type_etab": A3,
                "A3_autre": A3_autre,
                "A4_nb_salles": A4,
                "A5_nb_interventions_jour": A5,
                "A6_DébutP": A6,
                "A7_FinP": A7,

                # B
                "B1_1_horizon_programme": B1_1,
                "B1_2_modifs_majeures": B1_2,
                "B1_3_1_respect_programme": B1_3_1,
                "B1_3_2_procedure_formalisee": B1_3_2,
                "B1_3_3_integration_indispo": B1_3_3,
                "B2_4_1_urgence": B2_4_1,
                "B2_4_2_duree": B2_4_2,
                "B2_4_3_disp_chir": B2_4_3,
                "B2_4_4_disp_anesth": B2_4_4,
                "B2_4_5_lits": B2_4_5,
                "B2_4_6_equipement": B2_4_6,
                "B2_4_7_contraintes_patient": B2_4_7,
                "B2_4_8_equite": B2_4_8,
                "B2_5_ordre_interventions": B2_5,
                "B2_5_autre": B2_5_autre,
                "B2_6_regles_non_ecrites": B2_6,
                "B2_6_exemples": B2_6_exemples,
                "B_commentaires": B_commentaires,

                # C
                "C1_1_capacite_salles": C1_1,
                "C1_2_temps_entre_interv": C1_2,
                "C1_3_variabilite_temps": C1_3,
                "C2_4_chir_plusieurs_salles": C2_4,
                "C2_5_gestion_conflits": C2_5,
                "C2_6_changements_chir": C2_6,
                "C3_7_manque_lits_reveil": C3_7,
                "C3_8_anticipation_lits_aval": C3_8,
                "C3_9_regles_priorisation_lits": C3_9,
                "C3_9_details": C3_9_details,
                "C_commentaires": C_commentaires,

                # D
                "D1_sources_durees": "; ".join(D1),
                "D1_autre": D1_autre,
                "D2_2_1_ecart_estimations": D2_2_1,
                "D2_2_2_variabilite_famille": D2_2_2,
                "D2_2_3_variabilite_install_sortie": D2_2_3,
                "D2_2_4_Prisedestemps": D2_2_4,
                "D3_actualisation_durees": D3,
                "D4_seuil_perturbation": D4,
                "D5_Durée_longue": D5,
                "D6_Durée_moins": D6,
                "D_commentaires": D_commentaires,

                # E
                "E1_1_flux_urgences": E1_1,
                "E1_2_salle_urgences": E1_2,
                "E1_3_Crébeaux_réservés": E1_3,
                "E1_3_1_utilisation_salle_urgence": E1_3_1,
                "E1_3_2_annulation_elective": E1_3_2,
                "E1_3_3_heures_sup": E1_3_3,
                "E1_3_'_Décalage_salle": E1_3_4,
                "E1_4_regles_choix_decalage": E1_4,
                "E1_4_details": E1_4_details,
                "E2_5_1_annulation_patient": E2_5_1,
                "E2_5_2_retard_patient": E2_5_2,
                "E2_5_3_absence_chirurgien": E2_5_3,
                "E2_5_4_absence_paramedical": E2_5_4,
                "E2_5_5_panne_equipement": E2_5_5,
                "E2_6_mode_replanification": E2_6,
                "E2_6_autre": E2_6_autre,
                "E2_7_regles_decision_claires": E2_7,
                "E_commentaires": E_commentaires,

                # F
                "F1_1_1_changer_ordre": F1_1_1,
                "F1_1_2_transferer_salle": F1_1_2,
                "F1_1_3_modifier_equipe": F1_1_3,
                "F1_1_4_avancer_retarder_journee": F1_1_4,
                "F1_2_1_eviter_annulations": F1_2_1,
                "F1_2_2_limite_heures_sup": F1_2_2,
                "F1_2_3_optimiser_salles": F1_2_3,
                "F1_2_4_garantir_acces_urgences": F1_2_4,
                "F1_2_5_proteger_equipes": F1_2_5,
                "F1_3_1_processus_reactif": F1_3_1,
                "F1_3_2_outils_temps_reel": F1_3_2,
                "F1_3_3_besoin_outil_decision": F1_3_3,
                "F_commentaires": F_commentaires,

                # G
                "G1_1_1_taux_occupation": G1_1_1,
                "G1_1_2_reduction_heures_sup": G1_1_2,
                "G1_1_3_reduction_annulations": G1_1_3,
                "G1_1_4_reduction_delais_attente": G1_1_4,
                "G1_1_5_respect_horaires_personnel": G1_1_5,
                "G1_1_6_equite_services": G1_1_6,
                "G1_1_7_qualite_securite": G1_1_7,
                "G1_2_1_accepter_heures_sup": G1_2_1,
                "G1_2_2_annuler_pour_horaires": G1_2_2,
                "G1_2_3_limite_charge_chirurgien": G1_2_3,
                "G3_tableaux_de_bord": G3,
                "G_commentaires": G_commentaires,

                # H
                "H1_salles_ressources_limitees": H1,
                "H2_chirurgiens_ressources_critiques": H2,
                "H3_lits_reveil_goulot": H3,
                "H4_flux_patient_etapes": H4,
                "H5_regles_stables": H5,
                "H6_modele_aide_programme": H6,
                "H7_outil_simulation": H7,
                "H1_8_1_transparence": H1_8_1,
                "H1_8_2_contraintes_med_humaines": H1_8_2,
                "H1_8_3_marge_decision": H1_8_3,
                "H_commentaires": H_commentaires,

                # I
                "I1_ecarts_theorie_pratique": I1,
                "I2_1_source_perturbation": I2_1,
                "I2_2_source_perturbation": I2_2,
                "I2_3_source_perturbation": I2_3,
                "I3_outil_ideal": I3,
                "I4_element_non_aborde": I4,
            }

            new_row = pd.DataFrame([data])

            if os.path.exists(EXCEL_FILE):
                df = pd.read_excel(EXCEL_FILE)
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                df = new_row

            df.to_excel(EXCEL_FILE, index=False)

            st.success("Merci ! Vos réponses ont été enregistrées.")
            st.info(f"Les réponses sont stockées dans le fichier : {EXCEL_FILE}")
