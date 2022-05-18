
entry_fields = [
    ["type", "Type = M", 1, 1, True],
    ["num_compte", "Numero de compte", 2, 8, True],
    ["code_journal_2", "Code journal sur 2 caract. (obligatoire meme si renseigne en 111 sur 3)", 10, 2, True],
    ["num_folio", "Numero folio (a initialiser a '000' si pas de folio)", 12, 3, True],
    ["date_ecriture", "Date ecriture (JJMMAA)", 15, 6, True],
    ["code_libelle", "Code libelle", 21, 1, False],
    ["libelle_20", "Libelle libre", 22, 20, False],
    ["sens", "Sens Debit/Credit (D/C)", 42, 1, True],
    ["montant_cts", "Montant en centimes signe (position 43=signe)", 43, 13, True],
    ["compte_contrepartie", "Compte de contrepartie", 56, 8, False],
    ["date_echeance", "Date echeance (JJMMAA)", 64, 6, False],
    ["code_lettrage", "Code lettrage", 70, 2, False],
    ["code_stat", "Code statistiques", 72, 3, False],
    ["num_piece_5", "Numero de piece sur 5 caracteres maximum", 75, 5, False],
    ["code_affaire", "Code affaire", 80, 10, False],
    ["quantite_1", "Quantite 1", 90, 10, False],
    ["num_piece_8", "Numero de piece jusqu'a 8 caracteres", 100, 8, False],
    ["code_devise", "Code devise (FRF ou EUR, Espace = FRF, ou Devise)", 108, 3, False],
    ["code_journal_3", "Code journal sur 3 caracteres", 111, 3, True],
    ["flag_code_tva", "Flag Code TVA gere dans l'ecriture = O (oui)", 114, 1, False],
    ["code_tva_1", "Code TVA = 0 a 9", 115, 1, False],
    ["methode_calcul", "Methode de calcul TVA = D (Debits) ou E (Encaissements)", 116, 1, False],
    ["libelle_30", "Libelle ecriture sur 30 caract. (blanc si renseigne en 22 sur 20 caract.)", 117, 30, False],
    ["code_tva_2", "Code TVA sur 2 caracteres", 147, 2, False],
    ["num_alphanumerique", "Numero de piece alphanumerique sur 10 caract.", 149, 10, False],
    ["montant", "Montant dans la devise (en centimes signes position 169=signe)", 169, 13, False],
    ["piece_jointe", "Piece jointe a l'ecriture (format du nom du fichier : 8 caracteres suivis d'une extension sur 3 caracteres)", 182, 12, False],
    ["quantite_2", "Quantite 2", 194, 10, False],
    ["num_unique", "NumUniq", 204, 10, False],
    ["code_operateur", "Code operateur", 214, 4, False],
    ["date_system", "Date systeme", 218, 14, False],
]