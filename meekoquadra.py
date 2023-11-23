#!/usr/bin/env python3
# -*- coding: Latin-1 -*-
import sys, os, re
import logging
import tempfile
import argparse
from datetime import datetime


from src.quadra import QuadraFile, QuadraLine
from src.meeko import MeekoFile

# TODO: Move to a json with configurable file path
VARIANTS = {
    'LILI': {
        'facture': {
            'code_devise': 'EUR',
            'code_journal_2': 'VE',
            'code_journal_3': 'VE ',
            'num_compte': '70610000',
        },
        'paiement': {
            'code_devise': 'EUR',
            'code_journal_2': 'BQ',
            'code_journal_3': 'BQ ',
            'num_compte': '51200000'
        },
    },
    'LEAM': {
        'facture': {
            'code_devise': 'EUR',
            'code_journal_2': 'BQ',
            'code_journal_3': 'BQ ',
            'num_compte': '70610000',
        },
        'paiement': {
            'code_devise': 'EUR',
            'code_journal_2': 'BQ',
            'code_journal_3': 'BQ ',
            'num_compte': '51200000'
        },
    },
    'LOU': {
        'facture': {
            'code_devise': 'EUR',
            'code_journal_2': 'V1',
            'code_journal_3': 'V1 ',
            'num_compte': '70610000',
        },
        'paiement': {
            'code_devise': 'EUR',
            'code_journal_2': 'B1',
            'code_journal_3': 'B1 ',
            'num_compte': '51200000'
        },
    },
}

def run(in_file_path, out_file_path, variant):
    logging.debug('Input file path : %s', in_file_path)
    logging.debug('Output file path : {}'.format(out_file_path))
    logging.debug('Variant : {}'.format(variant))

    # Load meeko file
    meeko_file = MeekoFile.parse(in_file_path)

    # Create quadra file
    quadra_file = QuadraFile(out_file_path)

    variant_dict = VARIANTS[variant]
    
    # Pour chaque facture, une ligne de debit, une ligne de credit, code journal
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

            qline['code_devise'] = variant_dict['facture']['code_devise']
            qline['code_journal_2'] = variant_dict['facture']['code_journal_2']
            qline['code_journal_3'] = variant_dict['facture']['code_journal_3']

            op_debug = 'libelle'
            qline['libelle_30'] = '{} - {}'.format(facture['No'], facture['Client'])

            # Tous les chiffres qui terminent le facture
            op_debug = 'numero de facture'
            qline['num_alphanumerique'] = ''.join(re.findall(r'(\d)', facture['No']))

            quadra_file.append(qline)

            qline['num_compte'] = variant_dict['facture']['num_compte']
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
            qline['num_compte'] = variant_dict['paiement']['num_compte']
            qline['num_folio'] = '000'

            # Convert 15/06/1984 to 150684
            op_debug = 'date'
            qline['date_ecriture'] = datetime.strptime(paiement['Payé le'], '%d/%m/%Y').strftime('%d%m%y')
            qline['sens'] = 'D'

            # Convertion en centimes + padding avec 0 + signe
            op_debug = 'montant'
            qline['montant_cts'] = '+' + ('0'*12 + str(int(paiement['Montant'] * 100)))[-12:]
            qline['code_devise'] = variant_dict['paiement']['code_devise']
            qline['code_journal_2'] = variant_dict['paiement']['code_journal_2']
            qline['code_journal_3'] = variant_dict['paiement']['code_journal_3']

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

    in_file_path = os.path.abspath(in_args.in_file_name)

    # Output (def) and log in the same folder as the input file
    working_dir = os.path.dirname(os.path.abspath(in_args.in_file_name))

    # Logger to console
    stream_log = logging.StreamHandler()
    stream_log.setLevel(logging.INFO)
    # Logger to file
    debug_file_path = os.path.join(working_dir, 'meekoquadra.log')
    file_log = logging.FileHandler(debug_file_path)
    file_log.setLevel(logging.DEBUG)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y - %H:%M:%S', handlers = (stream_log, file_log), level=logging.DEBUG)

    # Require user to select variant
    variant = input(''.join([f'{k} ? ' for k in VARIANTS.keys()]) + ': ').upper()
    if not variant in VARIANTS.keys():
        logging.error(f'{variant} not in {list(VARIANTS.keys())}')
        exit()

    # Compute the output file name if not forced
    if not in_args.out_file_name:
        now = datetime.now()
        out_file_path = os.path.join(
            working_dir,
            '{}_{}_{}.txt'.format(os.path.splitext(in_args.in_file_name)[0], variant, now.strftime('%y%m%d_%H%M%S')),
        )
    else:
        out_file_path = os.path.abspath(in_args.out_file_name)

    logging.info(f'Debug file name : {debug_file_path}')

    try:
        logging.info(f'Input file name : {in_file_path}')
        run(in_file_path, out_file_path, variant)
        logging.info(f'Output file name : {out_file_path}')
        logging.info('Conversion OK !!')
    except Exception as e:
        logging.error(e)


    os.system('pause')

