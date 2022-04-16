from reducers.reducer import *
from loaders.mongo_db_loader import *

if __name__ == "__main__":
    # Data parsing
    reduce_basic_info('movie', startYear=1970, runtimeMinutes=80)
    combine_ratings_basic_info('movie', 10000)
    reduce_basic_info('tvSeries', startYear=1970)
    combine_ratings_basic_info('tvSeries', 10000)

    # Database populating
    reset_collection(get_collection('movie'))
    insert_movies('/Users/justinli/Documents/code/magic_eight_ball_data/reducers/output/basic_info_with_ratings_10000_movie.tsv')
    reset_collection(get_collection('tvShow'))
    insert_tv_shows('/Users/justinli/Documents/code/magic_eight_ball_data/reducers/output/basic_info_with_ratings_10000_tvSeries.tsv')