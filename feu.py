# -*- coding: Latin-1 -*-
import sys, os, re
import logging
from datetime import datetime


from quadra import QuadraFile, QuadraLine
from meeko import MeekoFile

def run(in_file_name, out_file_name=None):
    logging.info('Input file name : %s', file_name)

    # Compute the output file name if not forced
    if not out_file_name:
        now = datetime.now()
        out_file_name = '{}_{}.txt'.format(os.path.splitext(in_file_name)[0], now.strftime('%y%m%d_%H%M%S'))
        logging.info('Output file name : {}'.format(out_file_name))

    # Load meeko file
    meeko_file = MeekoFile.parse(in_file_name)

    # Create quadra file
    quadra_file = QuadraFile(out_file_name)

    
    # Pour chaque facture, une ligne de debit, une ligne de credit, code VE
    for facture in meeko_file.factures():
        qline = QuadraLine()
        qline['type'] = 'M'
        num_compte = facture['Compte Client']
        if num_compte:
            qline['num_compte'] = num_compte
        qline['num_folio'] = '000'
        # Convert 15/06/1984 to 150684
        qline['date_ecriture'] = datetime.strptime(facture['Date'], '%d/%m/%Y').strftime('%d%m%y')
        qline['sens'] = 'D'
        # Convertion en centimes + padding avec 0 + signe
        qline['montant_cts'] = '+' + ('0'*12 + str(int(facture['Montant'] * 100)))[-12:]
        qline['code_devise'] = 'EUR'
        qline['code_journal_2'] = 'VE'
        qline['code_journal_3'] = 'VE '
        qline['libelle_30'] = '{} - {}'.format(facture['No'], facture['Client'])
        # Tous les chiffres qui terminent le facture
        qline['num_alphanumerique'] = ''.join(re.findall(r'(\d)', facture['No']))

        quadra_file.append(qline)

        qline['num_compte'] = '70610000'
        qline['sens'] = 'C'

        quadra_file.append(qline)

    # Pour chaque peiement, une ligne de debit, une ligne de credit, code BQ
    for paiement in meeko_file.paiements():
        qline = QuadraLine()
        qline['type'] = 'M'
        qline['num_compte'] = '51200000'
        qline['num_folio'] = '000'
        # Convert 15/06/1984 to 150684
        qline['date_ecriture'] = datetime.strptime(paiement['Payé le'], '%d/%m/%Y').strftime('%d%m%y')
        qline['sens'] = 'D'
        # Convertion en centimes + padding avec 0 + signe
        qline['montant_cts'] = '+' + ('0'*12 + str(int(paiement['Montant'] * 100)))[-12:]
        qline['code_devise'] = 'EUR'
        qline['code_journal_2'] = 'BQ'
        qline['code_journal_3'] = 'BQ '
        qline['libelle_30'] = '{} - {}'.format(paiement['Facture'], paiement['Client'])
        # Tous les chiffres qui terminent le facture
        qline['num_alphanumerique'] = ''.join(re.findall(r'(\d)', paiement['Facture']))

        quadra_file.append(qline)

        num_compte = paiement['Compte Client']
        if num_compte:
            qline['num_compte'] = num_compte
        qline['sens'] = 'C'

        quadra_file.append(qline)

    quadra_file.save()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y - %H:%M:%S', level=7)

    file_name = 'Excel bis sept à decemrbe 2021.xlsx'
    run(file_name)
