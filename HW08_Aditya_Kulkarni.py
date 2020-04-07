"""
Functions for file-reading and date arithmetic File Analyzer module
"""

import os
from typing import Iterator, Tuple, IO, Dict, List
from datetime import datetime, timedelta
from prettytable import PrettyTable


def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ Code segment demonstrating expected return values. """
    three_days_after_02272000: datetime = datetime(2000, 2, 27) + timedelta(days=3)
    three_days_after_02272017: datetime = datetime(2017, 2, 27) + timedelta(days=3)
    days_passed_01012017_10312017: int = (datetime(2017, 9, 30) - datetime(2017, 2, 1)).days

    return three_days_after_02272000, three_days_after_02272017, days_passed_01012017_10312017


def file_reader(path: str, fields: int, sep: str = ',', header: bool = False) -> Iterator[Tuple[str]]:
    """ generator function to read field-separated text files and yield a tuple with all of the values \
    from a single line in the file """
    try:
        file: IO = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"Unable to open the file")
    else:
        with file:
            line_num = 0
            for line in file:
                line_num += 1
                line = line.rstrip().split(sep)
                if len(line) != fields:
                    raise ValueError(f"Line {line_num} has {len(line)} fields expected {fields}")
                if header:
                    header = False
                else:
                    yield line


class FileAnalyzer:
    """ Class which checks for python files and analyzes the content."""

    def __init__(self, directory: str) -> None:
        """ Constructor to initialize data structure and call class methods analyze_files and pretty_print."""
        self.directory: str = directory  # NOT mandatory!
        self.files_summary: Dict[str, Dict[str, int]] = dict()
        self.analyze_files()

    def analyze_files(self) -> None:
        """ Your docstring should go here for the description of the method."""
        py_files: List = [f for f in os.listdir(self.directory) if f.endswith(".py")]
        for pyf in py_files:
            try:
                file: IO = open(os.path.join(self.directory, pyf), 'r')
                classes: int = 0
                functions: int = 0
                lines: int = 0
                char: int = 0
            except FileNotFoundError:
                raise FileNotFoundError(f"Unable to open the file")
            else:
                with file:
                    for line in file:
                        lines += 1
                        char += len(line)
                        if line.strip().startswith("class"):
                            classes += 1
                        elif line.strip().startswith("def"):
                            functions += 1
                    self.files_summary[pyf] = self.files_summary.get(pyf, {'class': classes,
                                                                           'function': functions,
                                                                           'line': lines,
                                                                           'char': char})

    def pretty_print(self) -> None:
        """ Display the data stored in a tabular format."""
        pt: PrettyTable = PrettyTable(field_names=["File Name", "Classes", "Functions", "Lines", "Characters"])
        for fname, v in self.files_summary.items():
            classes, functions, lines, char = v.values()
            pt.add_row([fname, classes, functions, lines, char])
        print(pt)
