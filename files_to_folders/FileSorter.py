"""
Class FileSorter is used to handle the file sorting.
The regular expressions and the output path that shall be used
are given during object initialization and are not meant to be changed
during runtime.
Sorting can then be done an arbitrary time using the sort function. 
"""

import re
import shutil
from enum import Enum
from pathlib import Path
from typing import Iterable, Union


class FileAction(Enum):
    COPY = shutil.copy
    MOVE = shutil.move
    def DRYRUN(a, b): return print(f'Copy\n\t{a}\nto\n\t{b}')


class FileSorter:
    def __init__(self, regexes: list[Union[str, re.Pattern]], output_folder: Union[Path, str] = Path.cwd(), file_action: FileAction = FileAction.MOVE):
        self._regexes: list[re.Pattern] = self.__compile_regexes(regexes)
        self._output_folder: Path = self.__check_and_convert_output_folder(
            output_folder)
        self._file_action = file_action

    def __compile_regexes(self, regexes: list[Union[str, re.Pattern]]) -> list[re.Pattern]:
        compiled_regexes = []
        for regex in regexes:
            if isinstance(regex, str):
                regex = re.compile(regex)
            if not isinstance(regex, re.Pattern):
                raise TypeError(
                    f"{regex=} is of type {type(regex)} but needs to be of type string or re.Pattern.")

            compiled_regexes.append(regex)

        return compiled_regexes

    def __check_and_convert_output_folder(self, output_folder: Union[Path, str]) -> Path:
        if not (isinstance(output_folder, Path) or isinstance(output_folder, str)):
            raise TypeError(
                f"Expected pathlib.Path or string but got {output_folder=} that is of type {type(output_folder)}.")
        if isinstance(output_folder, str):
            output_folder = Path(output_folder)
        if output_folder.is_dir():
            return output_folder
        else:
            raise TypeError(
                f"Expected folder path but got {output_folder=} that is not a folder when checked with pathlib.Path.is_dir().")

    def sort(self, files: Union[list[str, Path], Path, str]) -> list[Path]:
        if not isinstance(files, Iterable):
            files = [files]

        result_file_paths = []
        for file in files:
            if isinstance(file, str):
                file = Path(file)
            if not file.is_file():
                raise TypeError(
                    f"Expected file but {file=} is not recognized as file by pathlib.Path.")

            regex_hits = []
            for regex in self._regexes:
                regex_result = regex.search(str(file.as_posix()))
                if regex_result:
                    regex_hits.extend(regex_result.groups())
                else:
                    regex_hits.append("_Undefined_")
                    continue

            result_file_paths.append(
                self.__copy_file_to_folder(file, regex_hits))

        return result_file_paths

    def __copy_file_to_folder(self, file: Path, regex_hits: list[str]) -> Path:
        folder_to_copy_to = self._output_folder / Path('/'.join(regex_hits))
        if self._file_action is not FileAction.DRYRUN:
            folder_to_copy_to.mkdir(parents=True, exist_ok=True)
        output_file_path = folder_to_copy_to / file.name
        self._file_action(file, output_file_path)

        return output_file_path
