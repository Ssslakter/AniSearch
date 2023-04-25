import json


class DataWriter:
    def __init__(self) -> None:
        pass

    def prepare(self) -> None:
        pass

    def write(self, object) -> None:
        pass

    def finalize(self) -> None:
        pass


class JsonWriter(DataWriter):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def prepare(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("[\n")

    def write(self, object) -> None:
        with open(self.file_path, "a", encoding="utf-8") as f:
            json.dump(object, f, ensure_ascii=False, indent=4)
            f.write(",\n")

    def finalize(self) -> None:
        json_str = open(self.file_path, "r", encoding="utf-8").read()
        with open(self.file_path, "w", encoding="utf-8") as f:
            json_str = json_str[:-2]
            f.write(json_str+"\n]")


# TODO implement db writer
class DbWriter(DataWriter):
    def __init__(self, db) -> None:
        pass

    def prepare(self) -> None:
        pass

    def write(self, object) -> None:
        pass

    def finalize(self) -> None:
        pass
