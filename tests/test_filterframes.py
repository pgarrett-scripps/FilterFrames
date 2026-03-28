"""Tests for filterframes package."""

import os
from io import StringIO

import pandas as pd
import pytest

from filterframes import from_dta_select_filter, to_dta_select_filter

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestRoundTrip:
    """Round-trip tests: read -> parse -> write -> re-parse -> compare."""

    def test_v2_1_12_paser(self):
        with open(os.path.join(DATA_DIR, "DTASelect-filter_V2_1_12_paser.txt"), "r") as file:
            head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(file)
        assert len(protein_df) == 3

        io = to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)
        assert isinstance(io, StringIO)

        head_lines2, peptide_df2, protein_df2, tail_lines2 = from_dta_select_filter(io)
        pd.testing.assert_frame_equal(peptide_df, peptide_df2)
        pd.testing.assert_frame_equal(protein_df, protein_df2)
        assert head_lines == head_lines2
        assert tail_lines == tail_lines2

    def test_v2_1_13(self):
        with open(os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt"), "r") as file:
            head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(file)
        assert len(protein_df) == 8

        io = to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)
        assert isinstance(io, StringIO)

        head_lines2, peptide_df2, protein_df2, tail_lines2 = from_dta_select_filter(io)
        pd.testing.assert_frame_equal(peptide_df, peptide_df2)
        pd.testing.assert_frame_equal(protein_df, protein_df2)
        assert head_lines == head_lines2
        assert tail_lines == tail_lines2


class TestInputTypes:
    """Test that all supported input types work correctly."""

    def test_file_path_input(self):
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(path)
        assert len(protein_df) > 0
        assert len(peptide_df) > 0

    def test_string_input(self):
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        with open(path, "r") as f:
            content = f.read()
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(content)
        assert len(protein_df) == 8

    def test_stringio_input(self):
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        with open(path, "r") as f:
            content = f.read()
        sio = StringIO(content)
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(sio)
        assert len(protein_df) == 8

    def test_stringio_input_rewind(self):
        """Ensure StringIO is rewound before reading (seek(0) is called internally)."""
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        with open(path, "r") as f:
            content = f.read()
        sio = StringIO(content)
        sio.read()  # exhaust the StringIO
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(sio)
        assert len(protein_df) == 8


class TestErrorHandling:
    """Test error conditions."""

    def test_unsupported_input_type(self):
        with pytest.raises(ValueError, match="Unsupported input type"):
            # Pass an integer, which is not iterable in the expected way
            from_dta_select_filter(12345)

    def test_invalid_file_content(self):
        with pytest.raises((ValueError, TypeError)):
            from_dta_select_filter("not a valid DTASelect file at all")


class TestDataIntegrity:
    """Test that parsed data has expected structure and types."""

    def test_peptide_df_has_filename_components(self):
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        _, peptide_df, _, _ = from_dta_select_filter(path)
        assert "FileName" in peptide_df.columns
        assert "LowScan" in peptide_df.columns
        assert "HighScan" in peptide_df.columns
        assert "Charge" in peptide_df.columns

    def test_protein_group_column_exists(self):
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        _, peptide_df, protein_df, _ = from_dta_select_filter(path)
        assert "ProteinGroup" in peptide_df.columns
        assert "ProteinGroup" in protein_df.columns

    def test_to_dta_select_filter_does_not_mutate_input(self):
        """Ensure that to_dta_select_filter does not modify the input DataFrames."""
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        head_lines, peptide_df, protein_df, tail_lines = from_dta_select_filter(path)

        peptide_copy = peptide_df.copy(deep=True)
        protein_copy = protein_df.copy(deep=True)

        to_dta_select_filter(head_lines, peptide_df, protein_df, tail_lines)

        pd.testing.assert_frame_equal(peptide_df, peptide_copy)
        pd.testing.assert_frame_equal(protein_df, protein_copy)

    def test_header_and_end_lines_are_strings(self):
        path = os.path.join(DATA_DIR, "DTASelect-filter_V2_1_13.txt")
        head_lines, _, _, tail_lines = from_dta_select_filter(path)
        assert all(isinstance(line, str) for line in head_lines)
        assert all(isinstance(line, str) for line in tail_lines)
