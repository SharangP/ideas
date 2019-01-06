#!/usr/bin/env python

import yaml

from flask import Flask, render_template, redirect, url_for

SCHEMA = {
    'required': {
        'title': str,
        'desc': str
    },
    'optional': {
        'details': list,
        'comments': list
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
        seen = set()
        for field_name, field_type in SCHEMA['required'].items():
            if not isinstance(row.get(field_name), field_type):
                errors.append({
                    "field_name": field_name,
                    "field_type": field_type,
                    "value": row.get(field_name),
                    "message": "This is required"
                })

            seen.add(field_name)
        for field_name, field_type in SCHEMA['optional'].items():
            if field_name in row and not isinstance(row[field_name], field_type):
                errors.append({
                    "field_name": field_name,
                    "field_type": field_type,
                    "value": row[field_name],
                    "message": "This is optional"
                })

            seen.add(field_name)

        other_fields = set(row.keys()) - seen
        for other in other_fields:
            errors.append({
                "field_name": other,
                "value": row[other],
                "message": "This is not allowed"
            })

        return (row, errors)

    return list(map(annotate, rows))

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
    return render_template('view.html', name=list_file, num_items=len(rows), rows=rows, any_errors=any_errors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
