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
    try:
        movieName=dict(request.form)['movieName']
        searchList = model.userSearch(movieName)
        if(len(searchList)==0):
            return render_template("noresults.html", searchList=searchList)
        return render_template("search.html", searchList=searchList)
    except:
        return render_template("noresults.html",searchList=[])
    
@app.route('/genresearch/<genreName>/<genreID>',methods=['GET','POST'])
def genresearch(genreName,genreID):
    discoverList = model.genreDiscover(genreID)
    return render_template("genresearch.html",discoverList=discoverList,genreName=genreName)

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

 
@app.route('/addMovie', methods=['GET',"POST"])
def addMovie():
    formData = dict(request.form)
    movieName=formData["movie-name"]
    name = formData["name"]
    favID=model.userSearch(movieName)[0]["id"]
    if request.method=='GET':
        return "You haven't submitted the favorite movie form. Please go back and fill out the form"
    else:
        if movieName == "" or name == "":
            return "You haven't filled out the whole favorite movie form. Please go back and fill out the form"
        else:
            collection=mongo.db.favMovies
            collection.insert({"movie-name":movieName,"name":name,"id":favID})
            return render_template("addedPage.html")

@app.route('/findTheaters',methods=['GET',"POST"])
def findTheaters():
    return render_template("findTheaters.html")

@app.route('/calcNearby',methods=['GET',"POST"])
def calcNearby():
    formData = dict(request.form)
    address=formData["address"]
    lat=model.findLatitude(address)
    longi=model.findLongitude(address)
    thea=model.findTheaters(lat,longi)
    return render_template("printTheaters.html",thea=thea,address=address)  

@app.route('/calcTime',methods=['GET',"POST"])
def calcTime():
    formData = dict(request.form)
    hours=formData["hours"]
    minn = formData["minn"]
    if request.method=='GET':
        return "You haven't submitted the time form. Please go back and fill it out."
    else:
        hoursName="hours"
        minName="minutes"
        if (minn==""):
            minn = 0
        if (hours==""):
            hours = 0
        totalTime=60*int(hours) + int(minn)
        searchList = model.findMovieTimeRecs(totalTime)
        if(hours=="1"):
            hoursName="hour"
        if(minn=="1"):
            minName="minute"
        return render_template('searchTimeResults.html', searchList = searchList , hours=hours, minn=minn,hoursName=hoursName,minName=minName )