from reducers.reducer import *


if __name__ == "__main__":
    reduce_ratings_by_votes(10000)
    reduce_basic_info('movie', startYear=1960, runtimeMinutes=60)
    reduce_basic_info('tvSeries', startYear=1960)
    combine_ratings_basic_info('movie', 10000)
