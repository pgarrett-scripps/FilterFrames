from io import StringIO

import pandas as pd

from filterframes import from_dta_select_filter, to_dta_select_filter


def test_from_dta_select_filter_to_df_V2_1_12_paser():
    with open('tests/data/DTASelect-filter_V2_1_12_paser.txt', 'r') as file:
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(file)
    assert len(protein_df) == 3

    io = to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)

    assert isinstance(io, StringIO)
    head_lines2, peptide_df2, protein_df2, tail_lines2 = from_dta_select_filter(io)
    pd.testing.assert_frame_equal(peptide_df, peptide_df2)
    assert head_lines == head_lines2
    assert tail_lines == tail_lines2

    str_value = io.getvalue()
    assert isinstance(str_value, str)
    head_lines3, peptide_df3, protein_df3, tail_lines3 = from_dta_select_filter(str_value)
    pd.testing.assert_frame_equal(peptide_df, peptide_df3)
    assert head_lines == head_lines3
    assert tail_lines == tail_lines3


def test_from_dta_select_filter_to_df_V2_1_13():
    with open('tests/data/DTASelect-filter_V2_1_13.txt', 'r') as file:
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(file)
    assert len(protein_df) == 8

    io = to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)

    assert isinstance(io, StringIO)
    head_lines2, peptide_df2, protein_df2, tail_lines2 = from_dta_select_filter(io)
    pd.testing.assert_frame_equal(peptide_df, peptide_df2)
    assert head_lines == head_lines2
    assert tail_lines == tail_lines2

    str_value = io.getvalue()
    assert isinstance(str_value, str)
    head_lines3, peptide_df3, protein_df3, tail_lines3 = from_dta_select_filter(str_value)
    pd.testing.assert_frame_equal(peptide_df, peptide_df3)
    assert head_lines == head_lines3
    assert tail_lines == tail_lines3
