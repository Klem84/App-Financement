from collections import Counter
from datetime import datetime
from modeles import Utilisateur, Projet, Livrable, StatutPipelineProjet, RoleUtilisateur

def get_projets_par_statut(consultant: Utilisateur) -> dict:
    """
    Compte le nombre de projets par statut pour un consultant donné.
    """
    if not consultant or consultant.role != RoleUtilisateur.CONSULTANT:
        # Ou gérer autrement si l'utilisateur n'est pas un consultant
        return {}

    statuts_counts = Counter(projet.statut_pipeline for projet in consultant.projets_associes)

    # Assurer que tous les statuts sont présents dans le résultat, même avec un compte de 0
    resultat = {statut: 0 for statut in StatutPipelineProjet}
    resultat.update(statuts_counts)

    return resultat

def get_projets_recents(consultant: Utilisateur, n: int = 5) -> list[Projet]:
    """
    Retourne les n projets les plus récemment mis à jour pour un consultant.
    """
    if not consultant or consultant.role != RoleUtilisateur.CONSULTANT:
        return []

    # Trier les projets par date_mise_a_jour, du plus récent au plus ancien
    # Gérer les cas où date_mise_a_jour pourrait être None, bien que notre modèle l'initialise
    projets_tries = sorted(
        consultant.projets_associes,
        key=lambda p: p.date_mise_a_jour if p.date_mise_a_jour else datetime.min,
        reverse=True
    )
    return projets_tries[:n]

def get_livrables_recents(consultant: Utilisateur, n: int = 3) -> list[Livrable]:
    """
    Retourne les n livrables les plus récemment générés pour les projets d'un consultant.
    """
    if not consultant or consultant.role != RoleUtilisateur.CONSULTANT:
        return []

    tous_les_livrables_consultant = []
    for projet in consultant.projets_associes:
        tous_les_livrables_consultant.extend(projet.livrables)

    # Trier les livrables par date_generation, du plus récent au plus ancien
    # Gérer les cas où date_generation pourrait être None
    livrables_tries = sorted(
        tous_les_livrables_consultant,
        key=lambda l: l.date_generation if l.date_generation else datetime.min,
        reverse=True
    )
    return livrables_tries[:n]

# --- Fonctions pour la Fiche Projet ---

def update_statut_projet(projet: Projet, nouveau_statut: StatutPipelineProjet) -> Projet:
    """Met à jour le statut d'un projet et sa date de mise à jour."""
    if not projet:
        # Gérer le cas où le projet est None, bien que typiquement on s'attend à un objet Projet valide
        raise ValueError("Le projet ne peut pas être None pour la mise à jour du statut.")

    projet.statut_pipeline = nouveau_statut
    projet.date_mise_a_jour = datetime.now()
    return projet

def add_aide_to_projet(projet: Projet, nom_aide: str, lien_aide: str = None, remarque: str = None) -> Projet:
    """Ajoute une aide (sous forme de dictionnaire) à la liste aides_identifiees du projet."""
    if not projet:
        raise ValueError("Le projet ne peut pas être None pour l'ajout d'une aide.")

    aide = {
        "nom": nom_aide,
        "lien": lien_aide if lien_aide else "N/A",
        "remarque": remarque if remarque else "N/A"
    }
    projet.aides_identifiees.append(aide)
    projet.date_mise_a_jour = datetime.now()
    return projet

# Compteur simple pour les ID de livrables en simulation
_livrable_id_counter = 0

def _generer_id_livrable(prefix: str = "liv") -> str:
    """Génère un ID de livrable unique pour la simulation."""
    global _livrable_id_counter
    _livrable_id_counter += 1
    return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{_livrable_id_counter}"

def create_livrable_pour_projet(
    projet: Projet,
    type_livrable: "TypeLivrable",  # Forward declaration if TypeLivrable is in modeles.py
    fichier_associe: str,
    cree_par: Utilisateur,
    id_livrable_prefix: str = "liv",
    statut_validation: "StatutValidationLivrable" = None # Forward declaration
) -> Livrable:
    """Crée un nouveau livrable, l'ajoute au projet et retourne le livrable créé."""
    from modeles import TypeLivrable, StatutValidationLivrable # Local import for Enums if not already available

    if not projet:
        raise ValueError("Le projet ne peut pas être None pour la création d'un livrable.")
    if not cree_par:
        raise ValueError("L'utilisateur créateur ne peut pas être None pour la création d'un livrable.")

    # Utilisation de l'import local pour StatutValidationLivrable.BROUILLON
    statut_initial = statut_validation if statut_validation else StatutValidationLivrable.BROUILLON

    id_nouveau_livrable = _generer_id_livrable(id_livrable_prefix)

    nouveau_livrable = Livrable(
        id_livrable=id_nouveau_livrable,
        type_livrable=type_livrable,
        fichier_associe=fichier_associe,
        projet_parent=projet,
        cree_par=cree_par,
        statut_validation=statut_initial,
        date_generation=datetime.now() # La date de génération est au moment de la création
    )
    projet.livrables.append(nouveau_livrable)
    projet.date_mise_a_jour = datetime.now()
    return nouveau_livrable

def update_statut_livrable(livrable: Livrable, nouveau_statut: "StatutValidationLivrable", projet_parent: Projet) -> Livrable:
    """Met à jour le statut de validation d'un livrable et la date de MàJ du projet parent."""
    if not livrable:
        raise ValueError("Le livrable ne peut pas être None pour la mise à jour du statut.")
    if not projet_parent:
        raise ValueError("Le projet parent ne peut pas être None pour la mise à jour du statut du livrable.")

    livrable.statut_validation = nouveau_statut
    # On pourrait choisir de mettre à jour livrable.date_generation ou ajouter un champ date_derniere_modif_statut
    # Pour l'instant, on considère que la date_generation est la date de la dernière action significative sur le livrable.
    livrable.date_generation = datetime.now()
    projet_parent.date_mise_a_jour = datetime.now()
    return livrable

def get_projet_by_id(id_projet: str, tous_les_projets: list[Projet]) -> Projet | None:
    """Récupère un projet spécifique par son ID à partir d'une liste de projets."""
    for projet in tous_les_projets:
        if projet.id_projet == id_projet:
            return projet
    return None

def get_livrables_par_projet(projet: Projet, sort_by_date: bool = True) -> list[Livrable]:
    """Retourne la liste des livrables pour un projet, triée par date de génération par défaut."""
    if not projet:
        return []

    livrables = projet.livrables
    if sort_by_date:
        return sorted(livrables, key=lambda l: l.date_generation if l.date_generation else datetime.min, reverse=True)
    return livrables
