import numpy as np
import pandas as pd
import datetime
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests
from tmdbv3api import Movie
from tmdbv3api import TMDb
from werkzeug.utils import redirect

app = Flask(__name__)

tmdb = TMDb()
tmdb.api_key = 'e03d67a61df283f6611e5d38a58c2456'
data = 'data/Movies.csv'

def create_similarity(data):
    movie = pd.read_csv(data)
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(movie['comb'])
    # creating a similarity score matrix
    similar = cosine_similarity(count_matrix)
    return similar

def find_recommendation(title,data):
    title = title.lower()
    try:
        similarity.shape
    except:
        similarity = create_similarity(data)
    movie_data = pd.read_csv(data)
    if title not in movie_data['movie_title'].unique():
        return('Sorry! The movie your searched is not in our database. Please check the spelling or try with some other movies')
    else:
        idx = movie_data.loc[movie_data['movie_title']==title].index[0]
        lst = list(enumerate(similarity[idx]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11]
        l = []
        for each in lst:
            movie_idx = each[0]
            l.append(movie_data['movie_title'][movie_idx])
        return l

def list_of_genres(genre_json):
    if genre_json:
        genres = []
        genre_str = ", " 
        for i in range(0,len(genre_json)):
            genres.append(genre_json[i]['name'])
        return genre_str.join(genres)

def date_convert(date):
    date = pd.to_datetime(date)
    day = date.day
    year = date.year
    month = datetime.datetime.strptime("{}".format(date.month), "%m").strftime("%B")
    return day,month,year

def movie_runtime(duration):
    if duration%60==0:
        return "{:.0f} hours".format(duration/60)
    else:
        return "{:.0f} hours {} minutes".format(duration/60,duration%60)



@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":
        movie_name = request.form.get('movie_name')
    return render_template("index.html")

@app.route("/recommend",methods=["GET","POST"])
def recommend():
    return render_template("recommend.html")


if __name__ == "__main__":
    app.run(debug=True)





    # movie_name = "avatar"
    # recommended_movies = find_recommendation(movie_name, data)
    # movie_name = movie_name.upper()
    # movie_details = {}

    # if type(recommended_movies) == type('string'): # no such movie found in the database
    #     print("NO MOVIES FOUND!..")
    # else:

    #     tmdb_movie_object = Movie()
    #     result = tmdb_movie_object.search(movie_name)

    #     # get movie id and movie title
    #     movie_id = result[0].id
    #     movie_title = result[0].title

    #     # making API call
    #     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    #     movie_json = response.json()
    #     imdb_id = movie_json['imdb_id']
    #     poster_path = movie_json['poster_path']
    #     img_path = 'https://image.tmdb.org/t/p/original{}'.format(poster_path)
    #     movie_details['movie_name'] = movie_json['title']
    #     movie_details['image'] = img_path

    #     # getting list of genres form json
    #     genre = list_of_genres(movie_json['genres'])
    #     movie_details['genre'] = genre

    #     # getting votes with comma as thousands separators
    #     vote_count = "{:,}".format(movie_json['vote_count'])
    #     movie_details['vote count'] = vote_count
        
    #     # convert date to readable format (eg. 10-06-2019 to June 10 2019)
    #     release_day,release_month,release_year = date_convert(movie_json['release_date'])
    #     release_date = "{} {},{}".format(release_month,release_day,release_year)
    #     movie_details['Date'] = release_date

    #     # getting the status of the movie (released or not)
    #     release_status = movie_json['status']
    #     movie_details['Released status'] = release_status

    #     # convert minutes to hours minutes (eg. 148 minutes to 2 hours 28 mins)
    #     runtime = movie_runtime(movie_json['runtime'])
    #     movie_details['runtime'] = runtime

    # print()    
    # print("---Movie Details---")
    # for key,value in movie_details.items():
    #     print("{} : {}".format(key,value))

    # print()
    # print()

    # print("----Top Recommendation----")
    # for movie_title in recommended_movies:
    #     movie_list = tmdb_movie_object.search(movie_title)
    #     movie_id = movie_list[0].id
    #     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    #     movie_json = response.json()
    #     img_path = 'https://image.tmdb.org/t/p/original{}'.format(movie_json['poster_path'])
    #     print("{} : {}".format(movie_title,img_path))

    # print()
