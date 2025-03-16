# flask_live_search

Python and Javascript for live search (not autocomplete, for [OpenSearch](https://github.com/dewitt/opensearch) [suggestions](https://github.com/dewitt/opensearch/blob/master/mediawiki/Specifications/OpenSearch/Extensions/Suggestions/1.1/Draft%201.wiki) see [pyopensearch](https://hg.sr.ht/~clach04/pyopensearch))

Technique adopted from https://tutorial101.blogspot.com/2020/11/flask-mysql-jquery-ajax-live-search.html

## Setup

    python -m pip install flask

Known to work with Python versions:

  * 2.7.13
  * 3.7.3
  * 3.8.10

Known to work with Flask versions:

  * Flask 1.0.2
  * Flask 1.1.2
  * Flask 2.2.1

Front end uses Bootstrap (CSS only, v3.3-5.2 tested) and pure Javascript (no other dependencies).

## Demo

Default:

    python app.py

which will load into memory the contents of the file [entry_per_line_utf8.txt](https://github.com/clach04/flask_live_search/blob/main/entry_per_line_utf8.txt) (sample file contains 2-letter short code and country name mapping)

Specify different input text file for search demo (UNIX/Linux):

    env LIVE_SEARCH_ENTRIES_FILENAME=alternative_filename.txt python app.py

Specify different input text file for search demo (Microsoft Windows):

    set LIVE_SEARCH_ENTRIES_FILENAME=alternative_filename.txt
    python app.py
