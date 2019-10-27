from flask import Flask,render_template,request, url_for
from imdb import IMDb
from pprint import pprint as pp
import tmdbsimple as tmdb

tmdb.API_KEY = 'b888b64c9155c26ade5659ea4dd60e64'
app = Flask(__name__)

local=True
enable_extra=True
tmdb_img_url = r'https://image.tmdb.org/t/p/w342'


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
    if query:
        q_res = ia.search_movie(query)
        results = []
        if local:
            for m in q_res:
                try:
                    results.append({
                        'id': m.getID(),
                        'title': m['title'],
                        'year': m['startYear'],
                        'kind': m['kind']
                        })
                except KeyError:
                    pass
        else: #if not local
            results = [{
                'id': m.getID(),
                'cover': m['cover url'],
                'title': m['title'],
                'year': m['year'],
                'kind': m['kind']
                } for m in q_res]

        return render_template("search.html", results=results, local=local)
    else: #not query
        return ('')


@app.route('/info')
def info():
    movid = request.args.get('id', None)
    if not movid:
        return ('')
    else:
        mov = ia.get_movie(movid)
        movie={}

        #collect all the relevent info in a dict
        long_title = mov.get('long imdb title')
        title = mov.get('title')
        rating = mov.get('rating', None)
        genres = (", ".join(mov.get('genres', []))).title()
        runmin = 0
        if mov.get('runtime'):
            runmin = int(mov.get('runtime', ['0'])[0])
        runtime = "{}h {}m".format(runmin//60, runmin%60)

        director = ''
        writer = ''
        if mov.get('director'):
            director = mov.get('director')[0]['name']
        if mov.get('writer'):
            writer = mov.get('writer')[0]['name']

        cover = mov.get('full-size cover url', None)
        plot = mov.get('plot', [''])[0].split('::')[0]

        find = tmdb.Find('tt{:07}'.format(int(movid)))
        find.info(external_source='imdb_id')

        if (find.movie_results or find.tv_results) and enable_extra:
            if (find.movie_results and find.movie_results[0]['poster_path']
            and find.movie_results[0]['overview']):
                cover = tmdb_img_url + find.movie_results[0]['poster_path']
                plot = find.movie_results[0]['overview']
            elif (find.tv_results and find.tv_results[0]['poster_path']
            and find.tv_results[0]['overview']):
                cover = tmdb_img_url + find.tv_results[0]['poster_path']
                plot = find.tv_results[0]['overview']




        movie = {
                'long title': long_title,
                'title': title,
                'rating': rating if rating else '',
                'genres': genres,
                'runtime': runtime,
                'director': director,
                'writer': writer,
                'plot': plot if plot else '',
                'cover': cover if cover else ''
        }
        return render_template("info.html", movie=movie)
