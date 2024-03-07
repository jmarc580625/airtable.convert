#!/usr/bin/env python3

import argparse
import sys
import os

def fatal(source, message):
    error(source, message)
    exit()

def error(source, message):
    if source: source+=" :"
    print(source, message, file=sys.stderr)

def trace(name, value):
    return "{name}:{value}".format(name=name, value=value)

def debug(message):
    print("DEBUG", message, file=sys.stderr)

def check_rename(value):
    rename = value.split('=')
    if len(rename) != 2:
        raise argparse.ArgumentTypeError("%s bad rename syntax" % value)
    return {rename[0]:rename[1]}

class ParseRenameArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for v in values:
            rename = v.split('=')
            if len(rename) != 2:
                raise argparse.ArgumentError(self, "%s bad rename argument syntax, '=' missing" % v)
            getattr(namespace, self.dest)[rename[0]] = rename[1]

    
parser = argparse.ArgumentParser(description='convert airtable content')
parser.add_argument('-o', '--outformat', default='csv', choices=["json", "csv"], help='define output format, default is csv')
parser.add_argument('-f', '--file', type=argparse.FileType(), help='airtable file to be processed')
group = parser.add_mutually_exclusive_group()
group.add_argument('-x', '--exclude', action='extend', nargs='+', help='exclude column from extraction')
group.add_argument('-i', '--include', action='extend', nargs='+', help='include column in extraction')
parser.add_argument('-r', '--rename', action='extend', nargs='+', type=check_rename, help='rename column during extraction')

debug("... parsing args")
args=parser.parse_args()
if args.include is None and args.exclude is None and args.rename is not None:
    parser.error('-r requires -i or -x')


debug("... checking file")
if not args.file:
    if os.isatty(sys.stdin.fileno()):
        fatal(os.path.basename(sys.argv[0]), "need a file to process")
    else:
        args.file = sys.stdin

debug(trace("parser.prog", parser.prog))
debug(trace("outformat", args.outformat))
debug(trace("file", args.file))
debug(trace("include", args.include))
debug(trace("exclude", args.exclude))
debug(trace("rename", args.rename))

