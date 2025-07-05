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
        self.aides_identifiees = [] # Liste de chaînes ou d'objets Aide plus tard
        self.livrables = [] # Liste d'objets Livrable
        self.date_creation = date_creation if date_creation else datetime.now()
        self.date_mise_a_jour = date_mise_a_jour if date_mise_a_jour else datetime.now()

    def __repr__(self):
        return f"<Projet {self.titre_projet} ({self.id_projet})>"
