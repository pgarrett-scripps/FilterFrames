# example.py
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
