from modeles import (
    Utilisateur, Organisation, Projet, Livrable,
    RoleUtilisateur, TypeOrganisation, StatutPipelineProjet, TypeLivrable, StatutValidationLivrable,
    Aide, TypeAide, NatureProjet, TypeStructureEntreprise, SecteurActivite, TailleEntreprise, LocalisationEntreprise # Pour Module 2
)
from services import (
    get_projets_par_statut, get_projets_recents, get_livrables_recents,
    update_statut_projet, add_aide_to_projet, create_livrable_pour_projet,
    update_statut_livrable, get_projet_by_id, get_livrables_par_projet,
    get_organisation_by_id, get_utilisateurs_pour_organisation, get_projets_pour_organisation,
    add_utilisateur_a_organisation, remove_utilisateur_de_organisation,
    add_projet_a_organisation, remove_projet_de_organisation, update_organisation_info,
    rechercher_aides, associer_aide_a_projet # Pour Module 2
)
from donnees_simulees import aides_simulees # Pour Module 2
from datetime import datetime
import time # Pour simuler des délais et rendre la génération d'ID unique plus robuste

def print_dashboard(consultant: Utilisateur, projets_par_statut: dict, projets_recents: list[Projet], livrables_recents: list[Livrable]):
    """Affiche les informations du dashboard pour un consultant."""
    print("\n" + "="*50)
    print(f"DASHBOARD CONSULTANT : {consultant.nom}")
    print("="*50)

    # 1. Informations générales du consultant
    print("\n🟦 1. Informations Générales")
    print(f"   Nom complet: {consultant.nom}")
    print(f"   Rôle: {consultant.role.value}")
    print(f"   Nombre total de projets assignés: {len(consultant.projets_associes)}")

    # 2. Vue d’ensemble des projets
    print("\n🟨 2. Vue d’ensemble des projets")
    if projets_par_statut:
        for statut, count in projets_par_statut.items():
            if count > 0 : # Affiche seulement les statuts avec des projets
                 print(f"   - {statut.value}: {count} projet(s)")
    else:
        print("   Aucun projet à afficher.")

    total_projets_statut = sum(projets_par_statut.values())
    print(f"   Compteur global: {total_projets_statut} projet(s) via statuts")


    # 3. Liste des projets récents ou actifs
    print("\n🟩 3. Liste des projets récents ou actifs")
    if projets_recents:
        for i, projet in enumerate(projets_recents):
            print(f"   --- Projet {i+1} ---")
            print(f"     Titre: {projet.titre_projet}")
            print(f"     Organisation cliente: {projet.organisation_cliente.nom if projet.organisation_cliente else 'N/A'}")
            print(f"     Statut pipeline: {projet.statut_pipeline.value}")
            print(f"     Dernière mise à jour: {projet.date_mise_a_jour.strftime('%Y-%m-%d %H:%M') if projet.date_mise_a_jour else 'N/A'}")
            print(f"     Nombre total de livrables: {len(projet.livrables)}")
            if projet.livrables:
                dernier_livrable_projet = sorted(projet.livrables, key=lambda l: l.date_generation, reverse=True)[0]
                print(f"     Statut du dernier livrable: {dernier_livrable_projet.type_livrable.value} - {dernier_livrable_projet.statut_validation.value}")
            else:
                print("     Aucun livrable pour ce projet.")
    else:
        print("   Aucun projet récent à afficher.")

    # 4. Activité récente sur les livrables
    print("\n🟥 4. Activité récente sur les livrables")
    if livrables_recents:
        for i, livrable in enumerate(livrables_recents):
            print(f"   --- Livrable {i+1} ---")
            print(f"     Type: {livrable.type_livrable.value}")
            print(f"     Projet parent: {livrable.projet_parent.titre_projet if livrable.projet_parent else 'N/A'}")
            print(f"     Date de génération: {livrable.date_generation.strftime('%Y-%m-%d %H:%M') if livrable.date_generation else 'N/A'}")
            print(f"     Statut de validation: {livrable.statut_validation.value}")
    else:
        print("   Aucune activité récente sur les livrables.")
    print("="*50 + "\n")

