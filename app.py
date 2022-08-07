#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Based on https://tutorial101.blogspot.com/2020/11/flask-mysql-jquery-ajax-live-search.html
https://www.youtube.com/watch?v=Us8gBacBDJ8
but without errors ;-) and plain text for simple demo setup
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

games = []
f = open('entry_per_line_utf8.txt', encoding='utf8')
for line in f:
    line = line.strip()
    if line:
        games.append(line.lower())
f.close()
print('Total entries %r' % len(games))
 
@app.route("/")
def index():
    return render_template("livesearch.html")
     
@app.route("/livesearch", methods=["POST","GET"])
def livesearch():
    term = request.form.get("text")
    print('term: %r' % term)
    result = [v for v in games if term in v]
    print('Entries returned %r for %r' % (len(result), term))
    return jsonify(result)

 
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
    print('Serving on %s://%s:%d' % (protocol, flask_config['host'], flask_config['port']))
    app.run(**flask_config)