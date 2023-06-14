## Main dataset
For anime data before 2021 the [kaggle](https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews) dataset was used
1. To get data for the last 3 years (2021 - summer 2023) use [this repo](https://github.com/marlesson/scrapy_myanimelist)

You may need to change main script according to the current MAL website layout for the scraping to work properly

2. After getting bunch of `.jl` files put them into data directory and run 
```sh
py ./src/cli/make_dataset.py merge-datasets ./data/external/animes.csv ./data/animes_2023_winter.jl ./data/animes.csv
```

3. To upload artifacts to wandb run (this will upload the whole data folder)
```sh
py ./src/cli/upload_data.py to-wandb ./data
```
