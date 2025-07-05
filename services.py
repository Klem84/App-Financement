from collections import Counter
from datetime import datetime
from modeles import (
    Utilisateur, Projet, Livrable, StatutPipelineProjet, RoleUtilisateur,
    Aide, LocalisationEntreprise, SecteurActivite, NatureProjet # Ajout de Aide et Enums pour rechercher_aides et associer_aide
)

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

# --- Fonctions pour la Fiche Client (Organisation) ---

def get_organisation_by_id(id_organisation: str, toutes_les_organisations: list["Organisation"]) -> "Organisation | None":
    """Récupère une organisation spécifique par son ID à partir d'une liste d'organisations."""
    from modeles import Organisation # Import local pour éviter dépendance circulaire si Organisation est typée
    for org in toutes_les_organisations:
        if org.id_organisation == id_organisation:
            return org
    return None

def get_utilisateurs_pour_organisation(organisation: "Organisation", sort_by_name: bool = True) -> list[Utilisateur]:
    """Retourne la liste des utilisateurs pour une organisation, triée par nom par défaut."""
    if not organisation:
        return []

    utilisateurs = organisation.utilisateurs
    if sort_by_name:
        return sorted(utilisateurs, key=lambda u: u.nom.lower())
    return utilisateurs

def get_projets_pour_organisation(organisation: "Organisation", sort_by_update: bool = True) -> list[Projet]:
    """Retourne la liste des projets pour une organisation, triée par date de mise à jour desc par défaut."""
    if not organisation:
        return []

    projets = organisation.projets
    if sort_by_update:
        return sorted(projets, key=lambda p: p.date_mise_a_jour if p.date_mise_a_jour else datetime.min, reverse=True)
    return projets

def add_utilisateur_a_organisation(organisation: "Organisation", utilisateur: Utilisateur) -> bool:
    """Ajoute un utilisateur à une organisation et met à jour la référence de l'utilisateur."""
    if not organisation or not utilisateur:
        return False
    if utilisateur in organisation.utilisateurs: # Eviter les doublons
        return True # Ou False si on considère que c'est un échec de "ré-ajouter"

    organisation.utilisateurs.append(utilisateur)
    utilisateur.organisation = organisation # Établir le lien bidirectionnel
    # Potentiellement mettre à jour une date de modification sur l'organisation si nécessaire
    return True

def remove_utilisateur_de_organisation(organisation: "Organisation", id_utilisateur_a_supprimer: str) -> bool:
    """Supprime un utilisateur d'une organisation par son ID."""
    if not organisation:
        return False

    utilisateur_a_retirer = None
    for utilisateur in organisation.utilisateurs:
        if utilisateur.id_utilisateur == id_utilisateur_a_supprimer:
            utilisateur_a_retirer = utilisateur
            break

    if utilisateur_a_retirer:
        organisation.utilisateurs.remove(utilisateur_a_retirer)
        utilisateur_a_retirer.organisation = None # Retirer le lien bidirectionnel
        # Ici, dans une vraie app, on vérifierait les implications (ex: projets où il est référent)
        return True
    return False

def add_projet_a_organisation(organisation: "Organisation", projet: Projet) -> bool:
    """Ajoute un projet à une organisation."""
    from modeles import TypeOrganisation # Import local
    if not organisation or not projet:
        return False
    if projet in organisation.projets: # Eviter les doublons
        return True

    organisation.projets.append(projet)
    if organisation.type_org == TypeOrganisation.CLIENT_FINAL:
        projet.organisation_cliente = organisation # Assigner comme client porteur
    # Si c'est un cabinet, le projet peut être pour un autre client, donc on ne change pas projet.organisation_cliente
    # sauf si explicitement demandé. Le cabinet peut juste "suivre" le projet.
    # La date de mise à jour du projet est gérée à la création/modification du projet lui-même.
    # L'organisation pourrait avoir sa propre date de mise à jour si pertinent.
    return True