def print_fiche_projet(projet: Projet, utilisateur_actuel: Utilisateur):
    """Affiche les informations de la fiche projet et les actions possibles."""
    if not projet:
        print("Erreur: Impossible d'afficher la fiche d'un projet non défini.")
        return

    print("\n" + "="*60)
    print(f"FICHE PROJET: {projet.titre_projet.upper()}")
    print("="*60)

    # 🟦 INFORMATIONS GÉNÉRALES
    print("\n🟦 INFORMATIONS GÉNÉRALES")
    print("-"*50)
    print(f"Titre: {projet.titre_projet}")
    print(f"Organisation Cliente: {projet.organisation_cliente.nom if projet.organisation_cliente else 'N/A'} (ID: {projet.organisation_cliente.id_organisation if projet.organisation_cliente else 'N/A'})")
    print(f"Consultant Référent: {projet.consultant_referent.nom if projet.consultant_referent else 'N/A'} (ID: {projet.consultant_referent.id_utilisateur if projet.consultant_referent else 'N/A'})")
    print(f"Date de Création: {projet.date_creation.strftime('%Y-%m-%d %H:%M') if projet.date_creation else 'N/A'}")
    print(f"Dernière Mise à Jour: {projet.date_mise_a_jour.strftime('%Y-%m-%d %H:%M') if projet.date_mise_a_jour else 'N/A'}")
    print(f"Statut Pipeline: {projet.statut_pipeline.value}")

    # Actions possibles (simulées par des numéros pour l'interaction en console)
    print("  Actions possibles (Informations Générales):")
    print(f"    1. Modifier Statut Pipeline (actuel: {projet.statut_pipeline.value})")
    # Lister les statuts possibles pour la modification
    for i, statut_enum_membre in enumerate(StatutPipelineProjet):
        if statut_enum_membre != projet.statut_pipeline:
             print(f"       1.{i+1} Passer à '{statut_enum_membre.value}'")


    # 🟨 SUIVI DES AIDES SÉLECTIONNÉES
    print("\n🟨 SUIVI DES AIDES SÉLECTIONNÉES")
    print("-"*50)
    if projet.aides_identifiees: # Maintenant une liste d'objets Aide
        print("Aides Actuelles:")
        for i, aide_associee in enumerate(projet.aides_identifiees):
            if isinstance(aide_associee, Aide): # Vérifier si c'est bien un objet Aide
                print(f"  - Aide {i+1}: {aide_associee.nom} (ID: {aide_associee.id_aide})")
                print(f"      Organisme: {aide_associee.organisme_financeur}, Type: {aide_associee.type_aide.value}")
                if aide_associee.date_limite_depot:
                    print(f"      Date Limite: {aide_associee.date_limite_depot.strftime('%d/%m/%Y')}")
            elif isinstance(aide_associee, dict) : # Ancien format, si la transition n'est pas complète
                print(f"  - Aide {i+1} (format dict): {aide_associee.get('nom', 'N/A')} (Lien: {aide_associee.get('lien', 'N/A')}, Remarque: {aide_associee.get('remarque', 'N/A')})")
            else:
                print(f"  - Aide {i+1}: format inconnu.")

    else:
        print("  Aucune aide sélectionnée pour ce projet.")
    print("  Actions possibles (Aides):")
    # L'action "Ajouter une Aide" manuellement via la fiche projet devrait maintenant aussi utiliser associer_aide_a_projet
    # ou une fonction qui crée un objet Aide. Pour l'instant, on se concentre sur l'association depuis la recherche.
    print("    2. Ajouter une Aide (via recherche et association)")

    # 🟩 SUIVI DES LIVRABLES
    print("\n🟩 SUIVI DES LIVRABLES")
    print("-"*50)
    livrables_du_projet = get_livrables_par_projet(projet) # Triés par date de génération desc par défaut
    if livrables_du_projet:
        print("Livrables du Projet:")
        # En-tête du tableau
        header = "| {:<20} | {:<12} | {:<19} | {:<25} | {:<15} |".format(
            "Type", "Statut", "Date Génération", "Fichier Associé", "Créé par"
        )
        print(header)
        print("-" * len(header))
        for i, livrable in enumerate(livrables_du_projet):
            row = "| {:<20} | {:<12} | {:<19} | {:<25} | {:<15} |".format(
                livrable.type_livrable.value,
                livrable.statut_validation.value,
                livrable.date_generation.strftime('%Y-%m-%d %H:%M') if livrable.date_generation else 'N/A',
                livrable.fichier_associe,
                livrable.cree_par.nom if livrable.cree_par else 'N/A'
            )
            print(row)
            # Actions pour chaque livrable
            print(f"  Livrable ID {livrable.id_livrable} - Actions:")
            for j, statut_val_enum_membre in enumerate(StatutValidationLivrable):
                 if statut_val_enum_membre != livrable.statut_validation:
                    print(f"    3.{i+1}.{j+1} Modifier statut vers '{statut_val_enum_membre.value}'")

    else:
        print("  Aucun livrable pour ce projet.")
    print("  Actions possibles (Livrables):")
    print("    4. Ajouter un Livrable (manuel)")
    # print("    5. Générer un Livrable (IA - non implémenté)") # Pour plus tard

    # 🔐 ACCÈS UTILISATEUR (Note)
    print("\n🔐 ACCÈS UTILISATEUR (Simulation)")
    print("-"*50)
    if utilisateur_actuel.role == RoleUtilisateur.CONSULTANT:
        print("  Accès Consultant: Total (simulation)")
    elif utilisateur_actuel.role == RoleUtilisateur.CLIENT and projet in utilisateur_actuel.projets_associes:
        print("  Accès Client: Limité/Lecture seule (simulation)")
    else:
        print("  Accès non défini pour cet utilisateur sur ce projet.")

    print("="*60 + "\n")

