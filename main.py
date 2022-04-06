from reducers.reducer import *
from loaders.mongo_db_loader import *

if __name__ == "__main__":
    reset_collection(get_collection('motionPictures'))
    insert_movies('/Users/justinli/Documents/code/magic_eight_ball_data/reducers/output/basic_info_with_ratings_30000_movie.tsv')
    insert_tv_shows('/Users/justinli/Documents/code/magic_eight_ball_data/reducers/output/basic_info_with_ratings_30000_tvSeries.tsv')