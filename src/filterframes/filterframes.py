"""Module providing function for converting between DTASelectFilter.tx files and pandas DataFrame objects"""
import os
from enum import Enum
from io import TextIOWrapper, StringIO
from typing import List, Union, Any, TextIO, Generator

import pandas as pd

FILE_TYPES = Union[str, TextIOWrapper, StringIO, TextIO]


def _get_lines(file_input: FILE_TYPES) -> Generator[str, None, None]:
    """
    Retrieve lines from a file or string input.

    This function reads lines from a given input, which can be a file path, a string containing lines,
    a TextIOWrapper, or a StringIO object.

    Args:
        file_input (Union[str, TextIOWrapper, StringIO]): The input source.

    Returns:
        generator: A generator that yields lines from the input source.

    Raises:
        ValueError: If the input type is not supported.
    """
    if isinstance(file_input, str): # File path or string
        if os.path.exists(file_input):
            with open(file=file_input, mode='r', encoding='UTF-8') as file:
                for line in file:
                    yield line.rstrip('\n')
        else:
            for line in file_input.split('\n'):
                yield line.rstrip('\n')
    elif isinstance(file_input, (TextIOWrapper, TextIO)): # TextIOWrapper or StringIO
        file_input.seek(0)
        for line in file_input:
            yield line.rstrip('\n')
    elif isinstance(file_input, StringIO): # StringIO
        file_input.seek(0)
        for line in file_input.readlines():
            yield line.rstrip('\n')
    else:
        try:
            for line in file_input:
                yield line.decode('UTF-8').rstrip('\n')
        except Exception as e:
            raise ValueError(f'Unsupported input type: {type(file_input)}!')


def _convert_to_best_datatype(values: List[Any]):
    """
    Convert a list of values to the most suitable datatype.

    This function tries to convert a list of values to either float, int, or str datatypes, in that order.

    Args:
        values (List[Any]): A list of values to be converted.

    Returns:
        list: A list of converted values.

    Raises:
        ValueError: If unable to convert values to any datatype.
    """

    for datatype in [float, int, str]:
        try:
            converted_values = [datatype(value) for value in values]
            return converted_values
        except (ValueError, TypeError):
            continue
    raise ValueError("Unable to convert values to any datatype")


def _create_file_name(peptide_row: pd.Series) -> str:
    """
    Create a file name from a given peptide row.

    This function constructs a file name string from the FileName, LowScan, HighScan, and Charge
    fields of a given peptide row.

    Args:
        peptide_row (pd.Series): A row from a peptide dataframe.

    Returns:
        str: The constructed file name string.
    """

    return f"{peptide_row['FileName']}.{peptide_row['LowScan']}.{peptide_row['HighScan']}.{peptide_row['Charge']}"


def _reorder_columns(dataframe: pd.DataFrame, column: str, new_position: int) -> pd.DataFrame:
    """
    Reorder columns in a dataframe by moving a specified column to a new position.

    Args:
        dataframe (pd.DataFrame): The input dataframe.
        column (str): The column to be moved.
        new_position (int): The new position for the specified column.

    Returns:
        pd.DataFrame: A dataframe with reordered columns.
    """

    columns = dataframe.columns.tolist()
    columns.insert(new_position, columns.pop(columns.index(column)))
    return dataframe[columns]


def _write_lines(file_output, lines):
    """
    Write a list of lines to a given file output.

    Args:
        file_output (TextIOWrapper or StringIO): The output file object.
        lines (list): A list of lines to be written.
    """

    for line in lines:
        file_output.write(line + '\n')


