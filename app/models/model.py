import requests

# jackReacher = requests.get("https://api.themoviedb.org/3/search/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&query=avengers")
# print(jackReacher.json()['results'])
# jackReacherID = requests.get('https://api.themoviedb.org/3/movie/75780/videos?api_key=d7f3201b6c7960f747f412e7c08d8993')
#print(jackReacherID.json())

def userSearch(movieName):
    searchByName = requests.get("https://api.themoviedb.org/3/search/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&query="+movieName).json()['results']
    return searchByName
    #return movie.search(movieName)[0:5]
    
def searchResult(movieID):
    result = requests.get("https://api.themoviedb.org/3/movie/"+str(movieID)+"?api_key=d7f3201b6c7960f747f412e7c08d8993&append_to_response=videos,credits,reviews").json()
    return result
    
def printPop():
    discoverPop = requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=d7f3201b6c7960f747f412e7c08d8993&language=en-US&page=1").json()['results']
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

def getCast(movieID):
    cast = []
    for mem in searchResult(movieID)['credits']['cast'][0:6]:
        mem['personInfo']=requests.get("https://api.themoviedb.org/3/person/"+str(mem['id'])+"?api_key=d7f3201b6c7960f747f412e7c08d8993").json()
        cast.append(mem)
    return cast

    
def getCrew(movieID):
    crew = []
    for mem in searchResult(movieID)['credits']['crew'][0:6]:
        mem['personInfo']=requests.get("https://api.themoviedb.org/3/person/"+str(mem['id'])+"?api_key=d7f3201b6c7960f747f412e7c08d8993").json()
        crew.append(mem)
    return crew

def genreDiscover(genreID):
    discoverList = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=d7f3201b6c7960f747f412e7c08d8993&with_genres="+str(genreID)).json()
    return discoverList['results']

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="FinTech App")
def findLatitude(address):
    location = geolocator.geocode(address)
    latitude=location.latitude
    return latitude
def findLongitude(address):
    location = geolocator.geocode(address)
    longitude=location.longitude
    return longitude
def findTheaters(latitude,longitude):
    arr=[]
    theaters = requests.get("https://api.internationalshowtimes.com/v4/cinemas/?apikey=O7adMPVLBzHIbhlmVpocOSXy8x7qUdLM&location="+str(latitude)+","+str(longitude)+"&distance=10").json()
    return theaters['cinemas']


