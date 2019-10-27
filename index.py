from flask import Flask,render_template,request, url_for
from imdb import IMDb
from pprint import pprint as pp

app = Flask(__name__)

local=False;

if local:
    ia = IMDb('s3', 'mysql+mysqldb://may:venom123@localhost/imdb')
else:
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
        q_res = ia.search_movie(query)
        if local:
            results = []
            for a in q_res:
                try:
                    results.append(
                            {'title': a['title'],
                             'year': a['startYear'],
                             'kind': a['kind']
                             }
                    )
                except KeyError:
                    pass
        else: #if not local
            results = []
            try:
                results = [{
                    'id': m.getID(),
                    'cover': m['cover url'],
                    'title': m['title'],
                    'year': m['year'],
                    'kind': m['kind']
                    } for m in q_res]
            except KeyError:
                pass
            return render_template("search.html", results=results, local=local)


@app.route('/info')
def info():
    movid = request.args.get('id', None)
    if not movid:
        return ('')
    else:
        mov = ia.get_movie(movid)

        #collect all the relevent info in a dict
        long_title = mov['long imdb title']
        title = mov['title']
        rating = mov['rating']
        genres = ", ".join(mov['genres'])
        runtime = "{}h {}m".format(int(mov['runtime'][0])//60,
                int(mov['runtime'][0])%60
                )
        plot = mov['plot'][0].split('::')[0]
        director = mov['director'][0]['name']
        writer = mov['writer'][0]['name']
        cover = mov['full-size cover url']

        movie = {
                'long title': long_title,
                'title': title,
                'rating': rating,
                'genres': genres,
                'runtime': runtime,
                'plot': plot,
                'director': director,
                'writer': writer,
                'cover': cover
        }

        return render_template("info.html", movie=movie, runtime=runtime)
