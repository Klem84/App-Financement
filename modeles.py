from enum import Enum
from datetime import datetime

class RoleUtilisateur(Enum):
    CONSULTANT = "Consultant"
    CLIENT = "Client"
    ADMIN = "Admin"

class TypeOrganisation(Enum):
    CABINET = "Cabinet"
    CLIENT_FINAL = "Client final"

class StatutPipelineProjet(Enum):
    IDEE = "Idée"
    ELIGIBILITE = "Eligibilité"
    REDACTION = "Rédaction"
    DEPOT = "Dépôt"
    SUIVI = "Suivi"

class TypeLivrable(Enum):
    PRE_DIAGNOSTIC = "Pré-diagnostic"
    CIR = "CIR"
    ADEME = "ADEME"
    # Ajouter d'autres types au besoin

class StatutValidationLivrable(Enum):
    BROUILLON = "Brouillon"
    VALIDE = "Validé"
    A_REVOIR = "À revoir"

# Les classes seront ajoutées ici dans les étapes suivantes

class Utilisateur:
    def __init__(self, id_utilisateur: str, nom: str, email: str, role: RoleUtilisateur, organisation = None, derniere_connexion: datetime = None):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.email = email
        self.role = role
        self.organisation = organisation  # Sera un objet Organisation
        self.projets_associes = []  # Liste d'objets Projet
        self.derniere_connexion = derniere_connexion

    def __repr__(self):
        return f"<Utilisateur {self.nom} ({self.role.value})>"

class Organisation:
    def __init__(self, id_organisation: str, nom: str, type_org: TypeOrganisation):
        self.id_organisation = id_organisation
        self.nom = nom
        self.type_org = type_org
        self.utilisateurs = []  # Liste d'objets Utilisateur
        self.projets = []  # Liste d'objets Projet

    def __repr__(self):
        return f"<Organisation {self.nom} ({self.type_org.value})>"

class Livrable:
    def __init__(self, id_livrable: str, type_livrable: TypeLivrable, fichier_associe: str, projet_parent = None, cree_par = None, statut_validation: StatutValidationLivrable = StatutValidationLivrable.BROUILLON, date_generation: datetime = None):
        self.id_livrable = id_livrable
        self.type_livrable = type_livrable
        self.fichier_associe = fichier_associe # Simule le chemin du fichier
        self.projet_parent = projet_parent # Sera un objet Projet
        self.cree_par = cree_par # Sera un objet Utilisateur
        self.statut_validation = statut_validation
        self.date_generation = date_generation if date_generation else datetime.now()

    def __repr__(self):
        return f"<Livrable {self.type_livrable.value} ({self.id_livrable})>"

class Projet:
    def __init__(self, id_projet: str, titre_projet: str, organisation_cliente = None, consultant_referent = None, statut_pipeline: StatutPipelineProjet = StatutPipelineProjet.IDEE, date_creation: datetime = None, date_mise_a_jour: datetime = None):
        self.id_projet = id_projet
        self.titre_projet = titre_projet
        self.organisation_cliente = organisation_cliente # Sera un objet Organisation
        self.consultant_referent = consultant_referent # Sera un objet Utilisateur
        self.statut_pipeline = statut_pipeline
        self.aides_identifiees: list[Aide] = [] # Modifié pour stocker des objets Aide
        self.livrables = [] # Liste d'objets Livrable
        self.date_creation = date_creation if date_creation else datetime.now()
        self.date_mise_a_jour = date_mise_a_jour if date_mise_a_jour else datetime.now()

    def __repr__(self):
        return f"<Projet {self.titre_projet} ({self.id_projet})>"

# --- Énumérations et Classe pour le Module 2 : Recherche de Financements ---

class SecteurActivite(Enum):
    TOUS = "Tous secteurs"
    INDUSTRIE = "Industrie"
    ENVIRONNEMENT = "Environnement & Énergie"
    ENERGIE = "Énergie" # Peut être fusionné avec Environnement ou gardé séparé
    AGRICULTURE = "Agriculture & Agroalimentaire"
    NUMERIQUE = "Numérique & Tech"
    SERVICES = "Services"
    SANTE = "Santé"
    CONSTRUCTION = "Construction & BTP"
    COMMERCE = "Commerce & Distribution"
    TOURISME_CULTURE = "Tourisme, Culture & Loisirs"
    AUTRE = "Autre secteur"

class TailleEntreprise(Enum):
    TPE = "Très Petite Entreprise (moins de 10 salariés)"
    PME = "Petite et Moyenne Entreprise (10 à 249 salariés)"
    ETI = "Entreprise de Taille Intermédiaire (250 à 4999 salariés)"
    GRANDE = "Grande Entreprise (5000 salariés et plus)"
    STARTUP = "Start-up (souvent assimilée TPE/PME avec spécificités)"
    # ASSOCIATION peut aussi être une taille/catégorie si on ne la met pas dans TypeStructureEntreprise

class LocalisationEntreprise(Enum):
    FRANCE = "France entière"
    HAUTS_DE_FRANCE = "Hauts-de-France"
    ILE_DE_FRANCE = "Île-de-France"
    NOUVELLE_AQUITAINE = "Nouvelle-Aquitaine"
    OCCITANIE = "Occitanie"
    AUVERGNE_RHONE_ALPES = "Auvergne-Rhône-Alpes"
    PROVENCE_ALPES_COTE_DAZUR = "Provence-Alpes-Côte d'Azur"
    BRETAGNE = "Bretagne"
    NORMANDIE = "Normandie"
    PAYS_DE_LA_LOIRE = "Pays de la Loire"
    CENTRE_VAL_DE_LOIRE = "Centre-Val de Loire"
    BOURGOGNE_FRANCHE_COMTE = "Bourgogne-Franche-Comté"
    GRAND_EST = "Grand Est"
    CORSE = "Corse"
    GUADELOUPE = "Guadeloupe"
    MARTINIQUE = "Martinique"
    GUYANE = "Guyane"
    LA_REUNION = "La Réunion"
    MAYOTTE = "Mayotte"
    AUTRE_INTERNATIONAL = "Autre / International"