def print_fiche_client(organisation: Organisation, utilisateur_actuel: Utilisateur):
    """Affiche les informations de la fiche client (organisation) et les actions possibles."""
    if not organisation:
        print("Erreur: Impossible d'afficher la fiche d'une organisation non définie.")
        return

    print("\n" + "="*70)
    print(f"FICHE CLIENT (ORGANISATION): {organisation.nom.upper()}")
    print("="*70)

    # 🟦 INFORMATIONS GÉNÉRALES DE L'ORGANISATION
    print("\n🟦 INFORMATIONS GÉNÉRALES DE L'ORGANISATION")
    print("-"*60)
    print(f"Nom: {organisation.nom}")
    print(f"ID Organisation: {organisation.id_organisation}")
    print(f"Type: {organisation.type_org.value}")

    projets_org = get_projets_pour_organisation(organisation, sort_by_update=False) # Pas besoin de trier juste pour compter
    utilisateurs_org = get_utilisateurs_pour_organisation(organisation, sort_by_name=False) # Idem

    print(f"Nombre Total de Projets Liés: {len(projets_org)}")
    print(f"Nombre Total d'Utilisateurs Rattachés: {len(utilisateurs_org)}")
    print("  Actions possibles (Organisation):")
    print(f"    1. Modifier les informations de l'Organisation (Nom actuel: '{organisation.nom}', Type actuel: '{organisation.type_org.value}')")

    # 🟨 UTILISATEURS ASSOCIÉS À L'ORGANISATION
    print("\n🟨 UTILISATEURS ASSOCIÉS À L'ORGANISATION")
    print("-"*60)
    utilisateurs_tries = get_utilisateurs_pour_organisation(organisation) # Triés par nom
    if utilisateurs_tries:
        header_users = "| {:<20} | {:<25} | {:<10} | {:<12} | {:<20} |".format(
            "Nom", "Email", "Rôle", "ID Utilisateur", "Dernière Connexion"
        )
        print(header_users)
        print("-" * len(header_users))
        for user in utilisateurs_tries:
            derniere_co = user.derniere_connexion.strftime('%Y-%m-%d %H:%M') if user.derniere_connexion else "Jamais connecté"
            row_user = "| {:<20} | {:<25} | {:<10} | {:<12} | {:<20} |".format(
                user.nom, user.email, user.role.value, user.id_utilisateur, derniere_co
            )
            print(row_user)
    else:
        print("  Aucun utilisateur rattaché à cette organisation.")
    print("  Actions possibles (Utilisateurs):")
    print("    2. Ajouter un Utilisateur à l'Organisation")
    if utilisateurs_tries : # On ne peut supprimer que s'il y en a
        print(f"    3. Supprimer un Utilisateur de l'Organisation (ex: ID '{utilisateurs_tries[0].id_utilisateur}' si liste non vide)")


    # 🟩 LISTE DES PROJETS DE L'ORGANISATION
    print("\n🟩 LISTE DES PROJETS DE L'ORGANISATION")
    print("-"*60)
    projets_tries = get_projets_pour_organisation(organisation) # Triés par date de MàJ desc
    if projets_tries:
        print("  (Triés par date de mise à jour, décroissante)")
        for i, projet in enumerate(projets_tries):
            print(f"  --- Projet {i+1} ---")
            print(f"    Titre: {projet.titre_projet} (ID: {projet.id_projet})")
            print(f"    Consultant Référent: {projet.consultant_referent.nom if projet.consultant_referent else 'N/A'}")
            print(f"    Statut Pipeline: {projet.statut_pipeline.value}")
            print(f"    Dernière Mise à Jour: {projet.date_mise_a_jour.strftime('%Y-%m-%d %H:%M') if projet.date_mise_a_jour else 'N/A'}")
            print(f"    Nombre de Livrables: {len(projet.livrables)}")
            print(f"    (Lien simulé vers Fiche Projet -> Afficher Fiche Projet ID {projet.id_projet})")
    else:
        print("  Aucun projet lié à cette organisation.")
    print("  Actions possibles (Projets):")
    print("    4. Ajouter un Projet à l'Organisation")
    if projets_tries: # On ne peut supprimer que s'il y en a
        print(f"    5. Supprimer un Projet de l'Organisation (ex: ID '{projets_tries[0].id_projet}' si liste non vide)")

    # Note sur l'accès utilisateur (similaire à Fiche Projet)
    print("\n🔐 ACCÈS UTILISATEUR (Simulation)")
    print("-"*60)
    # Logique d'accès simplifiée pour la démo
    if utilisateur_actuel.role == RoleUtilisateur.ADMIN or \
       (utilisateur_actuel.role == RoleUtilisateur.CONSULTANT and utilisateur_actuel.organisation == organisation): # Un consultant du cabinet voit la fiche du cabinet
        print("  Accès Admin/Consultant du cabinet: Total (simulation)")
    elif utilisateur_actuel.organisation == organisation and utilisateur_actuel.role == RoleUtilisateur.CLIENT : # Un client voit sa propre organisation
         print("  Accès Client de l'organisation: Vue limitée (simulation)")
    else:
        # Cas où un consultant externe voudrait voir la fiche d'un client auquel il n'est pas explicitement lié par un projet
        # Ou un client essayant de voir une autre organisation.
        # Pour l'instant, on se base sur l'appartenance directe à l'organisation.
        print("  Accès restreint ou non défini pour cet utilisateur sur cette organisation (simulation).")


    print("="*70 + "\n")


