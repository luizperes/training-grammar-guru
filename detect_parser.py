#!/usr/bin/env python3

import argparse
import subprocess
import json
from collections import namedtuple
from pathlib import Path

import detect

CHECK_SYNTAX_THROW_BIN = (*detect.TOKENIZE_JS_BIN, '--check-syntax-throw')

class SyntaxError(namedtuple('SyntaxError', 'message')):
    @classmethod
    def from_json(cls, obj):
        """
        Converts the JSON error into an error object
        """
        return SyntaxError(message=obj['error'])

    def __str__(self):
        return self.message

def check_syntax_throw(*, filename=None, **kwargs):
    """
    >>> check_syntax('function name() {}')
    True
    >>> check_syntax('function name() }')
    json as exception
    False
    """
    code = ''
    with open(filename) as f:
        code = f.read()
    with detect.synthetic_file(code) as source_file:
        status = subprocess.run(CHECK_SYNTAX_THROW_BIN,
                                stdin=source_file,
                                stdout=subprocess.PIPE)
    err = None
    if (status.returncode != 0):
        j = json.loads(status.stdout.decode('UTF-8'))
        err = SyntaxError.from_json(j)

    print(err)

    return (err, status.returncode == 0)

def add_common_args(parser):
    parser.add_argument('filename', nargs='?', type=Path,
                        default=Path('/dev/stdin'))

parser = argparse.ArgumentParser()
add_common_args(parser)
parser.set_defaults(func=check_syntax_throw)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.func:
        args.func(**vars(args))
    else:
        parser.print_usage()
        exit(-1)