class TypeAide(Enum):
    SUBVENTION = "Subvention"
    AVANCE_REMBOURSABLE = "Avance remboursable"
    CREDIT_IMPOT = "Crédit d’impôt"
    GARANTIE = "Garantie"
    PRET_A_TAUX_ZERO = "Prêt à taux zéro" # Ajout possible
    AUTRE = "Autre"

class TypeStructureEntreprise(Enum):
    PME = "PME" # Petites et Moyennes Entreprises
    ETI = "ETI" # Entreprises de Taille Intermédiaire
    TPE = "TPE" # Très Petites Entreprises
    STARTUP = "Start-up"
    ASSOCIATION = "Association"
    GRAND_GROUPE = "Grand Groupe"
    COLLECTIVITE = "Collectivité territoriale"
    PERSONNE_PHYSIQUE = "Personne physique (entrepreneur individuel)"
    ENTREPRISE = "Entreprise (générique)" # Ajouté pour correspondre aux données fournies
    AUTRE = "Autre structure"


class NatureProjet(Enum):
    INVESTISSEMENT_MATERIEL = "Investissement matériel"
    INVESTISSEMENT_IMMATERIEL = "Investissement immatériel (logiciels, brevets)"
    INNOVATION = "Projet d’innovation (R&D)"
    RECRUTEMENT = "Recrutement / Création d'emploi"
    FORMATION = "Formation du personnel"
    EXPORT = "Développement à l'international / Export"
    TRANSITION_ECOLOGIQUE = "Transition écologique / Décarbonation"
    TRANSITION_NUMERIQUE = "Transformation numérique"
    CREATION_ENTREPRISE = "Création / Reprise d'entreprise"
    AUTRE = "Autre nature de projet"

class Aide:
    def __init__(
        self,
        id_aide: str, # Changé en str pour plus de flexibilité (ex: "bpifrance_subv_innov_001")
        nom: str,
        organisme_financeur: str, # Renommé pour clarté
        lien_officiel: str, # Renommé pour clarté
        type_aide: TypeAide,
        description_courte: str, # Ajout pour affichage résumé
        montant_max_aide: float = None, # Renommé et Optional par défaut
        taux_aide: str = None, # Ex: "jusqu'à 50%" ou "forfaitaire"
        date_limite_depot: datetime = None, # Renommé et Optional par défaut
        porteurs_eligibles: list[TypeStructureEntreprise] = None,
        secteurs_eligibles: list[SecteurActivite] = None, # Modifié pour utiliser l'Enum
        localisations_concernees: list[LocalisationEntreprise] = None, # Modifié pour utiliser l'Enum
        tailles_entreprise_eligibles: list[TailleEntreprise] = None, # Ajouté et utilise l'Enum
        trl_min: int = None,
        trl_max: int = None,
        natures_projet_eligibles: list[NatureProjet] = None,
        budget_min_projet: float = None, # Renommé pour clarté
        budget_max_projet: float = None, # Renommé pour clarté
        nb_etp_min_entreprise: int = None, # Renommé pour clarté
        nb_etp_max_entreprise: int = None, # Renommé pour clarté
        ca_min_entreprise: float = None, # Renommé pour clarté
        ca_max_entreprise: float = None, # Renommé pour clarté
        depenses_eligibles: list[str] = None, # Ex: ["Salaires", "Matériel", "Prestations externes"]
        conditions_eligibilite: str = None, # Texte libre plus détaillé
        mots_cles: list[str] = None # Ajout pour recherche par mot-clé
    ):
        self.id_aide = id_aide
        self.nom = nom
        self.organisme_financeur = organisme_financeur
        self.lien_officiel = lien_officiel
        self.type_aide = type_aide
        self.description_courte = description_courte
        self.montant_max_aide = montant_max_aide
        self.taux_aide = taux_aide
        self.date_limite_depot = date_limite_depot
        # Utiliser des listes vides par défaut si None est passé pour les listes
        self.porteurs_eligibles = porteurs_eligibles if porteurs_eligibles is not None else []
        self.secteurs_eligibles = secteurs_eligibles if secteurs_eligibles is not None else []
        self.localisations_concernees = localisations_concernees if localisations_concernees is not None else []
        self.tailles_entreprise_eligibles = tailles_entreprise_eligibles if tailles_entreprise_eligibles is not None else []
        self.trl_min = trl_min
        self.trl_max = trl_max
        self.natures_projet_eligibles = natures_projet_eligibles if natures_projet_eligibles is not None else []
        self.budget_min_projet = budget_min_projet
        self.budget_max_projet = budget_max_projet
        self.nb_etp_min_entreprise = nb_etp_min_entreprise
        self.nb_etp_max_entreprise = nb_etp_max_entreprise
        self.ca_min_entreprise = ca_min_entreprise
        self.ca_max_entreprise = ca_max_entreprise
        self.depenses_eligibles = depenses_eligibles if depenses_eligibles is not None else []
        self.conditions_eligibilite = conditions_eligibilite
        self.mots_cles = mots_cles if mots_cles is not None else []

    def __repr__(self):
        return f"<Aide {self.nom} ({self.id_aide})>"
