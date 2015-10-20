#!/usr/bin/env python

import os
import sys
import yaml
import argparse

SCHEMA = {
    'required': {
        'title': str,
        'desc': str
    },
    'optional': {
        'details': list
    }
}

def find_schema_errors(rows):
    errors = False
    for i, row in enumerate(rows):
        for field_name, field_type in SCHEMA['required'].iteritems():
            if not isinstance(row[field_name], field_type):
                print("Row %d: %s is not %s" % (i, field_name, field_type))
        for field_name, field_type in SCHEMA['optional'].iteritems():
            if field_name in row and not isinstance(row[field_name], field_type):
                errors = True
                print("Row %d: %s is not %s" % (i, field_name, field_type))

    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', default='list.yaml', help='The file to verify')

    options = parser.parse_args()
    if not os.path.exists(options.file):
        print("You suck %s doesn't exist" % options.file)
        sys.exit(1)

    try:
        with open(options.file, 'r') as f:
            rows = yaml.load(f)
            print("lets see here...")
            if find_schema_errors(rows):
                print("You sir, are a fucking idiot. Exiting.")
                sys.exit(4)
            else:
                print("You sir, are not a fucking idiot.")
                sys.exit(0)
    except IOError:
        print("You suck %s is not for plebs" % options.file)
        sys.exit(2)
    except Exception as e:
        print("You sir, are a fucking idiot: %s" % e)
        sys.exit(3)
