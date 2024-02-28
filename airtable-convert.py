#!/usr/bin/env python3

"""
# TODO
- default behaviour is to display existing airtable column descriptions i.e. column name and column characteristic
- offer option to choose output format, json is the default format (json, csv)
- offer option to chosse which columns are converted, all by default
# EXAMPLE
airtable-convert                 < airtable.json : list in json format all column descriptions airtable file
airtable-convert -fmt csv        < airtable.json : convert all existing colomns from airtable file in csv format 
airtable-convert -c title -c age < airtable.json : convert *title* and *age* columns from airtable file in flat json format
"""

import sys
import json
import copy
import csv

identifiers = {
    'Titre': 'titre',                       # multilineText
    'Description': 'description',           # multilineText
    'Catégorie': 'categorie',               # multiSelect
    'Âge': 'age',                           # select
    'Langue': 'langue',                     # select
    'Producteur': 'producteur',             # multiSelect
    'Narrateur': 'narrateur',               # text
    'Créateur du pack': 'createur',         # multiSelect
    'Mots-clés': 'mots cles',               # multiSelect
    'Dernière modification': 'mise à jour', # formula
    'Award': 'qualite',                     # multiSelect
    'Téléchargement.': 'url',               # button
#    'Mise à jour': 'lienmiseajour',         # button
#    'Erreur': 'lienerreur'                  # button
}

def get_data(row, columns):
    acc = {}
    for column in columns:
        if column['name'] in identifiers.keys():
#           id=identifiers[column['name']]
            id = column['name']#.encode('ascii', 'ignore')
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

def flatDict(D,p=""):
    if not isinstance(D,dict):
        return {"":D}
    return {p+k+s:v for k,d in D.items() for s,v in flatDict(d,".").items()}

def flatData(data):
    lines = [*map(flatDict,data)]
    names = dict.fromkeys(k for d in lines for k in d)
    return [[*names]] + [ [*map(line.get,names)] for line in lines ]

def main():
    args = sys.argv[1:]
    if len(args) == 1 :
        jsonfile=args[0]
        print("opening", jsonfile, file=sys.stderr)
        with open(jsonfile, "r") as f:
            airtable = json.load(f)
        columns = airtable["columns"]
        data = [get_data(row, columns) for row in airtable["rows"]]
#        json.dump(data, sys.stdout, indent=4)
        writer = csv.writer(sys.stdout)
        for line in flatData(data):
            writer.writerow(line)
#            print(line)

    else :
        print("usage", sys.argv[0], "<airtable json finename>")

# Python boilerplate.
if __name__ == '__main__':
    main()
