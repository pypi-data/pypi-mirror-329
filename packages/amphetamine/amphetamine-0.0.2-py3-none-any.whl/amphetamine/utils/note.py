"""
kosmo.utils.note

Interfaces for notetaking
"""
# Standard library imports: Package-level
import logging

# Standard library imports: Module-level
from datetime import datetime as dt
from pathlib import Path
from typing import Optional, Protocol, TypeVar, Union, runtime_checkable

# Set up logger
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


# Custom typing
T: TypeVar = TypeVar("T")


@runtime_checkable
class Notable(Protocol):
    """
    kosmo.utils.note.Notable

    Protocol to be implemented by the `Note` class.
    """
    date: str
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    data_dir: Optional[Union[Path, str]]

    @classmethod
    def create(cls, title, summary, content) -> "Note[T]":
        ...

    @classmethod
    def load(cls, fp: Union[Path, str]) -> "Note[T]":
        ...

    def save(self) -> None:
        ...


class Note:
    """
    kosmo.utils.note.Note

    Main interface for notetaking.
    """
    date: str
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[T] = None
    data_dir: Optional[Union[Path, str]] = Path("~/.kosmo/notes").expanduser()


    @classmethod
    def create(cls, title, summary, content, data_dir=data_dir) -> "Note[T]":
        """
        Create a new note.
        """
        note = cls()
        note.date = dt.now().strftime("%A %B %d, %Y %I:%M:%S %p")
        note.title = title
        note.summary = summary
        note.content = (f"""# {title}
###### {note.date}

[[{summary}]]

---

{content}""")
        note.data_dir = data_dir

        return note


    @classmethod
    def load(cls, fp: Union[Path, str]) -> "Note[T]":
        note = cls()
        with open(fp, "r") as f:
            note.content = f.read()
            for line in note.content.splitlines():
                if line.startswith("#"):
                    note.title = line[1:].strip()
                elif line.startswith("######"):
                    note.date = line[5:].strip()
                elif line.startswith("[[") and line.endswith("]]"):
                    note.summary = line[2:-2]

        return note


    def save(self) -> None:
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.data_dir / f"{self.title}.txt", "w") as f:
            f.write(self.content)
            logger.info(f"Saved note {self.title}.txt to {self.data_dir}.")


# def main():
#     """
#     kosmo.utils.note.main
#
#     Entry point for the `kosmo.utils.note` module.
#     """
#     note = Note.create(
#         title="Untitled Note",
#         summary="Summary...",
#         content="Content..."
#     )
#
#     return print(note.title)
#
#
# if __name__ == "__main__":
#     main()
