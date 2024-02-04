#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Based on https://tutorial101.blogspot.com/2020/11/flask-mysql-jquery-ajax-live-search.html
https://www.youtube.com/watch?v=Us8gBacBDJ8
but without errors ;-) and plain text for simple demo setup
"""

import codecs
import json
import os
import sqlite3  # TODO make optional?
import sys

import flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

index_location = ':memory:'
#db = sqlite3.connect(index_location)
db = sqlite3.connect(index_location, check_same_thread=False)  # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id -1212130624 and this is thread id -1239499968.
cur = db.cursor()
cur.execute('pragma compile_options;')
available_pragmas = cur.fetchall()

if ('ENABLE_FTS5',) not in available_pragmas:
    raise NotImplementedError('FTS5 missing %r' % (available_pragmas, ) )
cur.execute("CREATE VIRTUAL TABLE lines USING fts5(line, tokenize='porter')")

# TODO close...

live_search_entries = []
# TODO filename from env variable
f = codecs.open(os.environ.get('LIVE_SEARCH_ENTRIES_FILENAME', 'entry_per_line_utf8.txt'), encoding='utf8')
for line in f:
    line = line.strip()
    if line:
        live_search_entries.append(line.lower())
        cur.execute("""INSERT INTO lines (line) VALUES (?)""", (line, ) )
f.close()
db.commit()
print('Total entries %r' % len(live_search_entries))
 
@app.route("/")
def index():
    return render_template("livesearch.html")
     
@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    #print(request.args.to_dict())
    #print(request.get_json(force=True))
    #print(request.form.to_dict())
    request_args = request.args or {}
    request_form = request.form or {}
    request_json = request.get_json(force=True, silent=True) or {}  # how to handle errors, when force true applied
    #request_json = request.get_json() or {} # Need true for POST from web page to work
    term = (request_args or {}).get('text') or (request.get_json(force=True) or {}).get('text') or (request_form or {}).get("text")
    print('raw term: %r' % term)
    if term is not None:
        term = term.strip()
        term = term.lower()
    print('term: %r' % term)
    if not term:
        # fixme error handling - or return everything, probably better option... or option on URL to dictate empty versus full result set
        print('fixme error handling')
        result = []
    else:
        print('term: %r' % term)
        fts = request_args.get('fts') or request_form.get("fts")  or request_json.get('fts')
        print('fts: %r' % fts)
        if fts is not None:
            if isinstance(fts, (str, bytes)):
                fts = fts.strip()
                fts = fts.lower()
        if fts:
            result = ["au : australia",]  # TODO
            """
            sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id -1212130624 and this is thread id -1239499968.
            """
            cur.execute("""SELECT
                                line
                            FROM lines(?)
                            ORDER  BY rank""",
                            (term, ) )
            result = [v[0] for v in cur.fetchall()]
        else:
            # not FTS
            result = [v for v in live_search_entries if term in v]
    print('Entries returned %r for %r' % (len(result), term))
    #return jsonify(result)  # Microsoft Edge warnings https://github.com/pallets/flask/pull/4752
    resp = flask.Response(response=json.dumps(result),
                    status=200,
                    mimetype='application/json; charset=utf-8')
    resp.headers['X-Content-Type-Options'] = 'nosniff'  # direct browser to NOT sniff the mimetype, i.e. do not guess
    return resp

 
if __name__ == "__main__":
    # debug defaults, not for production!
    flask_config = {
        #'debug': False,
        'debug': True,
        'port': 5000,
        #'host': '127.0.0.1',
        'host': '0.0.0.0',
        #'ssl_context': 'adhoc'
        #'ssl_context': (cert_path, key_path)
    }
    protocol = 'http'
    if flask_config.get('ssl_context'):
        protocol = 'https'
    print('Python %s on %s' %(sys.version, sys.platform))
    print('Flask %s Serving on %s://%s:%d' % (flask.__version__, protocol, flask_config['host'], flask_config['port']))
    app.run(**flask_config)
