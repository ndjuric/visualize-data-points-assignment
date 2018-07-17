from flask import render_template, current_app
from . import main


@main.route('/')
def map_view():
    return render_template('index.html')


@main.route('/docs')
def api():
    api_url = current_app.config['API_DOCS_URL']
    return render_template('docs.html', doc_link=api_url)



