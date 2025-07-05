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

# --- Énumérations et Classes pour le Module 3 : Génération de Livrables ---

class StatutCompletionSection(Enum):
    EN_ATTENTE = "En attente"
    EN_COURS = "En cours"
    A_VALIDER = "À valider"
    VALIDE = "Validé"

class PorteeDocument(Enum):
    GLOBALE = "Globale au livrable"
    PARTIE = "Partie spécifique"
    SOUS_PARTIE = "Sous-partie spécifique"
    # SECTION = "Section générique" # Pourrait être utilisé si on a une hiérarchie plus plate

class DocumentSource:
    _id_counter = 0
    def __init__(self, nom_fichier: str, contenu_texte: str, annotations_utilisateur: str = "", portee: PorteeDocument = PorteeDocument.GLOBALE, id_section_portee: str = None):
        DocumentSource._id_counter += 1
        self.id_doc = f"docsrc_{DocumentSource._id_counter}"
        self.nom_fichier = nom_fichier
        self.contenu_texte = contenu_texte # Pourrait être un résumé ou le texte intégral
        self.annotations_utilisateur = annotations_utilisateur
        self.portee = portee
        self.id_section_portee = id_section_portee # ID de la Partie/SousPartie si portee spécifique

    def __repr__(self):
        return f"<DocumentSource {self.nom_fichier} (ID: {self.id_doc}, Portée: {self.portee.value})>"

class VersionSection:
    def __init__(self, contenu: str, instructions: str = "", timestamp: datetime = None):
        self.contenu = contenu
        self.instructions = instructions # Instructions qui ont mené à cette version
        self.timestamp = timestamp if timestamp else datetime.now()

    def __repr__(self):
        return f"<VersionSection à {self.timestamp.strftime('%Y-%m-%d %H:%M')}>"

class SectionLivrable:
    _id_counter = 0
    def __init__(self, titre: str, niveau: int, instructions_utilisateur: str = "", statut_completion: StatutCompletionSection = StatutCompletionSection.EN_ATTENTE, annotations_internes: str = "", priorite: int = 0):
        SectionLivrable._id_counter += 1
        self.id_section = f"sec_{SectionLivrable._id_counter}"
        self.titre = titre
        self.niveau = niveau # 1 pour Partie, 2 pour SousPartie, etc.
        self.contenu_genere = "" # Texte produit par l'IA pour cette section
        self.instructions_utilisateur = instructions_utilisateur # Instructions spécifiques pour cette section
        self.statut_completion = statut_completion
        self.annotations_internes = annotations_internes
        self.priorite = priorite # Ex: 0 = normal, 1 = haute
        self.historique_contenu: list[VersionSection] = [] # Pour stocker les versions du contenu
        self.documents_specifiques: list[DocumentSource] = [] # Documents sources spécifiques à cette section

    def ajouter_version_contenu(self, instructions_generation: str = ""):
        """Ajoute le contenu actuel à l'historique."""
        # L'instruction qui a généré self.contenu_genere actuel
        self.historique_contenu.append(VersionSection(contenu=self.contenu_genere, instructions=instructions_generation))

    def __repr__(self):
        return f"<SectionLivrable '{self.titre}' (ID: {self.id_section}, Statut: {self.statut_completion.value})>"

class SousPartie(SectionLivrable):
    def __init__(self, titre: str, instructions_utilisateur: str = "", statut_completion: StatutCompletionSection = StatutCompletionSection.EN_ATTENTE, annotations_internes: str = "", priorite: int = 0):
        super().__init__(titre, niveau=2, instructions_utilisateur=instructions_utilisateur, statut_completion=statut_completion, annotations_internes=annotations_internes, priorite=priorite)
        # Le contenu est géré par self.contenu_genere de la classe mère

    def __repr__(self):
        return f"<SousPartie '{self.titre}' (ID: {self.id_section}, Statut: {self.statut_completion.value})>"

class Partie(SectionLivrable):
    def __init__(self, titre: str, instructions_utilisateur: str = "", statut_completion: StatutCompletionSection = StatutCompletionSection.EN_ATTENTE, annotations_internes: str = "", priorite: int = 0):
        super().__init__(titre, niveau=1, instructions_utilisateur=instructions_utilisateur, statut_completion=statut_completion, annotations_internes=annotations_internes, priorite=priorite)
        self.sous_parties: list[SousPartie] = []
        # Le contenu de la partie elle-même (texte introductif/conclusif) est dans self.contenu_genere

    def ajouter_sous_partie(self, sous_partie: SousPartie):
        if isinstance(sous_partie, SousPartie):
            self.sous_parties.append(sous_partie)
        else:
            raise TypeError("Seules des instances de SousPartie peuvent être ajoutées.")

    def __repr__(self):
        return f"<Partie '{self.titre}' (ID: {self.id_section}, Sous-parties: {len(self.sous_parties)}, Statut: {self.statut_completion.value})>"


class Livrable:
    _id_counter = 0
    def __init__(self, titre_projet: str, type_livrable_cible: str, projet_associe: Projet = None):
        Livrable._id_counter +=1
        # Ce 'id_livrable' est pour le suivi de cette instance de génération,
        # il peut être différent de l'ID du Livrable final stocké dans Projet.livrables (qui est un objet modeles.Livrable)
        self.id_generation_livrable = f"genliv_{Livrable._id_counter}"
        self.titre_projet = titre_projet
        self.type_livrable_cible = type_livrable_cible # Ex: "CII", "ADEME Appel X"
        self.plan_document: list[Partie] = []
        self.documents_sources_globaux: list[DocumentSource] = []
        self.version_actuelle = 1 # Version majeure du livrable complet
        # historique_versions pourrait stocker des snapshots complets du Livrable ou des diffs. Complexe.
        # Pour l'instant, le versioning est par section via SectionLivrable.historique_contenu
        self.projet_associe = projet_associe # Lien vers l'objet Projet du Module 1

    def ajouter_partie(self, partie: Partie):
        if isinstance(partie, Partie):
            self.plan_document.append(partie)
        else:
            raise TypeError("Seules des instances de Partie peuvent être ajoutées au plan.")

    def ajouter_document_source_global(self, document: DocumentSource):
        if isinstance(document, DocumentSource) and document.portee == PorteeDocument.GLOBALE:
            self.documents_sources_globaux.append(document)
        else:
            # On pourrait aussi changer la portée du document ici si on le souhaite
            raise ValueError("Le document doit être de portée globale ou être ajouté à une section spécifique.")

    def get_section_by_id(self, id_section_recherchee: str) -> SectionLivrable | None:
        for partie in self.plan_document:
            if partie.id_section == id_section_recherchee:
                return partie
            for sous_partie in partie.sous_parties:
                if sous_partie.id_section == id_section_recherchee:
                    return sous_partie
        return None

    def __repr__(self):
        return f"<Livrable en génération '{self.titre_projet}' - {self.type_livrable_cible} (ID Gen: {self.id_generation_livrable})>"
