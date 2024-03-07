
"""
TODO:
    -   TRACE & DEBUG should be based upon logging feature instead of my own (over)simplified functions below
"""

import sys
import os
import json
import copy
import csv
import argparse

#-------------------------------------------------------------------------------
def trace(name, value):
    return f'{name}:{value}'

def debug(message):
    print('DEBUG', message, file=sys.stderr)

#def debug(x): pass
#-------------------------------------------------------------------------------

def get_dict(columns):
    dict = {} 
    for column in columns:
        col = {}
        col.update({'description':column['description']})
        col.update({'type':column['type']})
        dict.update({column['name']:col})
    return dict

def get_data(row, columns, dict):
    acc = {}
    for column in columns:
        if column['name'] in dict.keys():
            id = dict[column['name']].get('alias') or column['name']
            if row['cellValuesByColumnId'].get(column['id']):
                val = row['cellValuesByColumnId'][column['id']]
                if column['type'] == 'select':
                    acc[id] = column['typeOptions']['choices'][val]['name']
                elif column['type'] == 'button':
                    acc[id] = val['url']
                elif column['type'] == 'multiSelect':
                    values = []
                    for v in val:
                        values.append(column['typeOptions']['choices'][v]['name'])
                    acc[id] = '\n'.join(values)
                else:
                    acc[id] = val
    return acc

def flatDict(D,p=''):
    if not isinstance(D,dict):
        return {'':D}
    return {p+k+s:v for k,d in D.items() for s,v in flatDict(d,'.').items()}

def flatData(data):
    lines = [*map(flatDict,data)]
    names = dict.fromkeys(k for d in lines for k in d)
    return [[*names]] + [ [*map(line.get,names)] for line in lines ]

class ParseRename(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not getattr(namespace, self.dest):
            setattr(namespace, self.dest, dict())
        for v in values:
            rename = v.split('=')
            if len(rename) != 2:
                raise argparse.ArgumentError(self, f"bad rename argument syntax, '=' missing in '{v}'")
            getattr(namespace, self.dest).update({rename[0]:rename[1]})

def main():
    
    parser = argparse.ArgumentParser(description='convert airtable content',
                                     epilog='any include, exclude or rename parameter which did not match an airtable dictionary entry is silently ignored')
    parser.add_argument('-f', '--file', type=argparse.FileType(), help='airtable file to be processed (default: stdin)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x', '--exclude', nargs='+', action='extend', help='exclude column during convertion')
    group.add_argument('-i', '--include', nargs='+', action='extend', help='include column during convertion')
    parser.add_argument('-r', '--rename', nargs='+', action=ParseRename, help='rename column during convertion')
    parser.add_argument('-o', '--outformat', default='csv', choices=['json', 'csv'], help='define output format (default: csv)',)
    parser.add_argument('-v', '--verbose', default=0, action='count', help='define trace verbosity level',)
    
    debug('... parsing args')
    args=parser.parse_args()

    debug('... checking file')
    if not args.file:
        if os.isatty(sys.stdin.fileno()):
            parser.exit('need a file to process')
        else:
            args.file = sys.stdin

    debug(args)
    debug(trace("aaa", "bbb"))

    debug('... loading')
    airtable = json.load(args.file)
    columns = airtable['table']['columns']
    rows = airtable['table']['rows']

    debug('... extracting dict')
    dict = get_dict(columns)

    if not args.include and not args.exclude and not args.rename: 
        debug('... exporting dict')
        if args.outformat == 'csv':
            w = csv.DictWriter(sys.stdout, fieldnames='name description type'.split())
            for k,v in dict.items():
                D = v.copy() # So dict is not modified.
                D['name'] = k
                w.writerow(D)
        else:
            print(dict)
        exit()

    [dict[name].update({'keep':True}) for name in args.include or [] if name in dict.keys()]

    if args.exclude:
        [dict[name].update({'keep':True}) for name in dict.keys() if name not in args.exclude] 
 
    for name in list(dict.keys()):
        if args.rename and name in args.rename.keys():
            dict[name].update({'keep':True})
            dict[name].update({'alias':args.rename[name]})
        elif not dict[name].get('keep'):
            del dict[name]

    debug('... extracting data')
    data = [get_data(row, columns, dict) for row in rows]

    if args.outformat == 'csv':
        debug('... writing csv output')
        writer = csv.writer(sys.stdout)
        for line in flatData(data):
            writer.writerow(line)
    else:
        debug('... writing json output')
        print(data)

# Python boilerplate.
if __name__ == '__main__':
    main()