def main():
    # 1. Créer des Organisations
    cabinet_conseil = Organisation(id_organisation="org_cabinet_001", nom="Cabinet InnovConseil", type_org=TypeOrganisation.CABINET)
    client_alpha = Organisation(id_organisation="org_client_A", nom="Entreprise Alpha", type_org=TypeOrganisation.CLIENT_FINAL)
    client_beta = Organisation(id_organisation="org_client_B", nom="Société BetaTech", type_org=TypeOrganisation.CLIENT_FINAL)

    print("Organisations créées:")
    print(cabinet_conseil)
    print(client_alpha)
    print(client_beta)
    print("-" * 30)

    # 2. Créer des Utilisateurs et les lier aux organisations
    consultant_alice = Utilisateur(id_utilisateur="user_alice", nom="Alice Expert", email="alice@innovconseil.com", role=RoleUtilisateur.CONSULTANT, organisation=cabinet_conseil)
    admin_bob = Utilisateur(id_utilisateur="user_bob", nom="Bob Admin", email="bob@innovconseil.com", role=RoleUtilisateur.ADMIN, organisation=cabinet_conseil)
    client_charlie = Utilisateur(id_utilisateur="user_charlie", nom="Charlie ClientA", email="charlie@alpha.com", role=RoleUtilisateur.CLIENT, organisation=client_alpha)
    client_david = Utilisateur(id_utilisateur="user_david", nom="David ClientB", email="david@betatech.com", role=RoleUtilisateur.CLIENT, organisation=client_beta)

    # Lier utilisateurs à leur organisation (liste utilisateurs de l'organisation)
    cabinet_conseil.utilisateurs.extend([consultant_alice, admin_bob])
    client_alpha.utilisateurs.append(client_charlie)
    client_beta.utilisateurs.append(client_david)

    print("\nUtilisateurs créés et liés aux organisations:")
    print(consultant_alice, f"dans {consultant_alice.organisation.nom}")
    print(admin_bob, f"dans {admin_bob.organisation.nom}")
    print(client_charlie, f"dans {client_charlie.organisation.nom}")
    print(client_david, f"dans {client_david.organisation.nom}")
    print(f"Utilisateurs chez {cabinet_conseil.nom}: {len(cabinet_conseil.utilisateurs)}")
    print(f"Utilisateurs chez {client_alpha.nom}: {len(client_alpha.utilisateurs)}")
    print("-" * 30)

    # 3. Créer des Projets et les lier
    projet_cir_alpha = Projet(
        id_projet="proj_alpha_001",
        titre_projet="Dossier CIR 2024 - Alpha",
        organisation_cliente=client_alpha,
        consultant_referent=consultant_alice,
        statut_pipeline=StatutPipelineProjet.REDACTION
    )
    projet_ademe_beta = Projet(
        id_projet="proj_beta_002",
        titre_projet="Subvention ADEME GreenTech - Beta",
        organisation_cliente=client_beta,
        consultant_referent=consultant_alice,
        statut_pipeline=StatutPipelineProjet.ELIGIBILITE
    )

    # Lier projets à leur organisation cliente et au cabinet (si pertinent)
    client_alpha.projets.append(projet_cir_alpha)
    client_beta.projets.append(projet_ademe_beta)
    cabinet_conseil.projets.extend([projet_cir_alpha, projet_ademe_beta]) # Le cabinet gère ces projets

    # Associer utilisateurs aux projets
    consultant_alice.projets_associes.extend([projet_cir_alpha, projet_ademe_beta])
    client_charlie.projets_associes.append(projet_cir_alpha) # Charlie a accès au projet de son entreprise
    # David pourrait être ajouté à projet_ademe_beta si nécessaire

    print("\nProjets créés et liés:")
    print(projet_cir_alpha, f"Client: {projet_cir_alpha.organisation_cliente.nom}, Consultant: {projet_cir_alpha.consultant_referent.nom}")
    print(projet_ademe_beta, f"Client: {projet_ademe_beta.organisation_cliente.nom}, Consultant: {projet_ademe_beta.consultant_referent.nom}")
    print(f"Projets pour {client_alpha.nom}: {[p.titre_projet for p in client_alpha.projets]}")
    print(f"Projets gérés par {consultant_alice.nom}: {[p.titre_projet for p in consultant_alice.projets_associes]}")
    print("-" * 30)

    # 4. Créer des Livrables et les lier aux projets
    livrable_prediag_alpha = Livrable(
        id_livrable="liv_alpha_001_prediag",
        type_livrable=TypeLivrable.PRE_DIAGNOSTIC,
        fichier_associe="/chemin/vers/prediag_alpha.pdf",
        projet_parent=projet_cir_alpha,
        cree_par=consultant_alice,
        statut_validation=StatutValidationLivrable.VALIDE
    )
    livrable_cir_alpha_brouillon = Livrable(
        id_livrable="liv_alpha_002_cir",
        type_livrable=TypeLivrable.CIR,
        fichier_associe="/chemin/vers/cir_alpha_brouillon.docx",
        projet_parent=projet_cir_alpha,
        cree_par=consultant_alice,
        statut_validation=StatutValidationLivrable.BROUILLON
    )

    # Lier livrables aux projets
    projet_cir_alpha.livrables.extend([livrable_prediag_alpha, livrable_cir_alpha_brouillon])

    print("\nLivrables créés et liés:")
    print(livrable_prediag_alpha, f"pour Projet: {livrable_prediag_alpha.projet_parent.titre_projet}, créé par: {livrable_prediag_alpha.cree_par.nom}")
    print(livrable_cir_alpha_brouillon, f"pour Projet: {livrable_cir_alpha_brouillon.projet_parent.titre_projet}, statut: {livrable_cir_alpha_brouillon.statut_validation.value}")
    print(f"Livrables pour {projet_cir_alpha.titre_projet}: {len(projet_cir_alpha.livrables)}")
    print("-" * 30)

    # Vérifications des liens bidirectionnels (simulés)
    print("\nVérifications des liens:")
    # Consultant Alice et ses projets
    print(f"Projets de {consultant_alice.nom}:")
    for proj in consultant_alice.projets_associes:
        print(f"  - {proj.titre_projet} (Consultant référent: {proj.consultant_referent.nom})")

    # Projet CIR Alpha et son consultant
    print(f"Consultant pour {projet_cir_alpha.titre_projet}: {projet_cir_alpha.consultant_referent.nom}")
    # Organisation Alpha et ses projets
    print(f"Projets de l'organisation {client_alpha.nom}:")
    for proj in client_alpha.projets:
        print(f"  - {proj.titre_projet} (Organisation cliente: {proj.organisation_cliente.nom})")

    # Livrables du projet CIR Alpha
    print(f"Livrables pour {projet_cir_alpha.titre_projet}:")
    for liv in projet_cir_alpha.livrables:
        print(f"  - {liv.type_livrable.value} créé par {liv.cree_par.nom}")

    # --- Simulation du Dashboard pour Alice ---
    # S'assurer que consultant_alice est bien un consultant
    if consultant_alice.role == RoleUtilisateur.CONSULTANT:
        # Récupérer les données pour le dashboard d'Alice
        projets_statut_alice = get_projets_par_statut(consultant_alice)
        projets_recents_alice = get_projets_recents(consultant_alice, n=5) # Afficher les 5 projets les plus récents
        livrables_recents_alice = get_livrables_recents(consultant_alice, n=3) # Afficher les 3 livrables les plus récents

        # Afficher le dashboard simulé
        print_dashboard(consultant_alice, projets_statut_alice, projets_recents_alice, livrables_recents_alice)
    else:
        print(f"\nL'utilisateur {consultant_alice.nom} n'est pas un consultant, dashboard non applicable.")

    # --- Simulation du Dashboard pour un utilisateur sans projets (si besoin pour tester) ---
    # consultant_test_sans_projet = Utilisateur(id_utilisateur="user_test_empty", nom="Test Consultant Vide", email="empty@test.com", role=RoleUtilisateur.CONSULTANT, organisation=cabinet_conseil)
    # cabinet_conseil.utilisateurs.append(consultant_test_sans_projet) # Ne pas oublier de l'ajouter à l'organisation
    # projets_statut_test = get_projets_par_statut(consultant_test_sans_projet)
    # projets_recents_test = get_projets_recents(consultant_test_sans_projet)
    # livrables_recents_test = get_livrables_recents(consultant_test_sans_projet)
    # print_dashboard(consultant_test_sans_projet, projets_statut_test, projets_recents_test, livrables_recents_test)

    print("\n" + "#"*70)
    print("### SIMULATION DE LA FICHE PROJET ###")
    print("#"*70)

    # Sélectionner un projet pour la simulation (ex: projet_cir_alpha)
    # Dans une vraie application, on aurait une liste de tous les projets.
    # Ici, nous allons le chercher dans les projets du cabinet ou d'un client.
    # Pour simplifier, nous allons utiliser directement la référence que nous avons.
    projet_cible_id = projet_cir_alpha.id_projet

    # Créons une liste "globale" simulée de tous les projets pour get_projet_by_id
    tous_les_projets_simules = [projet_cir_alpha, projet_ademe_beta]
    # Dans une vraie app, cette liste viendrait d'une base de données ou d'un gestionnaire d'état.

    projet_pour_fiche = get_projet_by_id(projet_cible_id, tous_les_projets_simules)

    if projet_pour_fiche:
        utilisateur_courant_pour_fiche = consultant_alice # Simuler que c'est Alice qui regarde

        # Afficher la fiche projet initiale
        print_fiche_projet(projet_pour_fiche, utilisateur_courant_pour_fiche)

        # --- Simulation d'actions ---
        print("\n--- SIMULATION D'ACTIONS SUR LA FICHE PROJET ---")

        # 1. Modifier le statut du projet
        print(f"\nAction 1: Modifier statut du projet '{projet_pour_fiche.titre_projet}' de '{projet_pour_fiche.statut_pipeline.value}' vers '{StatutPipelineProjet.DEPOT.value}'...")
        time.sleep(0.01) # Simule un petit délai et aide à l'unicité des ID/timestamps
        update_statut_projet(projet_pour_fiche, StatutPipelineProjet.DEPOT)
        print(f"Statut du projet mis à jour. Nouvelle date de MàJ: {projet_pour_fiche.date_mise_a_jour.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        print_fiche_projet(projet_pour_fiche, utilisateur_courant_pour_fiche)

        # 2. Ajouter une aide au projet
        print(f"\nAction 2: Ajouter une aide au projet '{projet_pour_fiche.titre_projet}'...")
        time.sleep(0.01)
        add_aide_to_projet(projet_pour_fiche, nom_aide="Aide Régionale Innov+", lien_aide="http://region.innov.com", remarque="Dossier urgent")
        print("Aide ajoutée.")
        print_fiche_projet(projet_pour_fiche, utilisateur_courant_pour_fiche)

        # 3. Créer un nouveau livrable pour le projet
        print(f"\nAction 3: Créer un nouveau livrable (Dossier Technique) pour '{projet_pour_fiche.titre_projet}'...")
        time.sleep(0.01)
        nouveau_livrable_tech = create_livrable_pour_projet(
            projet=projet_pour_fiche,
            type_livrable=TypeLivrable.CIR, # Supposons un autre type pour varier
            fichier_associe="/chemin/vers/dossier_technique_alpha.pdf",
            cree_par=consultant_alice,
            statut_validation=StatutValidationLivrable.BROUILLON
        )
        print(f"Nouveau livrable '{nouveau_livrable_tech.id_livrable}' créé.")
        print_fiche_projet(projet_pour_fiche, utilisateur_courant_pour_fiche)

        # 4. Modifier le statut d'un livrable existant
        # Prenons le premier livrable de la liste (qui devrait être le plus récent après tri)
        livrables_actuels = get_livrables_par_projet(projet_pour_fiche)
        if livrables_actuels:
            livrable_a_modifier = livrables_actuels[0] # Le plus récent
            print(f"\nAction 4: Modifier statut du livrable '{livrable_a_modifier.id_livrable}' ({livrable_a_modifier.type_livrable.value}) vers '{StatutValidationLivrable.VALIDE.value}'...")
            time.sleep(0.01)
            update_statut_livrable(livrable_a_modifier, StatutValidationLivrable.VALIDE, projet_pour_fiche)
            print("Statut du livrable mis à jour.")
            print_fiche_projet(projet_pour_fiche, utilisateur_courant_pour_fiche)
        else:
            print("\nAction 4: Aucun livrable à modifier.")

    else:
        print(f"Erreur: Projet avec ID '{projet_cible_id}' non trouvé pour afficher la fiche.")

    print("\n" + "#"*70)
    print("### SIMULATION DE LA FICHE CLIENT (ORGANISATION) ###")
    print("#"*70)

    # Sélectionner une organisation pour la simulation (ex: client_alpha)
    toutes_les_organisations_simulees = [cabinet_conseil, client_alpha, client_beta]
    org_cible_id = client_alpha.id_organisation

    organisation_pour_fiche = get_organisation_by_id(org_cible_id, toutes_les_organisations_simulees)

    if organisation_pour_fiche:
        # Simuler que c'est l'admin Bob qui regarde la fiche du client Alpha
        utilisateur_courant_pour_fiche_org = admin_bob

        # Afficher la fiche client initiale
        print_fiche_client(organisation_pour_fiche, utilisateur_courant_pour_fiche_org)

        # --- Simulation d'actions sur la Fiche Client ---
        print("\n--- SIMULATION D'ACTIONS SUR LA FICHE CLIENT ---")

        # 1. Modifier les informations de l'organisation
        nouveau_nom_org = "Entreprise Alpha (MàJ)"
        print(f"\nAction 1: Modifier nom de l'organisation '{organisation_pour_fiche.nom}' vers '{nouveau_nom_org}'...")
        time.sleep(0.01)
        update_organisation_info(organisation_pour_fiche, nom=nouveau_nom_org)
        print(f"Informations de l'organisation mises à jour.")
        print_fiche_client(organisation_pour_fiche, utilisateur_courant_pour_fiche_org)

        # 2. Ajouter un nouvel utilisateur à l'organisation
        nouvel_utilisateur_eva = Utilisateur(
            id_utilisateur="user_eva",
            nom="Eva Employée",
            email="eva@alpha-maj.com",
            role=RoleUtilisateur.CLIENT,
            organisation=None # Sera défini par add_utilisateur_a_organisation
        )
        print(f"\nAction 2: Ajouter nouvel utilisateur '{nouvel_utilisateur_eva.nom}' à '{organisation_pour_fiche.nom}'...")
        time.sleep(0.01)
        add_utilisateur_a_organisation(organisation_pour_fiche, nouvel_utilisateur_eva)
        print(f"Utilisateur '{nouvel_utilisateur_eva.nom}' ajouté. Organisation de Eva: {nouvel_utilisateur_eva.organisation.nom if nouvel_utilisateur_eva.organisation else 'N/A'}")
        print_fiche_client(organisation_pour_fiche, utilisateur_courant_pour_fiche_org)

        # 3. Ajouter un nouveau projet à l'organisation (et l'associer à un consultant)
        id_projet_nouveau_gamma = f"proj_gamma_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        nouveau_projet_gamma = Projet(
            id_projet=id_projet_nouveau_gamma,
            titre_projet="Projet Gamma - Alpha (Nouveau)",
            consultant_referent=consultant_alice # Alice gère aussi ce nouveau projet
        )
        # Le statut par défaut est IDEE, l'organisation cliente sera mise par add_projet_a_organisation

        print(f"\nAction 3: Ajouter nouveau projet '{nouveau_projet_gamma.titre_projet}' à '{organisation_pour_fiche.nom}'...")
        time.sleep(0.01)
        add_projet_a_organisation(organisation_pour_fiche, nouveau_projet_gamma)
        # Ne pas oublier d'ajouter aussi ce projet aux projets du consultant référent et au cabinet
        consultant_alice.projets_associes.append(nouveau_projet_gamma)
        if organisation_pour_fiche.type_org == TypeOrganisation.CLIENT_FINAL:
             # Si le cabinet doit aussi lister les projets de ses clients (même s'il n'est pas le porteur)
             # Cela dépend de la logique métier. Ici, on suppose que le cabinet InnovConseil suit les projets de ses clients.
             if consultant_alice.organisation == cabinet_conseil and cabinet_conseil != organisation_pour_fiche:
                 add_projet_a_organisation(cabinet_conseil, nouveau_projet_gamma)


        print(f"Projet '{nouveau_projet_gamma.titre_projet}' ajouté. Client du projet: {nouveau_projet_gamma.organisation_cliente.nom if nouveau_projet_gamma.organisation_cliente else 'N/A'}")
        print_fiche_client(organisation_pour_fiche, utilisateur_courant_pour_fiche_org)

        # 4. (Optionnel) Supprimer un utilisateur (Charlie ClientA)
        id_user_a_supprimer = client_charlie.id_utilisateur
        print(f"\nAction 4: Supprimer utilisateur '{client_charlie.nom}' (ID: {id_user_a_supprimer}) de '{organisation_pour_fiche.nom}'...")
        time.sleep(0.01)
        if remove_utilisateur_de_organisation(organisation_pour_fiche, id_user_a_supprimer):
            print(f"Utilisateur '{client_charlie.nom}' supprimé.")
            # Vérifier si Charlie a été retiré des projets où il était associé (pas géré par la fonction de suppression d'org)
            # Pour la simulation, on peut le faire manuellement si besoin de propreté
            for projet_sim in tous_les_projets_simules + [nouveau_projet_gamma]:
                if client_charlie in projet_sim.consultant_referent.projets_associes: # Ceci est incorrect, charlie n'est pas consultant
                    pass # La liste projets_associes est sur l'utilisateur, pas sur le consultant_referent du projet
                # On devrait plutôt vérifier si Charlie est dans une liste "participants_client" du projet, si elle existait.
                # Pour l'instant, on suppose que son accès est juste via son appartenance à l'organisation.
                # Si Charlie était un consultant référent (improbable pour un client), il faudrait le gérer.
        else:
            print(f"Échec de la suppression de l'utilisateur ID {id_user_a_supprimer}.")
        print_fiche_client(organisation_pour_fiche, utilisateur_courant_pour_fiche_org)

    else:
        print(f"Erreur: Organisation avec ID '{org_cible_id}' non trouvée pour afficher la fiche client.")

