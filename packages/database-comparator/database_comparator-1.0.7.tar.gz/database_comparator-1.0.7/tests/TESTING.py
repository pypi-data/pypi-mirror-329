import sys
import os
import pandas as pd
import numpy as np
from tabulate import tabulate
import time

# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# open folder Database_comparator
sys.path.append(project_root)

# Now you can import db_compare
import Database_comparator.db_compare as db_compare

def clean_up_blast_files():
        # Cleanup temporary files
    if os.path.exists("Fasta_files"):
        for file in os.listdir("Fasta_files"):
            os.remove(os.path.join("Fasta_files", file))
        os.rmdir("Fasta_files")

    if os.path.exists("Query_files"):
        for file in os.listdir("Query_files"):
            os.remove(os.path.join("Query_files", file))
        os.rmdir("Query_files")

    if os.path.exists("BLAST_database"):
        for file in os.listdir("BLAST_database"):
            os.remove(os.path.join("BLAST_database", file))
        os.rmdir("BLAST_database")

    if os.path.exists("blastp_output.txt"):os.remove("blastp_output.txt")

def test_initialization():
    """Tests if the DB_comparator class initializes correctly and measures initialization time."""
    config_file = r"TEST_config_file.xlsx"

    try:
        start_time = time.time()
        db_comparator = db_compare.DB_comparator(config_file)
        end_time = time.time()
        elapsed_time = end_time - start_time

        passed = True
        if db_comparator is None: passed = False
        if db_comparator.config != db_comparator.aligner.config: passed = False
        if db_comparator.config != db_comparator.exact_match.config: passed = False
        if db_comparator.config != db_comparator.hamming_distances.config: passed = False
        if db_comparator.config != db_comparator.fast_hamming_distances.config: passed = False
        if db_comparator.config != db_comparator.blast.config: passed = False

        return "✅ Success" if passed else "❌ Failed", "N/A", elapsed_time

    except Exception as e:
        return "❌ Failed", "N/A", "N/A"

def test_exporting():
    """Tests if the DB_comparator class exports data frames correctly."""
    config_file = r"TEST_config_file.xlsx"
    possible_formats = ['xlsx', 'csv', 'tsv', 'md']
    try:
        db_comparator = db_compare.DB_comparator(config_file, show_log_in_console=False, log_write_append="a")

        start_time = time.time()
        for data_format in possible_formats:
            db_comparator.export_data_frame("TEST_exporting." + data_format, data_format)
            os.remove("TEST_exporting." + data_format)
        end_time = time.time()

        final_time = (end_time - start_time)/len(possible_formats)

        
        return "✅ Success", "N/A", final_time

    except Exception as e:
        for data_format in possible_formats:
            if os.path.exists("TEST_exporting." + data_format):
                os.remove("TEST_exporting." + data_format)

        return "❌ Failed", "N/A", "N/A"

def run_test(test_function, true_file_path, output_file_name):
    """Runs a test function, checks search success, file comparison, and measures execution time."""
    config_file = r"TEST_config_file.xlsx"

    try:
        db_comparator = db_compare.DB_comparator(config_file, show_log_in_console=False, log_write_append="a")

        # Measure search execution time
        start_time = time.time()
        test_function(db_comparator)
        end_time = time.time()
        elapsed_time = end_time - start_time

        search_status = "✅ Success"

        # Compare generated test file with true file
        true_file = pd.read_excel(true_file_path)
        test_file = pd.read_excel(output_file_name)
        comparison_status = "✅ Match" if true_file.equals(test_file) else "❌ Mismatch"

        os.remove(output_file_name)
        clean_up_blast_files()

        return search_status, comparison_status, elapsed_time

    except Exception as e:
        if os.path.exists(output_file_name): os.remove(output_file_name)
        clean_up_blast_files()
        return "❌ Failed", "❌ Not compared", "N/A"

def exact_match_TEST(db_comparator: db_compare.DB_comparator):
    """Performs an exact match test."""
    db_comparator.exact_match.exact_match_search_in_all_databases(parallel=False)
    db_comparator.export_data_frame("exact_match_TEST_testing.xlsx")

def hamming_distances_TEST(db_comparator: db_compare.DB_comparator):
    """Performs a hamming distances test."""
    db_comparator.fast_hamming_distances.find_hamming_distances_for_all_databases(parallel=False)
    db_comparator.export_data_frame("hamming_distances_TEST_testing.xlsx")

def aligner_TEST(db_comparator: db_compare.DB_comparator):
    """Performs an aligner test."""
    db_comparator.aligner.aligner_search_in_all_databases(parallel=False)
    db_comparator.export_data_frame("aligner_TEST_testing.xlsx")

def blast_TEST(db_comparator: db_compare.DB_comparator):
    """Performs a BLAST test."""
    db_comparator.blast.blast_make_database()
    db_comparator.blast.blast_search_and_analyze_matches_in_database()
    db_comparator.export_data_frame("blast_TEST_testing.xlsx")

    clean_up_blast_files()

def generate_table_of_results():
    """Generates a table of test results, including search success, file comparison, and execution time."""
    results = [
        ["Test Name", "Status", "File Comparison", "Execution Time (s)"],
        ["Initialization Test", *test_initialization()],
        ["Exporting Test", *test_exporting()],
        ["Exact Match Test", *run_test(exact_match_TEST, "True_files/exact_match_TEST_true.xlsx", "exact_match_TEST_testing.xlsx")],
        ["Hamming Distances Test", *run_test(hamming_distances_TEST, "True_files/hamming_distances_TEST_true.xlsx", "hamming_distances_TEST_testing.xlsx")],
        ["Aligner Test", *run_test(aligner_TEST, "True_files/aligner_TEST_true.xlsx", "aligner_TEST_testing.xlsx")],
        ["BLAST Test", *run_test(blast_TEST, "True_files/blast_TEST_true.xlsx", "blast_TEST_testing.xlsx")]
    ]

    table = tabulate(results, headers="firstrow", tablefmt="fancy_grid", floatfmt=".4f")
    print(table)

def main():
    generate_table_of_results()

if __name__ == "__main__":
    main()
