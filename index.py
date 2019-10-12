from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html",msg="YO");

@app.route('/SearchResult',methods=['GET','POST'])
def search():
   details=request.form; #Getting an array with details inputted
   srch=details['search']; #Getting value of search element 
   return render_template("search.html",srch=srch); #Passing the value of search text field to variable srch, to use in html .

@app.route('/TopRated',methods=['GET','POST']) #the def name is used while using url_for.
def rated():
   return render_template("rated.html");  #render template directs to html page rated.html present in templates directory.

@app.route('/Trending',methods=['GET','POST'])
def trend():
   return render_template("trend.html");


if __name__ =='__main__':
    app.run()