# --- Fonctions et simulation pour le Module 2 : Recherche d'Aides ---

def print_resultats_recherche(resultats: list[Aide], criteres_recherche: dict, recherche_idx: int):
    """Affiche les résultats d'une recherche d'aides de manière formatée."""
    print("\n" + "~"*70)
    print(f"Résultats de la Recherche d'Aides #{recherche_idx}")
    print("~"*70)

    print("Critères de recherche appliqués:")
    for cle, valeur in criteres_recherche.items():
        if hasattr(valeur, 'value'): # Si c'est un Enum
            print(f"  - {cle}: {valeur.value}")
        else:
            print(f"  - {cle}: {valeur}")

    if not resultats:
        print("\nAucune aide trouvée pour ces critères.")
        print("~"*70 + "\n")
        return

    print(f"\n{len(resultats)} aide(s) trouvée(s):")
    for aide in resultats:
        print("-"*40)
        print(f"  Nom: {aide.nom} (ID: {aide.id_aide})")
        print(f"  Organisme: {aide.organisme_financeur}")
        print(f"  Type: {aide.type_aide.value}")
        print(f"  Description: {aide.description_courte}")
        if aide.montant_max_aide:
            print(f"  Montant max: {aide.montant_max_aide:,.0f} €".replace(",", " "))
        if aide.taux_aide:
            print(f"  Taux: {aide.taux_aide}")
        if aide.date_limite_depot:
            print(f"  Date limite: {aide.date_limite_depot.strftime('%d/%m/%Y')}")
        if aide.localisations_concernees:
            print(f"  Localisations: {', '.join([loc.value for loc in aide.localisations_concernees])}")
        if aide.natures_projet_eligibles:
            print(f"  Natures projet: {', '.join([nat.value for nat in aide.natures_projet_eligibles])}")
        if aide.secteurs_eligibles:
             print(f"  Secteurs: {', '.join([sec.value for sec in aide.secteurs_eligibles])}")
        if aide.tailles_entreprise_eligibles:
            print(f"  Tailles entreprise: {', '.join([taille.value for taille in aide.tailles_entreprise_eligibles])}")
        if aide.porteurs_eligibles:
            print(f"  Porteurs éligibles: {', '.join([porteur.value for porteur in aide.porteurs_eligibles])}")
        # ... ajouter d'autres champs si nécessaire pour le résumé
    print("~"*70 + "\n")


