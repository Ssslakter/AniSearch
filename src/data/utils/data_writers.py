from abc import ABC, abstractmethod
import json
import os
from pathlib import Path


class DataWriterBase(ABC):
    """Base class to write data

    Usage:
    * before writing data, call prepare()
    * for single data object, call write()
    * after writing data, call finalize()
    """
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def prepare(self) -> None:
        """Method to prepare writer to write data
        """
        raise NotImplementedError

    @abstractmethod
    def write(self, obj: object) -> None:
        """Method to write data

        Args:
            obj (object): data object to write
        """
        raise NotImplementedError

    @abstractmethod
    def finalize(self) -> None:
        """Method to finalize writing data e.g. close file
        """
        raise NotImplementedError


class JsonWriter(DataWriterBase):
    """Class to write data to json file

    Inherits from DataWriterBase
    """

    def __init__(self, file_path: str) -> None:
        """Constructor for JsonWriter

        Args:
            file_path (str): path to write json file,
            * if `file_path` is a directory, `result.json` will be created
            * if `file_path` is a directory which does not exist, it will be created
            * if `file_path` is a file, it will be overwritten or created
        """
        if os.path.isdir(file_path) and not os.path.exists(file_path):
            os.makedirs(file_path)
        if os.path.isdir(file_path):
            self.file_path = Path(file_path)/'result.json'
        self.file_path = Path(file_path)

    def prepare(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("[\n")

    def write(self, obj) -> None:
        with open(self.file_path, "a", encoding="utf-8") as file:
            json.dump(obj, file, ensure_ascii=False, indent=4)
            file.write(",\n")

    def finalize(self) -> None:
        offset = 3
        with open(self.file_path, "r+b") as file:
            file.seek(-offset, os.SEEK_END)
            file.truncate()
            file.write(b"\n]")
