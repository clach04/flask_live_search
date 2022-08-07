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
import sys

import flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

live_search_entries = []
f = codecs.open('entry_per_line_utf8.txt', encoding='utf8')
for line in f:
    line = line.strip()
    if line:
        live_search_entries.append(line.lower())
f.close()
print('Total entries %r' % len(live_search_entries))
 
@app.route("/")
def index():
    return render_template("livesearch.html")
     
@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    #print(request.args.to_dict())
    #print(request.get_json(force=True))
    #print(request.form.to_dict())
    term = (request.args or {}).get('text') or (request.get_json(force=True) or {}).get('text') or (request.form or {}).get("text")
    print('term: %r' % term)
    if not term:
        # fixme error handling
        print('fixme error handling')
        result = []
    else:
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
