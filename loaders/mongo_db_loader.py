import os
import pandas as pd
import requests
import pycountry
from dotenv import load_dotenv
from pymongo import MongoClient
from tqdm import tqdm
from termcolor import colored


load_dotenv()
client = MongoClient(os.getenv('MONGO_DB_CONNECTION_STRING'))
API_KEY = os.getenv('API_KEY')


def get_collection(collection_name):
    db = client['magicEightBallDB']
    return db[collection_name]


def reset_collection(collection):
    print(f"Resetting {collection}")
    collection.delete_many({})


def supplement_model(model):
    URL = f'http://www.omdbapi.com/?&apikey={API_KEY}'
    PARAMS = { 'i': model['tconst'] }
    res = requests.get(URL, PARAMS)
    data = res.json()
    model['genres'] = data['Genre']
    model['director'] = data['Director']
    model['actors'] = data['Actors']
    model['plot'] = data['Plot']
    model['country'] = data['Country'].split(',')[0]
    model['awards'] = data['Awards']
    model['poster'] = data['Poster']
    model['languages'] = [language.strip() for language in data['Language'].split(",")]
    for rating in data['Ratings']:
        if rating['Source'] == 'Rotten Tomatoes':
            model['rottenTomatoes'] = rating['Value']
        if rating['Source'] == 'Metacritic':
            model['metacritic'] = rating['Value']

def insert_movies(filename):
    print(f"Inserting movies from {filename}...")
    movies = get_collection('movie')
    file = pd.read_csv(filename, low_memory=False)
    columns = list(file.columns)
    columns.remove('originalTitle')
    for index, row in tqdm(file.iterrows(), total=file.shape[0]):
        movie = {}
        for column in columns:
            field = convert_column_to_field(column)
            movie[field] = row[column]
        supplement_model(movie)
        movie['genres'] = [genre.strip() for genre in movie['genres'].split(",")]
        del movie['type']
        movies.insert_one(movie)
    print(colored("done", 'green'))


def insert_tv_shows(filename):
    print(f"Inserting TV shows from {filename}... ")
    tv_shows = get_collection('tvShow')
    file = pd.read_csv(filename, low_memory=False)
    columns = list(file.columns)
    columns.remove('originalTitle')
    for index, row in tqdm(file.iterrows(), total=file.shape[0]):
        tv_show = {}
        for column in columns:
            field = convert_column_to_field(column)
            tv_show[field] = row[column]
        supplement_model(tv_show)
        tv_show['genres'] = [genre.strip() for genre in tv_show['genres'].split(",")]
        del tv_show['type']
        tv_shows.insert_one(tv_show)
    print(colored("done", 'green'))


def convert_column_to_field(column):
    field = column
    if column == 'averageRating':
        field = 'rating'
    elif column == 'numVotes':
        field = 'votes'
    elif column == 'titleType':
        field = 'type'
    elif column == 'primaryTitle':
        field = 'title'
    elif column == 'startYear':
        field = 'year'
    elif column == 'runtimeMinutes':
        field = 'runtime'
    return field
