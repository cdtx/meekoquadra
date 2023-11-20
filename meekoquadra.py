# -*- coding: Latin-1 -*-
import sys, os, re
import logging
import tempfile
import argparse
from datetime import datetime


from src.quadra import QuadraFile, QuadraLine
from src.meeko import MeekoFile

def run(in_file_name, out_file_name):
    logging.info('Input file name : %s', in_file_name)
    logging.info('Output file name : {}'.format(out_file_name))

    # Load meeko file
    meeko_file = MeekoFile.parse(in_file_name)

    # Create quadra file
    quadra_file = QuadraFile(out_file_name)

    
    # Pour chaque facture, une ligne de debit, une ligne de credit, code VE
    logging.info(f'Parsing "Factures" sheet')
    for facture in meeko_file.factures():
        logging.debug(str(facture))
        try:
            # current operation name to help debugging
            op_debug = ''
            qline = QuadraLine()
            qline['type'] = 'M'

            op_debug = 'compte client'
            num_compte = facture['Compte Client']
            if num_compte:
                qline['num_compte'] = num_compte

            qline['num_folio'] = '000'

            # Convert 15/06/1984 to 150684
            op_debug = 'date'
            qline['date_ecriture'] = datetime.strptime(facture['Date'], '%d/%m/%Y').strftime('%d%m%y')

            qline['sens'] = 'D'

            # Convertion en centimes + padding avec 0 + signe
            op_debug = 'montant'
            qline['montant_cts'] = '+' + ('0'*12 + str(int(facture['Montant'] * 100)))[-12:]

            qline['code_devise'] = 'EUR'
            qline['code_journal_2'] = 'VE'
            qline['code_journal_3'] = 'VE '

            op_debug = 'libelle'
            qline['libelle_30'] = '{} - {}'.format(facture['No'], facture['Client'])

            # Tous les chiffres qui terminent le facture
            op_debug = 'numero de facture'
            qline['num_alphanumerique'] = ''.join(re.findall(r'(\d)', facture['No']))

            quadra_file.append(qline)

            qline['num_compte'] = '70610000'
            qline['sens'] = 'C'

            quadra_file.append(qline)
        except Exception as e:
            logging.error(f'Probleme de {op_debug}')
            raise e

    # Pour chaque peiement, une ligne de debit, une ligne de credit, code BQ
    logging.info(f'Parsing "Paiements" sheet')
    for paiement in meeko_file.paiements():
        logging.debug(str(paiement))
        try:
            op_debug = ''
            qline = QuadraLine()
            qline['type'] = 'M'
            qline['num_compte'] = '51200000'
            qline['num_folio'] = '000'

            # Convert 15/06/1984 to 150684
            op_debug = 'date'
            qline['date_ecriture'] = datetime.strptime(paiement['Payé le'], '%d/%m/%Y').strftime('%d%m%y')
            qline['sens'] = 'D'

            # Convertion en centimes + padding avec 0 + signe
            op_debug = 'montant'
            qline['montant_cts'] = '+' + ('0'*12 + str(int(paiement['Montant'] * 100)))[-12:]
            qline['code_devise'] = 'EUR'
            qline['code_journal_2'] = 'BQ'
            qline['code_journal_3'] = 'BQ '

            op_debug = 'libelle'
            qline['libelle_30'] = '{} - {}'.format(paiement['Facture'], paiement['Client'])

            # Tous les chiffres qui terminent le facture
            op_debug = 'numero de facture'
            qline['num_alphanumerique'] = ''.join(re.findall(r'(\d)', paiement['Facture']))

            quadra_file.append(qline)

            op_debug = 'numero de compte client'
            num_compte = paiement['Compte Client']
            if num_compte:
                qline['num_compte'] = num_compte
            qline['sens'] = 'C'

            quadra_file.append(qline)
        except Exception as e:
            logging.error(f'Probleme de {op_debug}')
            raise e


    quadra_file.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert meeko *.xlsx to quadra *.txt')

    parser.add_argument('in_file_name', type=str, help='Fichier meeko (*.xlxs)')
    parser.add_argument('--out', type=str, required=False, dest='out_file_name', help='Fichier quadra (*.txt), optionnel')

    in_args = parser.parse_args()

    # Compute the output file name if not forced
    if not in_args.out_file_name:
        now = datetime.now()
        in_args.out_file_name = '{}_{}.txt'.format(os.path.splitext(in_args.in_file_name)[0], now.strftime('%y%m%d_%H%M%S'))

    # Logger to console
    stream_log = logging.StreamHandler()
    stream_log.setLevel(logging.DEBUG)
    # Logger to file
    debug_file_path = os.path.join(tempfile.gettempdir(), 'DEBUG_' + in_args.out_file_name)
    file_log = logging.FileHandler(debug_file_path)
    file_log.setLevel(logging.DEBUG)

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y - %H:%M:%S', handlers = (stream_log, file_log), level=logging.DEBUG)

    try:
        run(**vars(in_args))
    except Exception as e:
        logging.error(e)

    logging.info(f'Debug file name : {debug_file_path}')

    os.system('pause')