def remove_projet_de_organisation(organisation: "Organisation", id_projet_a_supprimer: str) -> bool:
    """Supprime un projet d'une organisation par son ID."""
    if not organisation:
        return False

    projet_a_retirer = None
    for projet_item in organisation.projets:
        if projet_item.id_projet == id_projet_a_supprimer:
            projet_a_retirer = projet_item
            break

    if projet_a_retirer:
        organisation.projets.remove(projet_a_retirer)
        # Ici, dans une vraie app, on vérifierait les implications (projet.organisation_cliente, etc.)
        # Pour la simulation, on retire juste de la liste.
        return True
    return False

def update_organisation_info(organisation: "Organisation", nom: str = None, type_org: "TypeOrganisation" = None) -> "Organisation | None":
    """Met à jour le nom et/ou le type d'une organisation."""
    from modeles import TypeOrganisation # Import local
    if not organisation:
        return None

    updated = False
    if nom and organisation.nom != nom:
        organisation.nom = nom
        updated = True
    if type_org and organisation.type_org != type_org:
        organisation.type_org = type_org
        updated = True

    # Si on avait une date de mise à jour pour l'organisation, on la mettrait à jour ici si updated == True
    # par exemple: if updated: organisation.date_mise_a_jour = datetime.now()

    return organisation

# --- Fonctions pour le Module 2 : Recherche de Financements ---

