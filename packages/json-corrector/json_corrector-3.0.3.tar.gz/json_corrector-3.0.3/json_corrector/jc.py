"""
Fixes data that is almost json but not enterily. This issues are fixed:
  - single quotes are changed to double quotes
  - booleans gets quoted

Compliant json gets printed.
"""
import sys
import re


import json
import argparse


class MultipleArgumentError(Exception):
    """Raise when multiple Arguments detected but only one is expected
    This could be due to powershell version 5 or prior. Use PowerShell Core instead.
    """
    pass


def process_input() -> str:
    """Gets and return str passed in either via positional or stdin."""


    parser = argparse.ArgumentParser(description=("Fixes data that is almost json"
                                                  " but not enterily."),
                                                  epilog="Compliant json gets printed.")
     # nargs = '*': powershell5 and prior cannot pass data like
     # '{"hello": "my-friend", "hello2": "my friend"}'
     # as one argument. This will be split into two arguments
     # 1. 'hello: my-friend, hello2: my'
     # 2. 'friend'}
     # To avoid program crash with missleading error, I will catch it this way.
    parser.add_argument('almost_json', help=("Data thats almost in json format,"
                                            " but not enterily."
                                            " E.g. double quotes instead of single quotes"),
                                            nargs='*')
    args = parser.parse_args()


    if len(args.almost_json) == 0:
        # Check if stdin is NOT connected to tty/terminal.
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        else:
            parser.error("No 'almost_json' provided. Provide 'almost_json' as an argument or via stdin.")
        
    elif len(args.almost_json) == 1:
        return args.almost_json[0]
    else:
        if "linux" in sys.platform:
            raise MultipleArgumentError(("Multiple Arguments detected."))
        if "win" in sys.platform:
            raise MultipleArgumentError(("Multiple Arguments detected. This could be due to"
                                     " PowerShell version 5 or prior."
                                     " Use PowerShell core instead."))


def replace_single_quotes(almost_json: str) -> str:
    """Replace single quotes with double quotes.
    Json requires double quotes for keys and vals.

    Example input:  {'bool1': True, 'bool2': false, 'nobool': 'True'}
    Example output: {"bool1": true, "bool2": false, "nobool": "True"}
    
    :returns: data with replaced single quotes
    """


    # and all matches are convert to lowercase
    return almost_json.replace("'",'"')


def fix_bools(almost_json: str) -> str:
    """Fix bools in almost json data.
    Json allows bool values only lowercase.

    Example input:  '{"bool1": True, "bool2": false, "nobool": "True"}'
    Example output: '{"bool1": true, "bool2": false, "nobool": "True"}'
    
    :returns: data with json-valid bool values
    """


    # from example, this are the matches (ex single quotes):
    # - '": True'
    # - '": false'
    regex = r'"[\s]*:[\s]*(True|False|true|false)'

    # and all matches are convert to lowercase
    return re.sub(regex,lambda match: match.group().lower() ,almost_json)


def put_missing_double_quotes(almost_json: str) -> str:
    """Put missing double quotes for keys and values in almost json data.
    Example input:  '{"nr1": "val1", nr2: val2}'
    Example output: '{"nr1": "val1", "nr2": "val2"}'

    :returns: fixed json data
    """
    regex= r'(?<=[,{}:])\s*((?!true|false)\w[\w\-]*)(?=(?:[^"]*"[^"]*")*[^"]*$)'
    repl = r'"\1"'

    return re.sub(regex,repl,almost_json,flags=re.M)


def main(almost_json: str):

    almost_json = replace_single_quotes(almost_json)
    almost_json = fix_bools(almost_json)
    almost_json = put_missing_double_quotes(almost_json)


    loaded = json.loads(almost_json)
    print(json.dumps(loaded))
 

if __name__ == "__main__":
    main(process_input())
