from modeles import (
    Utilisateur, Organisation, Projet, Livrable,
    RoleUtilisateur, TypeOrganisation, StatutPipelineProjet, TypeLivrable, StatutValidationLivrable
)
from services import get_projets_par_statut, get_projets_recents, get_livrables_recents
from datetime import datetime

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


if __name__ == "__main__":
    main()
