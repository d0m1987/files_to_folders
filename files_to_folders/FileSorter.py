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

from files_to_folders.logger import logger
from functools import partial

def DRYRUN(a, b): return print(f'Copy\n\t{a}\nto\n\t{b}')
class FileAction(Enum):
    # Using partial because otherwise enum is not working properly. 
    # See https://stackoverflow.com/questions/40338652/how-to-define-enum-values-that-are-functions
    COPY = partial(shutil.copy)
    MOVE = partial(shutil.move)
    DRYRUN = partial(DRYRUN)


class FileSorter:
    def __init__(self, regexes: list[Union[str, re.Pattern]], output_folder: Union[Path, str] = Path.cwd(), file_action: FileAction = FileAction.MOVE):
        self._regexes: list[re.Pattern] = self.__compile_regexes(regexes)
        self._output_folder: Path = self.__check_and_convert_output_folder(
            output_folder)
        self._file_action: FileAction = file_action

    def __compile_regexes(self, regexes: list[Union[str, re.Pattern]]) -> list[re.Pattern]:
        compiled_regexes = []
        for regex in regexes:
            if isinstance(regex, str):
                regex = re.compile(regex)
            if not isinstance(regex, re.Pattern):
                msg = f"{regex=} is of type {type(regex)} but needs to be of type string or re.Pattern."
                logger.error(msg)
                raise TypeError(msg)

            compiled_regexes.append(regex)

        return compiled_regexes

    def __check_and_convert_output_folder(self, output_folder: Union[Path, str]) -> Path:
        if not (isinstance(output_folder, Path) or isinstance(output_folder, str)):
            msg = f"Expected pathlib.Path or string but got {output_folder=} that is of type {type(output_folder)}."
            logger.error(msg)
            raise TypeError(msg)
        if isinstance(output_folder, str):
            output_folder = Path(output_folder)
        if output_folder.is_dir():
            return output_folder
        else:
            msg = f"Expected folder path but got {output_folder=} that is not a folder when checked with pathlib.Path.is_dir()."
            logger.error(msg)
            raise TypeError(msg)

    def sort(self, files: Union[list[str, Path], Path, str]) -> list[Path]:
        if not isinstance(files, Iterable):
            files = [files]

        result_file_paths = []
        for file in files:
            logger.debug(f"Sorting file {file}")
            if isinstance(file, str):
                file = Path(file)
            if not file.is_file():
                msg = f"Expected file but {file=} is not recognized as file by pathlib.Path."
                logger.error(msg)
                raise TypeError(msg)

            regex_hits = []
            for regex in self._regexes:
                logger.debug(f"Using regex {regex.pattern}")
                regex_result = regex.search(str(file.as_posix()))
                if regex_result:
                    regex_groups = regex_result.groups()
                    regex_hits.extend(regex_groups)
                    logger.debug(f"Found the following regex groups {regex_groups}")
                else:
                    regex_hits.append("_Undefined_")
                    logger.debug(f"Found no matching regex and thus adding _Undefined_")
                    continue

            result_file_paths.append(
                self.__copy_file_to_folder(file, regex_hits))

        return result_file_paths

    def __copy_file_to_folder(self, file: Path, regex_hits: list[str]) -> Path:
        folder_to_copy_to = self._output_folder / Path('/'.join(regex_hits))
        
        # Prevent unnecessary folder creation if it is only a dryrun
        if self._file_action is not FileAction.DRYRUN:
            folder_to_copy_to.mkdir(parents=True, exist_ok=True)
        
        output_file_path = folder_to_copy_to / file.name
        self._file_action.value(file, output_file_path)
        logger.debug(f'Using {self._file_action.name} with the first parameter {file} and the second parameter {output_file_path}.')

        return output_file_path
