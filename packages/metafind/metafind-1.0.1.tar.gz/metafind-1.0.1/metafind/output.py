from metafind.models import Document
from rich.table import Table
from rich.console import Group


def fetch_output(documents: list[Document]):
    tables = create_document_tables(documents)
    return Group(*tables)


def create_document_tables(documents: list[Document]) -> list[Table]:
    tables: list[Table] = []
    for doc in documents:
        table = Table(title=doc.name)
        table.add_column("Tag", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        # Add rows for each key-value pair (except SourceFile itself if desired)
        for data in doc.metadata:
            table.add_row(data.tag, str(data.value))
        tables.append(table)
    return tables
