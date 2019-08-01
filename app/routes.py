from app import app
import os
from flask import render_template, request, redirect, session, url_for, escape
from app.models import model, formopener


app.secret_key=b'xa5x88x92x15Rxd4.Ex9dLxb3fxcexd9]'
@app.route('/')
@app.route('/index')
def index():
    popMovies = model.printPop()
    upcomingMovies=model.printUp()
    return render_template('index.html', popMovies = popMovies,upcomingMovies=upcomingMovies)
    
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
    return render_template("genresearch.html",discoverList=discoverList,genreName=genreName, genreID = genreID)

@app.route('/results/<movieID>', methods=['GET','POST'])
def results(movieID):
    if request.method=='GET':
        return render_template('results.html',movieID = movieID, movie=model.searchResult(movieID),similarMovies=model.getSimilarMovie(movieID), cast=model.getCast(movieID),crew=model.getCrew(movieID))
    # else:
    #     return render_template('results.html',movieName=model.userSearch(dict(request.form)['movieName']))



from flask_pymongo import PyMongo
app.config['MONGO_DBNAME'] = 'goldmansachs' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:VQCSruWQzJMLdFIE@cluster0-e45ty.mongodb.net/goldmansachs?retryWrites=true&w=majority' 

mongo = PyMongo(app)

import bcrypt

@app.route('/login/<type>/<path:redirectedFrom>', methods=['GET','POST'])
def login(type, redirectedFrom):
    msg = ""
    if request.method == 'GET':
        if type=="logout":
            session.pop('username',None)
            return redirect("/"+redirectedFrom)
        return render_template('login.html',msg=msg,redirectedFrom=redirectedFrom)
    else:
        collection=mongo.db.userLogin
        userData = dict(request.form)
        if type == 'login':
            if list(collection.find({'username':userData['username']})):
                user = list(collection.find({'username':userData['username']}))[0]
                if bcrypt.checkpw(userData['password'].encode('utf-8'),user['password'].encode('utf-8')):
                    session['username']=user['username']
                    return redirect('/'+redirectedFrom)
                else:
                    msg = "Invalid Username/Password"
            else:
                msg = "Invalid Username/Password"
        elif type=="signup":
            if list(collection.find({'username':userData['username']})):
                msg = "That username is already in use"
            else:
                collection.insert({'username':userData['username'],'password': bcrypt.hashpw(userData['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')})
                session['username']=userData['username']
                return redirect('/'+redirectedFrom)
        elif type=="logout":
            session.pop('username',None)
            return redirect('/'+redirectedFrom)
        return render_template('login.html',msg=msg)
            
        
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
    if movieName == "" or name == "":
            return render_template("noInput.html")
    try:
        favID=model.userSearch(movieName)[0]["id"]
    except:
        return render_template("invalidFav.html")
    if request.method=='GET':
        return render_template("noInput.html")
    else:
        try:
            collection=mongo.db.favMovies
            collection.insert({"movie-name":movieName,"name":name,"id":favID})
            return render_template("addedPage.html")
        except:
            return render_template("invalidFav.html")

@app.route('/findTheaters',methods=['GET',"POST"])
def findTheaters():
    return render_template("findTheaters.html")

@app.route('/calcNearby',methods=['GET',"POST"])
def calcNearby():
    formData = dict(request.form)
    address=formData["address"]
    if(address==""):
        return render_template("noInput.html")
    try:
        lat=model.findLatitude(address)
        longi=model.findLongitude(address)
        thea=model.findTheaters(lat,longi)
        return render_template("printTheaters.html",thea=thea,address=address) 
    except:
        return render_template("noresults.html")

@app.route('/calcTime',methods=['GET',"POST"])
def calcTime():
    formData = dict(request.form)
    hours=formData["hours"]
    minn = formData["minn"]
    hoursName=""
    minName=""
    if (minn==""):
        minn = 0
    if (hours==""):
        hours = 0
    if request.method=='GET':
        return render_template("noInput.html")
    elif( int(hours)==0 and int(minn)==0 ):
        return render_template("noInput.html")
    elif ( (int(hours)<0) or (int(minn)<0)  ):
        return render_template("noresults.html")
    else:
        hoursName+=str(hours)
        minName+=str(minn)
        totalTime=60*int(hours) + int(minn)
        searchList = model.findMovieTimeRecs(totalTime)
        if(hours=="1"):
            hoursName+=" hour"
        else:
            hoursName+=" hours"
        if(minn=="1"):
            minName+=" minute"
        else:
            minName+=" minutes"
        if(int(hours)==0):
            hoursName=""
        if(int(minn)==0):
            minName=""
        elif(int(hours)!=0):
            hoursName+=" and "
        return render_template('searchTimeResults.html', searchList = searchList , hoursName=hoursName,minName=minName )
        
@app.route('/searchCategory',methods=['GET',"POST"])
def searchCategory():
    genreIDS=[{"genre":"Drama","id":"18"},{"genre":"Crime","id":"80"},{"genre":"Comedy","id":"35"},{"genre":"Family","id":"10751"},{"genre":"Science Fiction","id":"18"},{"genre":"Thriller","id":"53"},{"genre":"Horror","id":"27"},{"genre":"Adventure","id":"12"},{"genre": "Music", "id":"10402",}, {"genre":"Action", "id":"28"}, {"genre":"Animation", "id":"16"},{"genre":"History", "id":"36"},{"genre":"War", "id":"10752"},{"genre":"Romance", "id":"10749"}]
    formData = dict(request.form)
    cat=formData["cat"]
    try:
        for element in genreIDS:
            if element["genre"]==cat.capitalize():
                id=element["id"]
        moviesInGenre = model.genreDiscover(id)
    except:
        return render_template("noresults.html")
    return render_template('categoryResults.html',moviesInGenre=moviesInGenre,cat=cat.capitalize())        








