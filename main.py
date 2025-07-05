from modeles import (
    Utilisateur, Organisation, Projet, Livrable,
    RoleUtilisateur, TypeOrganisation, StatutPipelineProjet, TypeLivrable, StatutValidationLivrable
)
from datetime import datetime

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

if __name__ == "__main__":
    main()
