import sys, os
from copy import deepcopy
from collections import OrderedDict

from .quadra_defs import entry_fields

class QuadraFile:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []

    @classmethod
    def parse(cls, filename):
        ret = cls(filename)
        with open(filename, 'r') as fin:
            for line in fin:
                ret.lines.append(QuadraLine.parse(line))
        return ret

    def append(self, line):
        self.lines.append(deepcopy(line))

    def save(self):
        with open(self.filename, 'w') as fout:
            fout.write('\n'.join(map(QuadraLine.encode, self.lines)))

class QuadraLine:
    def __init__(self):
        self.fields = OrderedDict()
        self.mandatory = {}

        for _key, _name, _start, _len, _mandatory in entry_fields:
            self.fields[_key] = ''
            self.mandatory[_key] = _mandatory

    @classmethod
    def parse(cls, line):
        ret = cls()
        ret.decode(line)
        return ret

    def decode(self, line):
        for _key, _name, _start, _len, _mandatory in entry_fields:
            _value = line[_start - 1 : _start - 1 +_len]

            self.fields[_key] = _value

    def encode(self):
        # Create empty string with max field size
        last_start, last_len = entry_fields[-1][2:4]
        ret = [' '] * (last_start + last_len - 1)
        for _key, _name, _start, _len, _mandatory in entry_fields:
            # Apply the maximum pading, then truncate the result to fit in all cases
            t_field = (self.fields[_key] + ' '*_len)[:_len]
            ret[_start - 1: _start + _len - 1] = t_field

        return ''.join(ret)

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __str__(self):
        ret = []
        for k,v in self.fields.items():
            ret.append('{}{} : {}'.format('*' if self.mandatory[k] else '' ,k, v))

        return '\n'.join(ret)

if __name__ == '__main__':
    quadra_file = QuadraFile.parse('Fichier qui fonctionnait avant.TXT')
    print(quadra_file.lines[0])

    line = QuadraLine()
    line.fields['date_ecriture'] = '150684'
    line.fields['libelle_30'] = 'There is a good side to every situation'
    print(line.encode())
    
    quadra_file = QuadraFile('new_quadra_file.txt')
    line = QuadraLine()
    line.fields['date_ecriture'] = '150684'
    line.fields['libelle_30'] = 'There is a good side to every situation'
    quadra_file.append(line)
    line = QuadraLine()
    line.fields['date_ecriture'] = '051015'
    line.fields['libelle_30'] = 'Hello world'
    quadra_file.append(line)

    quadra_file.save()


