"""Routes for flask app."""  # pylint: disable=cyclic-import

import os.path as op
import csv
from pprint import pprint
from flask import render_template
# from flask import request
from datapp import app


@app.route('/', methods=['GET'])
def index():
    """View displays or processes get form. Hashes and displays input text."""
    datadir = op.dirname(op.abspath(__file__))
    datafile = op.join(datadir, 'static/data/StateChildrenData.csv')

    with open(datafile) as csvfile:
        reader = csv.reader(csvfile)
        header_row = [column_head.strip() for column_head in next(reader)]

    short_labels = ['state',
                    'num_fams',
                    'num_fams_w_kids',
                    'tot_num_kids',
                    "ave_num_kids_per_fam",
                    "ave_num_kids_per_fam_w_kids"]

    header_label_dict = get_header_from_file(datafile, short_labels)
    data_db = parse_data_file(datafile)
    print('\n'.join(': '.join(item)) for item in header_label_dict.items())
    pprint([row for row in data_db])
    return render_template("index.html",
                           page_title="Children Data by State",
                           header_row=header_row,
                           data_db=data_db)

def parse_data_file(filename):
    data_converters = [str,
                       lambda x: int(x.replace(',', '')),
                       lambda x: int(x.replace(',', '')),
                       lambda x: int(x.replace(',', '')),
                       lambda x: float(x.replace(',', '')),
                       lambda x: float(x.replace(',', ''))]
    table = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skipping header row
        for row in reader:
            table.append(converter(item)
                         for item, converter in zip(row, data_converters))
    return table

def get_header_from_file(filename, short_labels):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header_row = [column_head.strip() for column_head in next(reader)]
    return dict(zip(short_labels, header_row))