def rechercher_aides(criteres: dict, toutes_les_aides: list[Aide]) -> list[Aide]:
    """
    Filtre une liste d'aides en fonction de multiples critères.
    Les critères peuvent inclure des correspondances exactes, des appartenances à des listes,
    des plages numériques, et une recherche par mot-clé.
    """
    resultats = toutes_les_aides

    # Filtre par mot-clé (recherche simple dans nom, description, organisme, conditions, dépenses)
    mot_cle = criteres.get("mot_cle")
    if mot_cle:
        mot_cle_lower = mot_cle.lower()
        resultats = [
            aide for aide in resultats if
            mot_cle_lower in aide.nom.lower() or
            mot_cle_lower in aide.description_courte.lower() or
            mot_cle_lower in aide.organisme_financeur.lower() or
            (aide.conditions_eligibilite and mot_cle_lower in aide.conditions_eligibilite.lower()) or
            any(mot_cle_lower in dep.lower() for dep in aide.depenses_eligibles) or
            any(mot_cle_lower in mc.lower() for mc in aide.mots_cles)
        ]

    # Filtre par TypeAide (correspondance exacte)
    type_aide_filtre = criteres.get("type_aide")
    if type_aide_filtre: # type_aide_filtre est un membre de l'Enum TypeAide
        resultats = [aide for aide in resultats if aide.type_aide == type_aide_filtre]

    # Filtre par TypeStructureEntreprise (le critère doit être dans la liste porteurs_eligibles de l'aide)
    type_structure_filtre = criteres.get("type_structure")
    if type_structure_filtre: # type_structure_filtre est un membre de l'Enum TypeStructureEntreprise
        resultats = [aide for aide in resultats if not aide.porteurs_eligibles or type_structure_filtre in aide.porteurs_eligibles]

    # Filtre par LocalisationEntreprise (le critère doit être dans la liste localisations_concernees de l'aide)
    # Ou si l'aide est nationale (LocalisationEntreprise.FRANCE)
    localisation_filtre = criteres.get("localisation")
    if localisation_filtre: # localisation_filtre est un membre de l'Enum LocalisationEntreprise
        resultats = [
            aide for aide in resultats if not aide.localisations_concernees or
            LocalisationEntreprise.FRANCE in aide.localisations_concernees or
            localisation_filtre in aide.localisations_concernees
        ]

    # Filtre par SecteurActivite (le critère doit être dans la liste secteurs_eligibles de l'aide)
    # Ou si l'aide est pour tous secteurs (SecteurActivite.TOUS)
    secteur_activite_filtre = criteres.get("secteur_activite")
    if secteur_activite_filtre: # secteur_activite_filtre est un membre de l'Enum SecteurActivite
        resultats = [
            aide for aide in resultats if not aide.secteurs_eligibles or
            SecteurActivite.TOUS in aide.secteurs_eligibles or
            secteur_activite_filtre in aide.secteurs_eligibles
        ]

    # Filtre par TailleEntreprise (le critère doit être dans la liste tailles_entreprise_eligibles de l'aide)
    taille_entreprise_filtre = criteres.get("taille_entreprise")
    if taille_entreprise_filtre: # taille_entreprise_filtre est un membre de l'Enum TailleEntreprise
        resultats = [aide for aide in resultats if not aide.tailles_entreprise_eligibles or taille_entreprise_filtre in aide.tailles_entreprise_eligibles]


    # Filtre par NatureProjet (le critère doit être dans la liste natures_projet_eligibles de l'aide)
    nature_projet_filtre = criteres.get("nature_projet")
    if nature_projet_filtre: # nature_projet_filtre est un membre de l'Enum NatureProjet
        resultats = [
            aide for aide in resultats if not aide.natures_projet_eligibles or
            NatureProjet.AUTRE in aide.natures_projet_eligibles or # Si l'aide accepte "Autre"
            nature_projet_filtre in aide.natures_projet_eligibles
        ]

    # Filtres de plage numérique
    # Pour ces filtres, la logique est : l'intervalle de l'aide doit ENGLOBER la valeur fournie par l'entreprise,
    # ou si l'entreprise fournit un intervalle, les deux intervalles doivent se chevaucher.
    # Pour simplifier ici, on va considérer que l'entreprise fournit une valeur unique pour ETP et CA,
    # et un budget de projet unique.

    # Filtre par Nombre d'ETP de l'entreprise (la valeur de l'entreprise doit être dans la plage de l'aide)
    etp_entreprise = criteres.get("nb_etp_entreprise")
    if etp_entreprise is not None:
        resultats = [
            aide for aide in resultats if
            (aide.nb_etp_min_entreprise is None or etp_entreprise >= aide.nb_etp_min_entreprise) and
            (aide.nb_etp_max_entreprise is None or etp_entreprise <= aide.nb_etp_max_entreprise)
        ]

    # Filtre par Chiffre d'Affaires (CA) de l'entreprise
    ca_entreprise = criteres.get("ca_entreprise")
    if ca_entreprise is not None:
        resultats = [
            aide for aide in resultats if
            (aide.ca_min_entreprise is None or ca_entreprise >= aide.ca_min_entreprise) and
            (aide.ca_max_entreprise is None or ca_entreprise <= aide.ca_max_entreprise)
        ]

    # Filtre par Budget du projet
    budget_projet = criteres.get("budget_projet")
    if budget_projet is not None:
        resultats = [
            aide for aide in resultats if
            (aide.budget_min_projet is None or budget_projet >= aide.budget_min_projet) and
            (aide.budget_max_projet is None or budget_projet <= aide.budget_max_projet)
        ]

    # Filtre par TRL (Total Readiness Level) du projet
    # Le TRL du projet doit être dans la plage [trl_min, trl_max] de l'aide
    # Ce filtre ne s'applique que si l'aide a des critères TRL ET si le projet a un TRL (implicite ici)
    trl_projet = criteres.get("trl_projet") # Un entier unique pour le TRL du projet
    if trl_projet is not None:
        resultats = [
            aide for aide in resultats if
            (aide.trl_min is None or trl_projet >= aide.trl_min) and
            (aide.trl_max is None or trl_projet <= aide.trl_max)
        ]

    return resultats

def associer_aide_a_projet(projet: Projet, aide: Aide) -> bool:
    """
    Associe une aide à un projet.
    Vérifie si l'aide n'est pas déjà associée pour éviter les doublons.
    Met à jour la date de mise à jour du projet.
    """
    if not projet or not aide:
        print("Erreur: Projet ou Aide non défini pour l'association.")
        return False

    # Vérifier les doublons basés sur l'id_aide
    if any(a.id_aide == aide.id_aide for a in projet.aides_identifiees):
        print(f"Info: L'aide '{aide.nom}' (ID: {aide.id_aide}) est déjà associée au projet '{projet.titre_projet}'.")
        return False # Ou True si on considère que l'état est déjà correct

    projet.aides_identifiees.append(aide)
    projet.date_mise_a_jour = datetime.now()
    print(f"Succès: Aide '{aide.nom}' associée au projet '{projet.titre_projet}'.")
    return True
