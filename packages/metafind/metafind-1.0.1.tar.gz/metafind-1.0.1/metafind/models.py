from dataclasses import dataclass, field


@dataclass(order=True)
class Metadata:
    """
    Metadata is a class used to encapsulate discovered metadata.

    :param parent: Identifies the parent file or resource from which the metadata was discovered.
    :type parent: str
    :param tag: The metadata tag (used for sorting).
    :type tag: str
    :param value: The value associated with the given tag.
    :type value: str
    """

    parent: str = field(compare=False)
    tag: str = field(compare=True)
    value: str = field(compare=False)


class Document:
    """
    Document is a class used to encapsulate file metadata.
    """

    def __init__(self, name: str, data: dict, filetype: str, tags_to_skip: list):
        self.name = name
        self.filetype = filetype
        self.metadata: list[Metadata] = self._add_metadata(data, tags_to_skip)

    def _add_metadata(self, data: dict, tags_to_skip: list) -> list[Metadata]:
        """
        add_metadata adds metadata to the Document.
        """
        metadata: list[Metadata] = []
        for tag, value in data.items():
            if tag not in tags_to_skip:
                clean_tag = tag.split(":")[1]
                metadata.append(Metadata(parent=self.name, tag=clean_tag, value=value))
        return metadata

    def __repr__(self) -> str:
        return f"{self.name}, {self.filetype}, {self.metadata}"
