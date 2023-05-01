import unittest
from io import StringIO

import pandas as pd

from filterframes import from_dta_select_filter, to_dta_select_filter


class TestPandasParser(unittest.TestCase):

    def test_from_dta_select_filter_to_df_V2_1_12_paser(self):
        # tests passing TextIO
        with open('tests/data/DTASelect-filter_V2_1_12_paser.txt', 'r') as file:
            head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(file)
        self.assertEqual(3, len(protein_df))

        io = to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)

        # tests passing StringIO
        self.assertEqual(type(io), StringIO)
        head_lines2, peptide_df2, protein_df2, tail_lines2 = from_dta_select_filter(io)
        pd.testing.assert_frame_equal(peptide_df, peptide_df2)
        self.assertEqual(head_lines, head_lines2)
        self.assertEqual(tail_lines, tail_lines2)

        # tests passing str
        str_value = io.getvalue()
        self.assertEqual(type(str_value), str)
        head_lines3, peptide_df3, protein_df3, tail_lines3 = from_dta_select_filter(str_value)
        pd.testing.assert_frame_equal(peptide_df, peptide_df3)
        self.assertEqual(head_lines, head_lines3)
        self.assertEqual(tail_lines, tail_lines3)

    def test_from_dta_select_filter_to_df_V2_1_13(self):
        # tests passing TextIO
        with open('tests/data/DTASelect-filter_V2_1_13.txt', 'r') as file:
            head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(file)
        self.assertEqual(8, len(protein_df))

        io = to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)

        # tests passing StringIO
        self.assertEqual(type(io), StringIO)
        head_lines2, peptide_df2, protein_df2, tail_lines2 = from_dta_select_filter(io)
        pd.testing.assert_frame_equal(peptide_df, peptide_df2)
        self.assertEqual(head_lines, head_lines2)
        self.assertEqual(tail_lines, tail_lines2)

        # tests passing str
        str_value = io.getvalue()
        self.assertEqual(type(str_value), str)
        head_lines3, peptide_df3, protein_df3, tail_lines3 = from_dta_select_filter(str_value)
        pd.testing.assert_frame_equal(peptide_df, peptide_df3)
        self.assertEqual(head_lines, head_lines3)
        self.assertEqual(tail_lines, tail_lines3)


if __name__ == '__main__':
    unittest.main()
