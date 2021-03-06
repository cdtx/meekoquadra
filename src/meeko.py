# -*- coding: Latin-1 -*-
from openpyxl import load_workbook

class MeekoFile:
    def __init__(self, filename):
        self.workbook = None
        self.filename = filename

    @classmethod
    def parse(cls, filename):
        ret = cls(filename)

        ret.workbook = load_workbook(filename)

        return ret

    def worksheet(self, name, line_cls):
        headers = []

        gen_rows = self.workbook[name].rows

        # Get headers line
        first_row = next(gen_rows)
        headers = [cell.value for cell in first_row]

        # Get data
        ret = []
        for row in gen_rows:
            ret_line = line_cls()
            for i, data in enumerate(row):
                ret_line[headers[i]] = data.value
            ret.append(ret_line)

        return ret


    def factures(self):
        return self.worksheet('Factures', MeekoFactures)

    def paiements(self):
        return self.worksheet('Paiements', MeekoPaiements)

class MeekoFactures(dict):
    pass

class MeekoPaiements(dict):
    pass



if __name__ == '__main__':
    meeko_file = MeekoFile.parse('Excel plusieurs mois MEEKO.xlsx')

    print(meeko_file.factures())
    print(meeko_file.paiements())

