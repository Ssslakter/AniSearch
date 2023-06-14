import os
import pandas as pd
import wandb


GROUP_NAME = "dataset"
ENTITY = "pujak-ai"
PROJECT = "AniSearch"


def merge_data(csv_path: str, jl_path: str):
    """Merges csv and jl files into pandas df. Duplicates will be overwritten by data in jl"""
    df = pd.read_csv(csv_path).drop_duplicates(subset=["uid"])
    new_df: pd.DataFrame = pd.read_json(jl_path, lines=True).drop_duplicates(
        subset=["uid"]
    )
    df.drop(df[df["uid"].isin(new_df["uid"])].index)
    return pd.concat([df, new_df])


def __create_artifacts(data_dir: str):
    artifact = wandb.Artifact(
        name="anime-data",
        type="dataset",
        description="Anime dataset before 2020 from kaggle",
    )
    if os.path.isdir(data_dir):
        artifact.add_dir(data_dir)
    else:
        artifact.add_file(data_dir)
    return artifact


def upload_artifacts(data_dir: str):
    """Upload artifacts to wandb with default configs"""
    run = wandb.init(group=GROUP_NAME, project=PROJECT, entity=ENTITY)
    artifacts = __create_artifacts(data_dir)
    run.log_artifact(artifacts)  # type:ignore
