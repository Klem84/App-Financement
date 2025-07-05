from modeles import (
    Aide, TypeAide, NatureProjet, TypeStructureEntreprise,
    SecteurActivite, TailleEntreprise, LocalisationEntreprise
)
from datetime import datetime

# Conversion des dates string en objets datetime
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None

aides_simulees = [
    Aide(
        id_aide="france_relance_indus_01", # ID en str
        nom="France Relance - Investissement Industrie",
        organisme_financeur="Bpifrance", # Champ renommé
        description_courte="Soutien à l'investissement productif dans l’industrie.",
        lien_officiel="https://www.bpifrance.fr/nos-solutions/france-relance-industrie", # Champ renommé
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.INVESTISSEMENT_MATERIEL], # Champ renommé et utilise Enum
        secteurs_eligibles=[SecteurActivite.INDUSTRIE], # Champ renommé et utilise Enum
        localisations_concernees=[LocalisationEntreprise.HAUTS_DE_FRANCE], # Champ renommé et utilise Enum
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE], # Utilise Enum
        tailles_entreprise_eligibles=[TailleEntreprise.PME, TailleEntreprise.ETI], # Nouveau champ et utilise Enum
        montant_max_aide=800000.0, # Champ renommé
        taux_aide=None,
        date_limite_depot=parse_date("2025-12-31"), # Champ renommé et converti
        conditions_eligibilite="Projet situé en Hauts-de-France.", # Champ renommé
        depenses_eligibles=["Machines", "Outils", "Travaux d’aménagement"],
        mots_cles=["industrie", "investissement", "hauts-de-france", "production"]
    ),
    Aide(
        id_aide="ademe_innov_pme_02",
        nom="AAP Innovation PME",
        organisme_financeur="ADEME",
        description_courte="Aide à l’innovation pour les PME du secteur environnemental.",
        lien_officiel="https://www.ademe.fr/aap-innovation-pme",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.INNOVATION],
        secteurs_eligibles=[SecteurActivite.ENVIRONNEMENT],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE],
        tailles_entreprise_eligibles=[TailleEntreprise.STARTUP, TailleEntreprise.PME],
        montant_max_aide=500000.0,
        taux_aide="jusqu'à 60%", # Ajouté pour correspondre au modèle
        date_limite_depot=parse_date("2025-09-15"),
        conditions_eligibilite="Innovation à fort impact environnemental.",
        depenses_eligibles=["Études", "Prototypage", "Tests"],
        trl_min=3, # Ajouté pour exemple
        trl_max=7, # Ajouté pour exemple
        mots_cles=["innovation", "pme", "environnement", "ademe", "prototype"]
    ),
    Aide(
        id_aide="cir_eco_03",
        nom="Crédit d’impôt recherche (CIR)",
        organisme_financeur="Ministère de l'Économie",
        description_courte="Crédit d’impôt pour les dépenses de R&D.",
        lien_officiel="https://www.economie.gouv.fr/cedef/credit-impot-recherche",
        type_aide=TypeAide.CREDIT_IMPOT,
        natures_projet_eligibles=[NatureProjet.INNOVATION],
        secteurs_eligibles=[SecteurActivite.TOUS],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE],
        tailles_entreprise_eligibles=[TailleEntreprise.TPE, TailleEntreprise.PME, TailleEntreprise.ETI, TailleEntreprise.GRANDE],
        montant_max_aide=None, # Pas de montant max direct pour CIR
        taux_aide="30% (ou 50% DOM)",
        date_limite_depot=None, # Permanent
        conditions_eligibilite="Activités éligibles selon le BOFIP.",
        depenses_eligibles=["Salaires chercheurs", "Sous-traitance R&D", "Brevets"],
        mots_cles=["cir", "recherche", "développement", "innovation", "impôt"]
    ),
    Aide(
        id_aide="ademe_fonds_chaleur_04",
        nom="Fonds chaleur - ADEME",
        organisme_financeur="ADEME",
        description_courte="Aide pour la production de chaleur renouvelable.",
        lien_officiel="https://www.ademe.fr/fonds-chaleur",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.TRANSITION_ECOLOGIQUE, NatureProjet.INVESTISSEMENT_MATERIEL],
        secteurs_eligibles=[SecteurActivite.ENERGIE, SecteurActivite.INDUSTRIE, SecteurActivite.AGRICULTURE, SecteurActivite.CONSTRUCTION],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE, TypeStructureEntreprise.COLLECTIVITE],
        tailles_entreprise_eligibles=[TailleEntreprise.PME, TailleEntreprise.ETI, TailleEntreprise.GRANDE],
        montant_max_aide=300000.0, # Exemple, peut varier fortement
        taux_aide="jusqu'à 50%",
        date_limite_depot=parse_date("2025-10-01"),
        conditions_eligibilite="Investissement dans la chaleur renouvelable (biomasse, géothermie, solaire thermique).",
        depenses_eligibles=["Chaudières biomasse", "Réseaux de chaleur", "Installations géothermiques"],
        budget_min_projet=50000.0, # Ajouté pour exemple
        mots_cles=["fonds chaleur", "ademe", "énergie renouvelable", "biomasse", "géothermie"]
    ),
    Aide(
        id_aide="france_travail_jeunes_05",
        nom="Plan de relance - Recrutement jeunes",
        organisme_financeur="France Travail",
        description_courte="Prime pour l’embauche de jeunes de moins de 26 ans.",
        lien_officiel="https://www.francetravail.fr/plan-jeunes",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.RECRUTEMENT],
        secteurs_eligibles=[SecteurActivite.TOUS],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE, TypeStructureEntreprise.ASSOCIATION],
        tailles_entreprise_eligibles=[TailleEntreprise.TPE, TailleEntreprise.PME, TailleEntreprise.ETI], # CIR s'applique aussi aux ETI
        montant_max_aide=4000.0, # Montant typique de la prime 1 jeune 1 solution
        taux_aide=None, # C'est un forfait
        date_limite_depot=parse_date("2025-07-31"), # Exemple, vérifier dates réelles
        conditions_eligibilite="Contrat d’au moins 3 mois, jeune de moins de 26 ans.",
        depenses_eligibles=["Salaires", "Charges sociales"],
        nb_etp_max_entreprise=249, # Souvent pour PME
        mots_cles=["recrutement", "jeunes", "emploi", "prime", "france travail"]
    ),
    Aide(
        id_aide="ademe_fonds_friche_06",
        nom="Fonds friche – ADEME",
        organisme_financeur="ADEME",
        description_courte="Aide à la réhabilitation de friches industrielles ou urbaines.",
        lien_officiel="https://www.ademe.fr/fonds-friches",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.INVESTISSEMENT_MATERIEL, NatureProjet.TRANSITION_ECOLOGIQUE],
        secteurs_eligibles=[SecteurActivite.TOUS], # Large éligibilité
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE, TypeStructureEntreprise.COLLECTIVITE],
        tailles_entreprise_eligibles=[TailleEntreprise.PME, TailleEntreprise.ETI, TailleEntreprise.GRANDE],
        montant_max_aide=1000000.0, # Peut être élevé
        taux_aide="variable",
        date_limite_depot=parse_date("2026-01-31"),
        conditions_eligibilite="Le projet doit être prêt à démarrer sous 12 mois. Concerne la reconversion de sites pollués ou abandonnés.",
        depenses_eligibles=["Déconstruction", "Dépollution", "Aménagement", "Études de faisabilité"],
        mots_cles=["friche", "ademe", "réhabilitation", "dépollution", "aménagement urbain"]
    ),
    Aide(
        id_aide="dreets_fne_formation_07",
        nom="FNE-Formation",
        organisme_financeur="DREETS (via OPCO)",
        description_courte="Aide pour la formation des salariés sur les compétences d’avenir.",
        lien_officiel="https://travail-emploi.gouv.fr/formation-professionnelle/fne-formation",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.FORMATION],
        secteurs_eligibles=[SecteurActivite.TOUS],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE, TypeStructureEntreprise.ASSOCIATION],
        tailles_entreprise_eligibles=[TailleEntreprise.TPE, TailleEntreprise.PME, TailleEntreprise.ETI],
        montant_max_aide=None, # Souvent un % des coûts pédagogiques
        taux_aide="jusqu'à 70%", # Variable selon taille et situation
        date_limite_depot=parse_date("2025-12-31"), # Souvent des campagnes annuelles
        conditions_eligibilite="Formation liée à la transition numérique, écologique, ou aux mutations économiques. Concerne les salariés en activité partielle ou entreprises en difficulté, mais aussi plus largement.",
        depenses_eligibles=["Frais pédagogiques", "Temps de formation salarié (parfois)"],
        mots_cles=["fne", "formation", "compétences", "dreets", "opco", "transition"]
    ),
    Aide(
        id_aide="franceagrimer_decarbon_08",
        nom="Prime Agri-Décarbonation",
        organisme_financeur="FranceAgriMer",
        description_courte="Soutien aux projets agricoles réduisant les émissions de GES.",
        lien_officiel="https://www.franceagrimer.fr/Accompagner/Aides-nationales/Prime-Agri-Decarbonation",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.TRANSITION_ECOLOGIQUE, NatureProjet.INVESTISSEMENT_MATERIEL],
        secteurs_eligibles=[SecteurActivite.AGRICULTURE],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE, TypeStructureEntreprise.PERSONNE_PHYSIQUE], # Agriculteurs
        tailles_entreprise_eligibles=[TailleEntreprise.TPE, TailleEntreprise.PME], # Exploitations agricoles
        montant_max_aide=200000.0,
        taux_aide="jusqu'à 40%",
        date_limite_depot=parse_date("2025-11-30"),
        conditions_eligibilite="Matériel ou technique réduisant les intrants ou les émissions directes. Plan de décarbonation.",
        depenses_eligibles=["Matériel économe en énergie", "Études de réduction GES", "Méthanisation"],
        mots_cles=["agriculture", "décarbonation", "ges", "franceagrimer", "environnement"]
    ),
    Aide(
        id_aide="region_idf_cheque_num_09",
        nom="Chèque Numérique TPE IDF",
        organisme_financeur="Région Île-de-France",
        description_courte="Chèque pour financer les premiers investissements numériques des TPE franciliennes.",
        lien_officiel="https://www.iledefrance.fr/cheque-numerique",
        type_aide=TypeAide.SUBVENTION,
        natures_projet_eligibles=[NatureProjet.TRANSITION_NUMERIQUE, NatureProjet.INVESTISSEMENT_IMMATERIEL],
        secteurs_eligibles=[SecteurActivite.TOUS], # Souvent artisans, commerçants
        localisations_concernees=[LocalisationEntreprise.ILE_DE_FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE],
        tailles_entreprise_eligibles=[TailleEntreprise.TPE],
        montant_max_aide=1500.0,
        taux_aide=None, # Forfaitaire
        date_limite_depot=parse_date("2025-10-01"), # Souvent des campagnes avec budgets limités
        conditions_eligibilite="Entreprise de moins de 10 salariés, située en Île-de-France. Ne pas avoir déjà bénéficié.",
        depenses_eligibles=["Création site web", "Logiciels de gestion", "Publicité en ligne", "Matériel informatique (partiellement)"],
        nb_etp_max_entreprise=10,
        ca_max_entreprise=2000000.0, # Exemple de critère TPE
        mots_cles=["numérique", "tpe", "digitalisation", "site web", "ile-de-france", "région"]
    ),
    Aide(
        id_aide="ademe_aap_recyclage_10",
        nom="AAP - Recyclage & Économie circulaire",
        organisme_financeur="ADEME",
        description_courte="Soutien aux projets innovants dans le recyclage des matériaux.",
        lien_officiel="https://www.ademe.fr/aap-recyclage-economie-circulaire",
        type_aide=TypeAide.SUBVENTION, # Peut aussi être Avance Remboursable
        natures_projet_eligibles=[NatureProjet.INNOVATION, NatureProjet.INVESTISSEMENT_MATERIEL],
        secteurs_eligibles=[SecteurActivite.ENVIRONNEMENT, SecteurActivite.INDUSTRIE],
        localisations_concernees=[LocalisationEntreprise.FRANCE],
        porteurs_eligibles=[TypeStructureEntreprise.ENTREPRISE],
        tailles_entreprise_eligibles=[TailleEntreprise.PME, TailleEntreprise.ETI],
        montant_max_aide=600000.0,
        taux_aide="jusqu'à 55%",
        date_limite_depot=parse_date("2025-09-30"),
        conditions_eligibilite="Le projet doit améliorer significativement un process de valorisation ou développer de nouvelles filières.",
        depenses_eligibles=["Études de faisabilité", "Pilotes industriels", "Matériel de tri et traitement", "R&D"],
        trl_min=5,
        trl_max=8,
        budget_min_projet=100000.0,
        mots_cles=["recyclage", "économie circulaire", "ademe", "déchets", "valorisation", "innovation"]
    )
]
