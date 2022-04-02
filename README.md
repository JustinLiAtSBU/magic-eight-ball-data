# Magic Eight Ball Data
This repository is used to parse and reduce `.tsv` data from IMDB's website: https://datasets.imdbws.com
## File structure
In the `reducers` folder, create a `data/` and `output/` folder.
### Raw Data
Raw data, such as csv files used to populate databases, should be saved under the `data/` folder. The accepted file extension for data is `.tsv`, although this can be changed with a few simple modifications to in `reducer.py`.
### Output
Output of functions in `reducer.py` is stored under `output/`
