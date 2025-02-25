from metafind.client import Client
from metafind.models import Document

from pathlib import Path
from exiftool.exceptions import ExifToolOutputEmptyError

import exiftool


_TAGS_TO_SKIP = {"SourceFile", "ExifTool:ExifToolVersion", "ExifTool:Warning"}


class ExifToolClient(Client):
    """
    ExifToolClient is a wrapper built around the `exiftool.ExifToolHelper` class.
    """

    def __init__(self, path: str):
        self.client = exiftool.ExifToolHelper()
        self.path = path

    def get_metadata(self) -> list[Document]:
        result = self.client.get_metadata(self.path)
        return [_make_new_doc(data) for data in result]

    def scrub_metadata(self) -> (list[str], list[str]):
        all_tags = self.get_unique_tags()
        try:
            self.client.execute_json("-all= ", self.path)
        except ExifToolOutputEmptyError:
            immutable_tags = self.get_unique_tags()
            mutable_tags = all_tags - immutable_tags
            return sorted(mutable_tags), sorted(immutable_tags)

    def get_unique_tags(self) -> set[str]:
        result = self.client.get_metadata(self.path)
        unique_tags = {
            tag.split(":", 1)[1]
            for data in result
            for tag in data
            if tag not in _TAGS_TO_SKIP
        }
        return unique_tags


def _make_new_doc(data: dict) -> Document:
    name = Path(data["SourceFile"]).name
    filetype = data["File:FileType"]
    return Document(name, data, filetype, _TAGS_TO_SKIP)