if __name__ == "__main__":
    main()

    # --- Simulation pour le Module 2 : Recherche d'Aides ---
    print("\n" + "#"*70)
    print("### SIMULATION DE RECHERCHE D'AIDES (MODULE 2) ###")
    print("#"*70)

    # Liste de critères de recherche à simuler
    recherches_a_simuler = [
        {"mot_cle": "innovation"},
        {"type_aide": TypeAide.SUBVENTION, "localisation": LocalisationEntreprise.FRANCE},
        {"secteur_activite": SecteurActivite.INDUSTRIE, "nature_projet": NatureProjet.INVESTISSEMENT_MATERIEL},
        {"taille_entreprise": TailleEntreprise.PME, "nb_etp_entreprise": 50, "ca_entreprise": 5000000},
        {"budget_projet": 100000, "localisation": LocalisationEntreprise.HAUTS_DE_FRANCE},
        {"trl_projet": 6}, # Projets avec TRL 6
        {"mot_cle": "écologie", "type_structure": TypeStructureEntreprise.ASSOCIATION}, # Test mot clé + structure
        {"localisation": LocalisationEntreprise.ILE_DE_FRANCE, "taille_entreprise": TailleEntreprise.TPE},
        {"mot_cle": "inexistant"}, # Test sans résultat
        {"nature_projet": NatureProjet.RECRUTEMENT, "secteur_activite": SecteurActivite.TOUS}
    ]

    for idx, criteres_test in enumerate(recherches_a_simuler):
        resultats = rechercher_aides(criteres_test, aides_simulees)
        print_resultats_recherche(resultats, criteres_test, recherche_idx=idx+1)
        # Pause légère pour mieux voir les résultats défiler si nombreux
        if len(resultats) > 2:
            time.sleep(0.01)
        elif len(resultats) == 0:
            time.sleep(0.01)

    # --- Simulation de l'association d'une aide à un projet ---
    print("\n" + "#"*70)
    print("### SIMULATION D'ASSOCIATION AIDE À PROJET (MODULE 2) ###")
    print("#"*70)

    # Choisir un projet pour l'association (ex: projet_cir_alpha)
    projet_pour_association = get_projet_by_id(projet_cir_alpha.id_projet, tous_les_projets_simules)

    # Choisir une aide à associer (ex: la première aide trouvée par la première recherche "innovation")
    # Ré-exécuter la première recherche pour obtenir une liste d'aides
    criteres_pour_association = recherches_a_simuler[0] # {"mot_cle": "innovation"}
    aides_trouvees_pour_assoc = rechercher_aides(criteres_pour_association, aides_simulees)

    if projet_pour_association and aides_trouvees_pour_assoc:
        aide_a_associer = aides_trouvees_pour_assoc[0] # Prendre la première aide trouvée

        print(f"\nTentative d'association de l'aide '{aide_a_associer.nom}' (ID: {aide_a_associer.id_aide})")
        print(f"au projet '{projet_pour_association.titre_projet}' (ID: {projet_pour_association.id_projet}).")

        # Afficher l'état des aides du projet AVANT association
        print("\nÉtat du projet AVANT association d'aide (section Aides):")
        # Pour afficher seulement la section des aides, on peut tricher un peu ou améliorer print_fiche_projet
        # Ici, on va ré-afficher une partie de la fiche projet manuellement pour se concentrer sur les aides.
        print("--- Section Aides du Projet ---")
        if projet_pour_association.aides_identifiees:
            for i, aide_associee in enumerate(projet_pour_association.aides_identifiees):
                 print(f"  - Aide {i+1}: {aide_associee.nom} (ID: {aide_associee.id_aide})")
        else:
            print("  Aucune aide actuellement associée.")
        print("-----------------------------")


        if associer_aide_a_projet(projet_pour_association, aide_a_associer):
            print(f"\nSuccès de l'association. Nouvelle date de MàJ du projet: {projet_pour_association.date_mise_a_jour.strftime('%Y-%m-%d %H:%M:%S.%f')}")

            # Afficher l'état des aides du projet APRÈS association
            print("\nÉtat du projet APRÈS association d'aide (section Aides):")
            print("--- Section Aides du Projet ---")
            if projet_pour_association.aides_identifiees:
                for i, aide_associee in enumerate(projet_pour_association.aides_identifiees):
                    print(f"  - Aide {i+1}: {aide_associee.nom} (ID: {aide_associee.id_aide})")
            else:
                print("  Aucune aide actuellement associée.") # Ne devrait pas arriver si succès
            print("-----------------------------")

            # Tentative d'associer la MÊME aide une seconde fois (devrait être empêché)
            print("\nTentative d'associer la MÊME aide une seconde fois...")
            associer_aide_a_projet(projet_pour_association, aide_a_associer)

        else:
            print("\nÉchec de l'association (peut-être déjà associée ou autre erreur).")

        # Pour une vue complète, on pourrait ré-appeler print_fiche_projet
        # print("\nAffichage complet de la Fiche Projet mise à jour:")
        # print_fiche_projet(projet_pour_association, admin_bob) # ou l'utilisateur courant pertinent

    elif not projet_pour_association:
        print("\nErreur: Projet pour association non trouvé.")
    elif not aides_trouvees_pour_assoc:
        print("\nErreur: Aucune aide trouvée avec les critères pour l'association (cela ne devrait pas arriver avec la recherche 'innovation').")
