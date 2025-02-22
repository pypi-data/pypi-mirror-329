import pandas as pd
from .config_class import cfg
import os

import subprocess

import Database_comparator.Fasta_maker as Fasta_maker


FastaSeparator = "!"


class Blast:
    """
    The blast class provides methods for performing BLAST (Basic Local Alignment Search Tool) searches
    and analyzing the results.

    It can create BLAST databases, perform BLAST searches with provided query sequences, and analyze the
    search results, including inserting matching results into the input DataFrame based on the provided
    configuration.
    """
    def __init__(self, config: cfg) -> None:
        self.config = config
        self.config.logger.info("Blast class initialized.")



    # PUBLIC Blast algorithm
    def blast_database_info(self):
        """
        Print information about inserted databases for blast search.

        Note:
            This method prints information about the databases used for BLAST searches, including matrix, gap penalties,
            neighboring words threshold, and window size for multiple hits.
        """
        print("Inserted databases:")
        for database in self.config.in_blast_database:
            print(database)
        print("-----------------------------------------------------")
        print("Matrix: BLOSUM62")
        print("GaPenalties: Existence: 11, Extension: 1")
        print("Neighboring words threshold: 11")
        print("Window for multiple hits: 40")

    def blast_make_database(self, name = "Database", force=False):
        """
        Create a BLAST database with the given name.

        Args:
            name (str): Name of the BLAST database.
            force (bool): Whether to overwrite an existing database and make a new fasta file for all databases (default is False).

        Note:
            This method creates a BLAST database, including the generation of a fasta file from the provided data
            configurations and specified name.
        """

        self.config.logger.info(f"Creating BLAST database {name}.")
        os.makedirs("Fasta_files", exist_ok=True)
        os.makedirs("Query_files", exist_ok=True)
        fasta_file_name = "Fasta_files/BLAST_fasta_file.fasta"

        if not os.path.exists(fasta_file_name) or force:
            fasta_maker = Fasta_maker.Fasta_maker(
                data_dfs=[self.config.load_database(database_index = i) for i in range(len(self.config.data_info))],
                sequence_column_names=[self.config.data_info[i]["sequence_column_name"] for i in range(len(self.config.data_info))],
                identifiers=[self.config.data_info[i]["identifier_of_seq"] for i in range(len(self.config.data_info))],
                result_columns=[self.config.data_info[i]["results_column"] for i in range(len(self.config.data_info))],
                output_file_name=fasta_file_name,
                separator=FastaSeparator)

            fasta_maker.make_file()

        command = [
        "makeblastdb", "-dbtype", "prot", "-in", fasta_file_name,
        "-title", name, "-max_file_sz", "4GB", "-out", self.config.blast_database_full_name]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
        except FileNotFoundError:
            self.config.logger.critical("BLAST+ tools are not installed. Please install BLAST+ tools to use this feature.")
            raise FileNotFoundError("BLAST+ tools are not installed. Please install BLAST+ tools to use this feature.")
        except Exception as e:
            self.config.logger.critical(f"BLAST database creation failed: {e}")
            raise RuntimeError(f"BLAST database creation failed: {e}")
        
        if result.returncode != 0:
            self.config.logger.error(f"BLAST database creation failed: {result.stderr}")
            raise RuntimeError(f"BLAST database creation failed: {result.stderr}")
        
        self.config.logger.info(f"BLAST database {name} created.")

    def blast_search_for_match_in_database(self, query=None):
        """
        Perform a BLAST search in a BLAST database.

        Args:
            query (str or None): Path to the query sequence file (default is None, uses default input query).

        Note:
            This method performs a BLAST search against the specified database, using the provided query sequence
            or the default input query.
        """

        self.config.logger.info(f"Performing BLAST search. Blasting against {self.config.blast_database_full_name}")

        if query is None:
            fasta_maker = Fasta_maker.Fasta_maker(
                data_dfs=[self.config.input_df],
                sequence_column_names=[self.config.input_file_info["sequence_column_name"]],
                identifiers=[],
                result_columns=[],
                output_file_name=self.config.blast_default_input_query,
                separator=FastaSeparator)
            fasta_maker.make_query()
            query = self.config.blast_default_input_query

        command = [
        "blastp", "-query", query, "-db", self.config.blast_database_full_name,
        "-evalue", str(self.config.e_value), "-outfmt", self.config.blast_outfmt,
        "-out", self.config.blast_output_name]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
        except FileNotFoundError:
            self.config.logger.critical("BLAST+ tools are not installed. Please install BLAST+ tools to use this feature.")
            raise FileNotFoundError("BLAST+ tools are not installed. Please install BLAST+ tools to use this feature.")
        except Exception as e:
            self.config.logger.critical(f"BLAST search failed: {e}")
            raise RuntimeError(f"BLAST search failed: {e}")
        
        if result.returncode != 0:
            self.config.logger.error(f"BLAST search failed: {result.stderr}")
            raise RuntimeError(f"BLAST search failed: {result.stderr}")
        
        self.config.logger.info("BLAST search completed.")

    def blast_search_and_analyze_matches_in_database(self, query=None) -> pd.DataFrame:
        """
        Perform a BLAST search in a BLAST database and then analyze the output data.

        Args:
            query (str or None): Path to the query sequence file (default is None, uses default input query).

        Note:
            This method combines BLAST search with the analysis of the search results, including inserting
            matching results into the input DataFrame.
        """
        self.blast_search_for_match_in_database(query)
        self.blast_analyze_output_data()

        return self.config.input_df.copy(deep=True)

    def blast_analyze_output_data(self) -> None:
        """
        Analyze the output data from a BLAST search and insert results into the input DataFrame.

        Note:
            This method analyzes the output data from a previous BLAST search and inserts matching results
            into the input DataFrame using the specified aligner and configuration settings.
        """

        self.config.logger.info("Analyzing BLAST output data with aligner.")
        self.config.reset_before_analysis()
        columns_names = self.config.blast_outfmt.split()
        data_df = pd.read_csv(self.config.blast_output_name, sep="\t", names=columns_names[1:]).drop_duplicates()

        for i in range(len(data_df)): self.__insert_blast_results_to_input_df(data_df, i)

        self.config.logger.info("BLAST output data analyzed and inserted into the input DataFrame.")
        
    def __insert_blast_results_to_input_df(self, data_df: pd.DataFrame, index):
        """
        Insert BLAST results into the input DataFrame.

        Args:
            data_df (pd.DataFrame): Data frame containing BLAST results.
            index (int): Index of the result to be inserted.

        Note:
            This private method processes and inserts BLAST search results into the input DataFrame based on the
            specified configuration settings.
        """
        input_seq_index = int(str(data_df["qseqid"][index]).replace("seq", ""))
        labels = data_df["sseqid"][index].split(sep="!")
        sseq = str(data_df["sseq"][index])

        file_name = labels[0]
        output_seq_identifier = labels[1] if len(labels) > 1 else labels[0]
        output_seq_identifier = ";".join(set(output_seq_identifier.split(sep=";")))

        database_index = self.config.find_database_index(filename=file_name)
        results_column = self.config.data_info[database_index]["results_column"]


        if pd.isnull(self.config.input_df[results_column][input_seq_index]):
            self.config.input_df.loc[input_seq_index, results_column] = f"[seq: {sseq} identifier:{output_seq_identifier}]" + self.config.separator_of_results_in_input_df
        else:
            self.config.input_df.loc[input_seq_index, results_column] += f"[seq: {sseq} identifier:{output_seq_identifier}]" + self.config.separator_of_results_in_input_df
