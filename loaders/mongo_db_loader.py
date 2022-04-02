import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from tqdm import tqdm
from termcolor import colored


load_dotenv()
client = MongoClient(os.getenv('MONGO_DB_CONNECTION_STRING'))


def get_collection(collection_name):
    db = client['magicEightBallDB']
    return db[collection_name]


def insert_movies(filename):
    print(f"Resetting movies from movies collection... ", end='')
    reset_collection(get_collection('movies'))
    print(colored('done', 'green'))

    print(f"Inserting movies from {filename}...")
    movies = get_collection('movies')
    file = pd.read_csv(filename, low_memory=False)
    columns = list(file.columns)
    for index, row in tqdm(file.iterrows(), total=file.shape[0]):
        movie = {}
        for column in columns:
            if column == 'genres':
                movie[column] = row[column].split(',')
            else:
                movie[column] = row[column]
        movies.insert_one(movie)
    print(colored("done", 'green'))


def insert_tv_shows(filename):
    print(f"Resetting TV shows from tvShows collection... ", end='')
    reset_collection(get_collection('tvShows'))
    print(colored('done', 'green'))

    print(f"Inserting TV shows from {filename}... ")
    movies = get_collection('tvShows')
    file = pd.read_csv(filename, low_memory=False)
    columns = list(file.columns)
    for index, row in tqdm(file.iterrows(), total=file.shape[0]):
        movie = {}
        for column in columns:
            if column == 'genres':
                movie[column] = row[column].split(',')
            else:
                movie[column] = row[column]
        movies.insert_one(movie)
    print(colored("done", 'green'))


def reset_collection(collection):
    collection.delete_many({})


def rename_db(original_name, new_name):
    client.admin.command('copydb', fromdb=original_name, todb=new_name)


if __name__ == "__main__":
    insert_movies('../reducers/output/basic_info_with_ratings_30000_movie.tsv')
    # insert_tv_shows('../reducers/output/basic_info_with_ratings_30000_tvSeries.tsv')