def from_dta_select_filter(file_input: Union[str, TextIOWrapper, StringIO, TextIO]) -> (
        List[str], pd.DataFrame, pd.DataFrame, List[str]):
    """
    Process the given file and extract relevant information to create peptide and protein dataframes.

    This function reads the input file and processes it line by line to create peptide and protein
    dataframes, as well as lists of header lines and end lines (information lines).

    Args:
        file_input (Union[str, TextIOWrapper, StringIO]): The input file as a string, TextIOWrapper, or StringIO.

    Returns:
        tuple: A tuple containing the following elements:
            - header_lines (List[str]): A list of header lines.
            - peptide_df (pd.DataFrame): A dataframe containing peptide data.
            - protein_df (pd.DataFrame): A dataframe containing protein data.
            - end_lines (List[str]): A list of end lines (information lines).
    """

    lines = _get_lines(file_input)

    class FileState(Enum):
        """
        Enum for specifying the different parts of the DTASelect-filter.txt file
        """
        HEADER = 1
        DATA = 2
        INFO = 3

    file_state = FileState.HEADER

    header_lines, end_lines = [], []
    peptide_data, protein_data = None, None
    current_protein_grp, peptide_line_cnt = 0, 0

    for i, line in enumerate(lines):
        line_elements = line.rstrip().split("\t")

        if line.startswith('Locus'):  # Protein Line Header
            protein_data = {key: [] for key in line_elements}
            protein_data['ProteinGroup'] = []

        if line.startswith('Unique'):  # Peptide Line Header
            peptide_data = {key: [] for key in line_elements}
            peptide_data['ProteinGroup'] = []

            header_lines.append(line)
            file_state = FileState.DATA
            continue

        if len(line_elements) > 1 and line_elements[1] == "Proteins":
            file_state = FileState.INFO

        if file_state == FileState.HEADER:
            header_lines.append(line)

        if file_state == FileState.DATA:
            if line_elements[0] == '' or '*' in line_elements[0] or line_elements[0].isnumeric():

                for key, value in zip(peptide_data, line_elements):
                    peptide_data[key].append(value)
                peptide_data['ProteinGroup'].append(current_protein_grp)

                peptide_line_cnt += 1
            else:
                if peptide_line_cnt != 0:
                    current_protein_grp += 1
                    peptide_line_cnt = 0

                for key, value in zip(protein_data, line_elements):
                    protein_data[key].append(value)
                protein_data['ProteinGroup'].append(current_protein_grp)

        if file_state == FileState.INFO:
            end_lines.append(line)

    for k in peptide_data:
        peptide_data[k] = _convert_to_best_datatype(peptide_data[k])

    for k in protein_data:
        protein_data[k] = _convert_to_best_datatype(protein_data[k])

    peptide_df = pd.DataFrame(peptide_data)
    protein_df = pd.DataFrame(protein_data)

    file_name_components = [fn.split('.') for fn in peptide_df['FileName']]
    peptide_df.drop(['FileName'], axis=1, inplace=True)

    peptide_df['FileName'] = _convert_to_best_datatype([comp[0] for comp in file_name_components])
    peptide_df['FileName'] = peptide_df['FileName'].astype('category')

    peptide_df['LowScan'] = _convert_to_best_datatype([comp[1] for comp in file_name_components])
    peptide_df['HighScan'] = _convert_to_best_datatype([comp[2] for comp in file_name_components])
    peptide_df['Charge'] = _convert_to_best_datatype([comp[3] for comp in file_name_components])

    peptide_df = peptide_df.convert_dtypes()
    protein_df = protein_df.convert_dtypes()

    if end_lines[-1] == '':
        end_lines = end_lines[:-1]

    return header_lines, peptide_df, protein_df, end_lines


def to_dta_select_filter(header_lines: List[str], peptide_df: pd.DataFrame, protein_df: pd.DataFrame,
                         end_lines: List[str]) -> StringIO:
    """
    Convert the given header lines, peptide and protein dataframes, and end lines into a StringIO object.

    This function takes the header lines, peptide and protein dataframes, and end lines as inputs, and writes
    them into a StringIO object in the DTASelect-filter.txt format.

    Args:
        header_lines (List[str]): A list of header lines.
        peptide_df (pd.DataFrame): A dataframe containing peptide data.
        protein_df (pd.DataFrame): A dataframe containing protein data.
        end_lines (List[str]): A list of end lines (information lines).

    Returns:
        StringIO: A StringIO object containing the reformatted data in DTASelect-filter.txt format.
    """

    peptide_df = peptide_df.copy(deep=True)
    protein_df = protein_df.copy(deep=True)

    file_output = StringIO()

    # Write header lines
    _write_lines(file_output, header_lines)

    # Write protein and peptide data
    concatenated_file_names = peptide_df.apply(_create_file_name, axis=1)
    peptide_df.drop(['FileName', 'LowScan', 'HighScan', 'Charge'], axis=1, inplace=True)
    peptide_df['FileName'] = concatenated_file_names
    # Re-order columns to make FileName the second column
    peptide_df = _reorder_columns(peptide_df, 'FileName', 1)

    protein_data_str = protein_df.drop(['ProteinGroup'], axis=1).to_csv(header=False, index=False, sep='\t')
    peptide_data_str = peptide_df.drop(['ProteinGroup'], axis=1).to_csv(header=False, index=False, sep='\t')

    protein_data_str = protein_data_str.replace('\r', '')
    peptide_data_str = peptide_data_str.replace('\r', '')

    current_protein_grp = 0
    protein_lines = protein_data_str.split('\n')
    peptide_lines = peptide_data_str.split('\n')

    if protein_lines[-1] == '':
        protein_lines = protein_lines[:-1]

    if peptide_lines[-1] == '':
        peptide_lines = peptide_lines[:-1]

    protein_line_idx = 0
    peptide_line_idx = 0

    while protein_line_idx < len(protein_lines) and peptide_line_idx < len(peptide_lines):
        if int(protein_df.iloc[protein_line_idx]['ProteinGroup']) == current_protein_grp:
            file_output.write(protein_lines[protein_line_idx] + '\n')
            protein_line_idx += 1
        else:
            file_output.write(peptide_lines[peptide_line_idx] + '\n')
            peptide_line_idx += 1
            if peptide_line_idx < len(peptide_lines) and int(
                    peptide_df.iloc[peptide_line_idx - 1]['ProteinGroup']) != int(
                peptide_df.iloc[peptide_line_idx]['ProteinGroup']):
                current_protein_grp += 1

    # Write remaining protein and peptide lines
    _write_lines(file_output, protein_lines[protein_line_idx:])
    _write_lines(file_output, peptide_lines[peptide_line_idx:])

    _write_lines(file_output, end_lines)

    return file_output
