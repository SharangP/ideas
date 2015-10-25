#!/usr/bin/env python

import os
import sys
import json
import yaml
import datetime
import decimal

from flask import Flask, render_template, redirect, request, url_for

SCHEMA = {
    'required': {
        'title': str,
        'desc': str
    },
    'optional': {
        'details': list
    }
}


app = Flask(__name__, template_folder='.')
app.config['DEBUG'] = True

def load_file(path):
    try:
        with open(path, 'r') as f:
            return yaml.load(f), None
    except Exception as e:
        return None, e

def find_schema_errors(rows):
    def annotate(row):
        errors = []
        for field_name, field_type in SCHEMA['required'].iteritems():
            if not isinstance(row.get(field_name), field_type):
                errors.append({
                    "field_name": field_name,
                    "field_type": field_type,
                    "value": row.get(field_name)
                })
        for field_name, field_type in SCHEMA['optional'].iteritems():
            if field_name in row and not isinstance(row[field_name], field_type):
                errors.append({
                    "field_name": field_name,
                    "field_type": field_type,
                    "value": row[field_name]
                })

        return (row, errors)

    return map(annotate, rows)

def save_the_shit():
    pass

@app.route('/')
def index():
    return redirect(url_for('.view', list_file='list.yaml'))

@app.route('/<list_file>')
def view(list_file):
    raw_rows, err = load_file(list_file)
    if err:
        return "%s is fucked: %s" % (list_file, err)

    rows = find_schema_errors(raw_rows)
    any_errors = any(map(lambda row: bool(row[1]), rows))
    return render_template('view.html', name=list_file, rows=rows, any_errors=any_errors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
