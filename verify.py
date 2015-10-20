#!/usr/local/bin/python

import yaml

SCHEMA = {
        'required': {'title': str, 'desc': str},
        'optional': {'details': list}
        }

def verify_schema(rows):
    for row in rows:
        for field_name, field_type in SCHEMA['required'].iteritems():
            assert isinstance(row[field_name], field_type)
        for field_name, field_type in SCHEMA['optional'].iteritems():
            if field_name in row:
                assert isinstance(row[field_name], field_type)

if __name__ == '__main__':
    with open('list.yaml', 'r') as f:
        y = yaml.load(f)

    print "lets see here..."
    verify_schema(y)
    print "you sir, are not a fucking idiot"
