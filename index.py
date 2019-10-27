from flask import Flask,render_template,request, url_for
from imdb import IMDb

app = Flask(__name__)

ia = IMDb()

@app.route('/')
def index():
    print(url_for('search'))
    return render_template("index.html");

@app.route('/search')
def search():
    query = request.args.get('q', None)
    if not query:
        return ('')
    else:
        movies = ia.search_movie(query)
        mov = [dict(m) for m in movies]
        # results = {'results': mov}
        print(mov[0]['cover url'])

    return render_template("search.html", results=mov)


