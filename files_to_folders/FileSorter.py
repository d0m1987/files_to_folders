"""
Class FileSorter is used to handle the file sorting.
The regular expressions and the output path that shall be used
are given during object initialization and are not meant to be changed
during runtime.
Sorting can then be done an arbitrary time using the sort function. 
"""

import re
from pathlib import Path
from typing import Union

class FileSorter:
    def __init__(self, regexes:list[Union[str, re.Pattern]], output_folder:Union[Path, str]=Path.cwd()):
        self._regexes:list[re.Pattern] = self.__compile_regexes(regexes)
        self._output_folder:Path = self.__check_and_convert_output_folder(output_folder)

    def __compile_regexes(self, regexes:list[Union[str, re.Pattern]]) -> list[re.Pattern]:
        compiled_regexes = []
        for regex in regexes:
            if isinstance(regex, str):
                compiled_regexes.append(re.compile(regex))
            elif isinstance(regex, re.Pattern):
                compiled_regexes.append(regex)
            else:
                raise TypeError(f"{regex=} is of type {type(regex)} but needs to be of type string or re.Pattern.")

        return compiled_regexes

    def __check_and_convert_output_folder(self, output_folder:Union[Path, str]) -> Path:
        if not (isinstance(output_folder, Path) or isinstance(output_folder, str)):
            raise TypeError(f"Expected pathlib.Path or string but got {output_folder=} that is of type {type(output_folder)}.")
        if isinstance(output_folder, str):
            output_folder = Path(output_folder)
        if output_folder.is_dir():
            return output_folder
        else:
            raise TypeError(f"Expected folder path but got {output_folder=} that is not a folder when checked with pathlib.Path.is_dir().")

    def sort(files:Union[list[str, Path], Path, str]) -> list[Path]:
        pass

