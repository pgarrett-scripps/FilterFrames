# pandas-dta-select-parser

`pandas_dta_select_parser` is a Python package that provides an easy way to parse and manipulate DTASelect filter 
files using pandas. The package allows you to read DTASelect-filter.txt files, create peptide and protein dataframes, 
modify the dataframes, and write the modified dataframes back to a new DTASelect-filter.txt file.

## Installation

You can install `pandas_dta_select_parser` using pip:

```sh
pip install pandas-dta-select-parser
```

## Usage
Here's a basic example of how to use the package:

```python
from src.filterframes import from_dta_select_filter, to_dta_select_filter

# Read DTASelect-filter.txt file and create peptide and protein dataframes
file_input = "path/to/DTASelect-filter.txt"
header_lines, peptide_df, protein_df, end_lines = from_dta_select_filter(file_input)

# Modify peptide or protein dataframes as needed (e.g., filtering, normalization, etc.)
# ...

# Write modified peptide and protein dataframes back to a DTASelect-filter.txt file
file_output = "path/to/output/DTASelect-filter_modified.txt"
with open(file_output, 'w') as f:
    output_string_io = to_dta_select_filter(header_lines, peptide_df, protein_df, end_lines)
    f.write(output_string_io.getvalue())
```

More advance use cases can be found in examples.py

## Functions
The main functions provided by the package are:


```
from_dta_select_filter(file_input: Union[str, TextIOWrapper, StringIO]) -> Tuple[List[str], pd.DataFrame, pd.DataFrame, List[str]]
```

Reads a DTASelect-filter.txt file and returns header lines, peptide dataframe, protein dataframe, and end lines.


```
to_dta_select_filter(header_lines: List[str], peptide_df: pd.DataFrame, protein_df: pd.DataFrame, end_lines: List[str]) -> StringIO
```

Writes the given header lines, peptide dataframe, protein dataframe, and end lines to a StringIO object in the DTASelect-filter.txt format.

