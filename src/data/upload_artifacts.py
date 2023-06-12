import wandb

GROUP_NAME = "dataset"
ENTITY = "pujak-ai"
PROJECT = "AniSearch"
DATA_DIR = "data/external"
# original dataset https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews

run = wandb.init(group=GROUP_NAME, project=PROJECT, entity=ENTITY)
artifact = wandb.Artifact(
    name="anime-data",
    type="dataset",
    description="Anime dataset before 2020 from kaggle",
)
artifact.add_dir(DATA_DIR)
run.log_artifact(artifact)
