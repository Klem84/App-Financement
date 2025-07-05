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
