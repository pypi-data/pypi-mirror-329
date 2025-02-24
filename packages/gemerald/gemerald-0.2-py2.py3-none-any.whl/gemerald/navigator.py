import os

from typing import Optional, override
from abc import ABC
from pathlib import Path
from os import path

from gemerald.strategies import find_strategy
from gemerald.format_config import Config


class NavigatorFile:

    def __init__(self, filepath: Path, absolute_path: Path):
        self.p = filepath
        self.abs = absolute_path

    def __repr__(self):
        return self.filename

    @property
    def filename(self) -> str:
        return path.basename(self.p)

    @property
    def relative_folder_path(self) -> str:
        """
        Returns str path to directory of the file from base directore in
        which mavigator was created
        """
        return path.dirname(self.p)

    @property
    def relative_path(self) -> str:
        return self.p.as_posix()

    @property
    def absolute_path(self) -> str:
        return path.abspath(self.abs)

    @property
    def contents(self) -> list[str]:
        with open(self.absolute_path, encoding="utf-8") as f:
            return f.readlines()


class DirectoryNavigator(ABC):
    """
    Searches for files in a given directory. Iterable.
    """

    def __init__(self, directory_path: Optional[Path]):
        self.files: list[NavigatorFile] = []
        if directory_path is not None:
            self.add_folder(directory_path)

    def __iter__(self):
        return self.files.__iter__()

    def clone(self):
        new_obj = self.__class__(directory_path=None)
        new_obj.files = self.files.copy()

    def get_file_by_relative(
        self, rp: str, extension: Optional[str] = None
    ) -> Optional[NavigatorFile]:
        searchpath = Path(rp).with_suffix(extension).as_posix() if extension else rp
        for file in self:
            if file.relative_path == searchpath:
                return file
        return None

    def add_folder(self, directory_path: Path, extension: Optional[str] = None):
        """Same as given in __init__ but adds to already existing files"""
        searchterm = "*" if extension is None else f"*.{extension}"
        for file in Path(directory_path).rglob(searchterm):
            if os.path.isfile(file):
                f = file.relative_to(directory_path)
                self.files.append(NavigatorFile(filepath=f, absolute_path=file))


class MarkdownNavigator(DirectoryNavigator):

    @override
    def __init__(self, directory_path: Path):
        super().__init__(None)
        self.add_folder(directory_path, "md")


class TemplateNavigator(DirectoryNavigator):

    class StrategyNotFoundException(Exception):
        pass

    class TemplateNotFoundException(Exception):
        pass

    class NoConfigException(Exception):
        pass

    def __init__(self, directory_path: Path):
        super().__init__(directory_path)
        self.markdown_files = {}
        self.name = os.path.basename(directory_path)
        fs = find_strategy(self.name)

        if fs is None:
            raise self.StrategyNotFoundException(
                f"There is no formatting strategy that could handle format: {self.name}"
            )
        self.formatting_strategy = fs()

        config_file = self.get_file_by_relative("config.yaml")
        if config_file is None:
            raise self.NoConfigException(
                f"Template path provided for format {self.name} "
                f"does not contain 'config.yaml' file."
            )
        self.config = Config(directory_path / config_file.relative_path)

    def get_template_for(self, f: NavigatorFile) -> NavigatorFile:
        alternative_path = Path(f.relative_folder_path) / "_entries_"
        ext = f".{self.name}"

        template = self.get_file_by_relative(
            f.relative_path, ext
        ) or self.get_file_by_relative(alternative_path.as_posix(), ext)

        if template:
            return template
        raise self.TemplateNotFoundException(
            "\n\n"
            f"Could not find template for path {f.relative_path}. "
            f"Please make sure it has corresponding template named "
            f"just like the file in question but with `.{self.name}` "
            f"file extension or have a common _entries_.{self.name} "
            f"template that would be aplied to all files without "
            f"strictly corresponfing template."
            "\n"
        )
