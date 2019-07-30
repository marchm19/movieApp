from app import app
import os
from flask import render_template, request, redirect
from app.models import model, formopener

@app.route('/')
@app.route('/index')
def index():
    popMovies = model.printPop()
    upcomingMovies=model.printUp()
    return render_template('index.html', popMovies = popMovies,upcomingMovies=upcomingMovies )

@app.route('/search',methods=['GET','POST'])
def search():
    searchList = model.userSearch(dict(request.form)['movieName'])
    if(len(searchList)==0):
        return render_template("noresults.html", searchList=searchList)
    return render_template("search.html", searchList=searchList)

@app.route('/results/<movieID>', methods=['GET','POST'])
def results(movieID):
    if request.method=='GET':
        return render_template('results.html',movie=model.searchResult(movieID),similarMovies=model.getSimilarMovie(movieID), cast=model.getCast(movieID),crew=model.getCrew(movieID))
    # else:
    #     return render_template('results.html',movieName=model.userSearch(dict(request.form)['movieName']))



from flask_pymongo import PyMongo
# name of database
app.config['MONGO_DBNAME'] = 'goldmansachs' 

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:VQCSruWQzJMLdFIE@cluster0-e45ty.mongodb.net/goldmansachs?retryWrites=true&w=majority' 

mongo = PyMongo(app)

@app.route('/userfav')
def userfav():
    collection = mongo.db.favMovies
    collection = collection.find({})
    print(collection)
    return render_template('userfav.html',collection=collection)

@app.route('/timeRec')
def timeRec():
    return render_template('timeRec.html')

 
@app.route('/addMovie',methods=['GET',"POST"])
def addMovie():
    formData = dict(request.form)
    movieName=formData["movie-name"]
    name = formData["name"]
    if request.method=='GET':
        return "You haven't submitted the favorite movie form. Please go back and fill out the form"
    else:
        if movieName == "" or name == "":
            return "You haven't submitted the favorite movie form. Please go back and fill out the form"
        else:
            collection=mongo.db.favMovies
            collection.insert({"movie-name":movieName,"name":name})
            return "Your favorite Movie has been added"
        
        
@app.route('/calcTime',methods=['GET',"POST"])
def calcTime():
    formData = dict(request.form)
    hours=formData["hours"]
    minn = formData["minn"]
    if (minn=="" and hours==""):
        return "You haven't submitted the time form. Please go back and fill it out."
    else:
        totalTime=60*int(hours) + int(minn)
        searchList = model.findMovieTimeRecs(totalTime)
        return render_template('searchTimeResults.html', searchList = searchList , hours=hours, minn=minn )
    