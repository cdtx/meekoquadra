# -*- coding: Latin-1 -*-
from openpyxl import load_workbook

def extract_xlsx(file_path):
    wb = load_workbook(file_path)

    headers = []

    gen_rows = wb['Factures'].rows

    # Get headers line
    first_row = next(gen_rows)
    headers = [cell.value for cell in first_row]

    # Get data
    ret = []
    for row in gen_rows:
        ret_line = {}
        for i, data in enumerate(row):
            ret_line[headers[i]] = data.value
        ret.append(ret_line)

    return ret

if __name__ == '__main__':
    data = extract_xlsx('export excel nouveau logiciel à convertir ou adapter factures.xlsx')


