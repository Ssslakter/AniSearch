from ast import literal_eval
import re
from pathlib import Path
from jinja2 import Template
import pandas as pd

from src.anisearch.data_models import AnimeData


DOCUMENT_TEMPLATE = "../templates/anime_template.j2"
# TODO extract names from template authomatically
TEMPLATE_VARS = [
    "title",
    "genres",
    "aired",
    "episodes",
    "popularity",
    "score",
    "synopsis",
]


class DocumentBuilder:
    """Class for creating documents from jinja templates and pandas data"""

    def __init__(self) -> None:
        with open(Path(__file__) / DOCUMENT_TEMPLATE, encoding="utf-8") as file:
            template_str = file.read()

        self.template = Template(template_str)

    def render_document(self, data: pd.Series | AnimeData) -> str:
        """Fills template with content of series

        Args:
            `data` (pd.Series | AnimeData): series with some fields or AnimeData model

        Raises:
            ValueError: if any of the keys in a `row` wasn't present in the template

        Returns:
            str: rendered document
        """
        if isinstance(data, AnimeData):
            data_dict = data.dict()
        else:
            data_dict = data.to_dict()
        keys = data_dict.keys()
        for key in TEMPLATE_VARS:
            if key not in keys:
                raise ValueError(f"Missing key in the row: '{key}'")

        return self.template.render(**data_dict)

    def build_documents(self, df: pd.DataFrame) -> pd.Series:
        """Applies `render_document` for every row in df

        Args:
            df (pd.DataFrame): table with documents

        Returns:
            pd.Series: list of rendered documents
        """
        rendered = df.apply(self.render_document, axis=1)
        return rendered


def fix_lists(
    df: pd.DataFrame | pd.Series, cols: list[str] | None = None
) -> pd.DataFrame | pd.Series:
    """Replaces list-like columns with columns of actual lists\n
    if df is a series then returns fixed series, otherwise applies fix to dataframe

    Args:
        df (pd.DataFrame): input dataframe
        cols (list[str], optional): Columns to fix. If None then uses regex to find list-like columns

    Returns:
            pd.DataFrame | pd.Series: dataframe or series with fixed lists
    """
    if isinstance(df, pd.Series):
        return df.apply(literal_eval)
    if cols is None:
        regex = r"\[('.*', )*'.*'?\]"
        cols = [
            key
            for key, value in df.iloc[0].to_dict().items()
            if re.fullmatch(regex, str(value)) is not None
        ]

    for col in cols:
        df[col] = df[col].apply(literal_eval)
    return df


def remove_text(df: pd.Series, substring: str) -> pd.Series:
    """Remove substring from every element in series"""
    return df.apply(lambda x: str(x).replace(substring, "").strip())
