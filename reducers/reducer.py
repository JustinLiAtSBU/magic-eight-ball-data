import pandas as pd


# TODO: Return filename
def reduce_ratings_by_votes(min):
    output = open(f'reducers/output/ratings_min_votes_{min}.tsv', 'w+')
    ratings = pd.read_csv(
        'reducers/data/ratings.tsv',
        low_memory=False,
        sep='\t'
    )
    ratings = ratings[ratings['numVotes'] >= min]
    ratings.to_csv(output, index=False)


def reduce_basic_info(titleType, **kwargs):
    output = open(f'reducers/output/basic_info_{titleType}.tsv', 'w+')
    basic_info = pd.read_csv(
        'reducers/data/imdb_basic_info.tsv',
        low_memory=False,
        sep='\t'
    )
    basic_info = basic_info.drop(columns=['isAdult', 'endYear'])
    basic_info = basic_info[basic_info['startYear'] != r"\N"]
    basic_info = basic_info[basic_info['runtimeMinutes'] != r"\N"]
    basic_info = basic_info[basic_info['titleType'] == titleType]
    basic_info = basic_info[basic_info['startYear'].astype(int) >= kwargs.get('startYear', 1940)]
    basic_info = basic_info[basic_info['runtimeMinutes'].astype(int) >= kwargs.get('runtimeMinutes', 0)]
    basic_info.to_csv(output, index=False)


def combine_ratings_basic_info(title_type, min_ratings):
    output = open(f'reducers/output/basic_info_with_ratings_{min_ratings}_{title_type}.tsv', 'w+')
    ratings = pd.read_csv(
        f'reducers/output/ratings_min_votes_{min_ratings}.tsv',
        low_memory=False,
    )
    basic_info = pd.read_csv(
        f'reducers/output/basic_info_{title_type}.tsv',
        low_memory=False,
    )
    merged = pd.merge(ratings, basic_info, on="tconst")
    print(merged.head())
    merged.to_csv(output, index=False)


def check_rows(filename):
    basic_info = pd.read_csv(
        f'reducers/data/{filename}',
        low_memory=False,
        sep='\t'
    )
    print(len(basic_info))
