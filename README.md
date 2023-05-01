![example workflow](https://github.com/pgarrett-scripps/FilterFrames/actions/workflows/python-package.yml/badge.svg)
![example workflow](https://github.com/pgarrett-scripps/FilterFrames/actions/workflows/pylint.yml/badge.svg)

# filterframes

filterframes is a Python package that provides an easy way to parse and manipulate DTASelect filter 
files using pandas. The package allows you to read DTASelect-filter.txt files, create peptide and protein dataframes, 
modify the dataframes, and write the modified dataframes back to a new DTASelect-filter.txt file. 

### Note on dataframe columns:

The column names in the peptide and protein dataframes will correspond to the header lines in the DTASelect-filter.txt
files. In order to edit and output a valid DTASelect-filter file you must ensure that the
peptide and protein dataframe column names and order are conserved, and that no additional columns are 
included. Any changes in the columns order or names will be reflected  in the output DTASelect-filter.txt file.

## Installation

You can install filterframes using pip:

```sh
pip install filterframes
```

You can also install filterframes locally:

```sh
git clone https://github.com/pgarrett-scripps/FilterFrames.git
cd filterframes
pip install .
```

## Usage

Here are some basic examples of how to use the package:

### Example Python Script:
```python
from filterframes import from_dta_select_filter, to_dta_select_filter

# Read DTASelect-filter.txt file and create peptide and protein dataframes
file_input = r'tests/data/DTASelect-filter_V2_1_12_paser.txt'
header_lines, peptide_df, protein_df, end_lines = from_dta_select_filter(file_input)

# Display the first 5 rows of the peptide and protein dataframes
print("Peptide DataFrame:")
print(peptide_df.head())
print("\nProtein DataFrame:")
print(protein_df.head())

# Modify peptide or protein dataframes as needed (e.g., filtering, normalization, etc.)
# ...

# Write modified peptide and protein dataframes back to a DTASelect-filter.txt file
file_output = r'tests/data/DTASelect-filter_V2_1_12_paser.out.txt'
with open(file_output, 'w') as f:
    output_string_io = to_dta_select_filter(header_lines, peptide_df, protein_df, end_lines)
    f.write(output_string_io.getvalue())

print(f"\nModified DTASelect-filter.txt file saved to {file_output}")
```

### Example Streamlit App:

```python
# app.py
from io import StringIO

import streamlit as st
from filterframes import from_dta_select_filter, to_dta_select_filter

uploaded_filter_file = st.file_uploader("Choose a DTASelect-filter.txt file", type="txt")

if uploaded_filter_file:
    header_lines, peptide_df, protein_df, end_lines = from_dta_select_filter(StringIO(uploaded_filter_file.getvalue().decode('utf-8')))
    
    st.header('Peptide df')
    st.dataframe(peptide_df)
    st.header('Protein df')
    st.dataframe(protein_df)

    # Modify peptide or protein dataframes as needed (e.g., filtering, normalization, etc.)
    # ...

    io = to_dta_select_filter(header_lines, peptide_df, protein_df, end_lines)

    st.download_button(label="Download Filter",
                       data=io.getvalue(),
                       file_name="DTASelect-filter.txt",
                       mime="text/plain")
```

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

