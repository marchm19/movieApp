from tmdbv3api import TMDb
import requests
tmdb = TMDb()
tmdb.api_key = 'd7f3201b6c7960f747f412e7c08d8993'

from tmdbv3api import Movie, Discover

movie = Movie()

# jackReacher = requests.get("https://api.themoviedb.org/3/search/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&query=avengers")
# print(jackReacher.json()['results'])
# jackReacherID = requests.get('https://api.themoviedb.org/3/movie/75780/videos?api_key=d7f3201b6c7960f747f412e7c08d8993')
#print(jackReacherID.json())

def userSearch(movieName):
    search=[]
    # print(len(movie.search(movieName)))
    
    # for i in range(0,min(len(movie.search(movieName)),5)):
    #     search.append(movie.search(movieName)[i].title)
    # return search
    searchByName = requests.get("https://api.themoviedb.org/3/search/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&query="+movieName).json()['results']
    return searchByName
    #return movie.search(movieName)[0:5]
    
def searchResult(movieID):
    result = requests.get("https://api.themoviedb.org/3/movie/"+str(movieID)+"?api_key=d7f3201b6c7960f747f412e7c08d8993&append_to_response=videos,credits").json()
    return result

#print(searchResult(420818)['credits'])
# print(searchResult(19404))

# discover = Discover()
# popular = discover.discover_movies({
#     'sort_by': 'popularity.desc','year':'2019'
# })


def printPop():
    discoverPop = requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=d7f3201b6c7960f747f412e7c08d8993&language=en-US&page=1").json()['results']
    #https://api.themoviedb.org/3/discover/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&sort_by=popularity.desc&year=2019
    # popMovies=[]
    # for i in range(0,10):
    #     popMovies.append(popular[i].title)
    return discoverPop[0:10]   

def printUp():
    upcomingMov = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key=d7f3201b6c7960f747f412e7c08d8993&language=en-US&page=1").json()['results']
    return upcomingMov[3:13]    
    
def findMovieTimeRecs(time):
    discoverTime = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&with_runtime.lte="+str(time)+"&with_runtime.gte=1").json()['results']
    return discoverTime[0:10]
    
def getSimilarMovie(movieID):
    similarMovies = requests.get("https://api.themoviedb.org/3/movie/"+str(movieID)+"/similar?api_key=d7f3201b6c7960f747f412e7c08d8993").json()['results']
    return similarMovies[0:6]
#print(getSimilarMovie(19404))

def getCast(movieID):
    cast = searchResult(movieID)['credits']['cast']
    return cast[0:6]
    
def getCrew(movieID):
    crew = searchResult(movieID)['credits']['crew']
    return crew[0:6]
    
    
import hashlib
import time

def Sha256Encode(stringToEncode):
    s = hashlib.sha256();
    s.update(stringToEncode.encode('utf-8'))
    result = s.hexdigest()
    return result

def intlShowtimesapi():
    response = requests.get("https://api.internationalshowtimes.com/v4/movies?apikey=O7adMPVLBzHIbhlmVpocOSXy8x7qUdLM&search_query=Avengers: Endgame&search_field=title")
intlShowtimesapi()

apikeysig = "apikey=egucb4e8bfrn4pv3guj4ktqn&sig="+Sha256Encode("egucb4e8bfrn4pv3guj4ktqnWQfu6MRysT"+str(int(time.time())))
print(apikeysig)
print(requests.get("http://api.fandango.com/v3?theatersbypostalcodesearch&postalcode=07073&"+apikeysig))
# from tmdb3 import set_key,searchMovie, Movie
# set_key('d7f3201b6c7960f747f412e7c08d8993')

# def userSearch(movieName):
#     search = []
#     res = searchMovie(movieName)
#     for i in range(0, min(len(res),5)):
#         search.append(res)
#     # if len(search) > 0:    
#     return search
#     # else:
#     #     return "Your search did not return any results"
    
# def searchResult(movieName):
#     return searchMovie(movieName)[0]
    
# def printPop():
#     popMovies = Movie.mostpopular()[0:10]
    # return popMovies
    # 
    
# print(requests.get("http://api.fandango.com/v3/?op=performancesbymoviepostalcodesearch&postalcode=07073&api_key=egucb4e8bfrn4pv3guj4ktqn&sig=WQfu6MRysT")