import pandas as pd
from .config_class import cfg
import multiprocessing as mp
import numpy as np
from joblib import Parallel, delayed  # Efficient parallel processing

class FastHammingDistance:
    """
    Class for efficiently computing Hamming distances between query sequences and database sequences.
    Supports both sequential and parallel processing for handling large datasets.
    """

    def __init__(self, config: cfg) -> None:
        """
        Initializes the FastHammingDistance class.

        Args:
            config (cfg): Configuration object containing database and input sequence information.
        """
        self.config = config
        # Convert input query sequences into a NumPy array for fast access
        self.query_sequences = np.array(self.config.input_df[self.config.input_file_info["sequence_column_name"]].tolist(), dtype=object)
        self.data_df = None  # Placeholder for the loaded database DataFrame
        self.original_indices = self.config.input_df.index.values  # Store original indices to preserve mapping

        self.config.logger.info("Fast Hamming distance initialized.")

    def __find_hamming_distance(self, query_seq: str, data_seq: str) -> int:
        """
        Computes the Hamming distance between two sequences.
        If sequences are of different lengths, they are padded with '?' to make them equal.

        Args:
            query_seq (str): Query sequence from input dataset.
            data_seq (str): Sequence from the database.

        Returns:
            int: Hamming distance between the two sequences.
        """
        max_length: int = max(len(query_seq), len(data_seq))

        # Pad sequences with '?' to match lengths for accurate comparison
        padded_query_seq = np.full(max_length, "?", dtype="<U1")
        padded_data_seq = np.full(max_length, "?", dtype="<U1")

        # Copy original sequence characters into padded arrays
        padded_query_seq[:len(query_seq)] = list(query_seq)
        padded_data_seq[:len(data_seq)] = list(data_seq)

        # Compute the Hamming distance by counting character mismatches
        return np.sum(padded_query_seq != padded_data_seq)

    def find_hamming_distances_for_single_database(self, database_index: int, parallel=True) -> None:
        """
        Computes Hamming distances for a single database against all query sequences.
        Supports parallel processing to speed up large computations.

        Args:
            database_index (int): Index of the database to process.
            parallel (bool): Whether to use parallel processing (default: True).
        """

        self.config.logger.info("Computing Hamming distances for database " + str(database_index) + "...")
        if parallel:
            self.config.logger.info("Switching to multiprocessing mode.")
            self.find_hamming_distances_for_single_database_MULTIPROCESSING(database_index)
            return

        # Load database only once to reduce file access overhead
        self.data_df = self.config.load_database(database_index=database_index, engine="python")

        for i in range(len(self.query_sequences)):
            for j in range(len(self.data_df)):
                distance = self.__find_hamming_distance(query_seq=self.query_sequences[i], 
                                                        data_seq=self.data_df[self.config.data_info[database_index]["sequence_column_name"]].iloc[j])
                

                if distance <= self.config.max_hamming_distance:
                    self.config.insert_match_to_input_df(
                        data_df=self.data_df,
                        database_index=database_index,
                        input_sequence_index=i,
                        output_sequence_index=j
                    )

        self.config.logger.info(f"Hamming distances for database {database_index} completed.")
        
    def find_hamming_distances_for_all_databases(self, parallel=False) -> None:
        """
        Computes Hamming distances for all databases sequentially or in parallel.
        """

        self.config.reset_before_analysis()
        self.config.logger.info("Computing Hamming distances for all databases.")
        for db_index in range(len(self.config.data_info)):
            self.find_hamming_distances_for_single_database(database_index=db_index, parallel=parallel)

    def find_hamming_distances_for_single_database_MULTIPROCESSING(self, database_index: int) -> None:
        """
        Computes Hamming distances for a single database in parallel using multiprocessing.
        Ensures proper handling of original indices to maintain correct results.

        Args:
            database_index (int): Index of the database to process.
        """

        self.config.logger.info(f"Computing Hamming distances for database {database_index} using multiprocessing.")
        self.data_df = self.config.load_database(database_index=database_index, engine="python")
        data_sequences = np.array(self.data_df[self.config.data_info[database_index]["sequence_column_name"]], dtype=object)
        
        # Correctly map original indices to corresponding query sequence chunks
        split_indices = np.array_split(self.original_indices, self.config.number_of_processors)
        split_queries = np.array_split(self.query_sequences, self.config.number_of_processors)
        input_chunks = list(zip(split_queries, split_indices))

        results = Parallel(n_jobs=self.config.number_of_processors)(
            delayed(self.process_chunk)(chunk, indices, data_sequences, database_index)
            for chunk, indices in input_chunks
        )

        # Store matching sequences in the input DataFrame

        self.config.logger.info("Procesing output chunks...")
        for result in results:
            for i, j in result:
                self.config.insert_match_to_input_df(
                    data_df=self.data_df,
                    database_index=database_index,
                    input_sequence_index=i,
                    output_sequence_index=j
                )
        self.config.logger.info(f"Hamming distances for database {database_index} completed using multiprocessing.")

    def find_hamming_distances_for_all_databases_MULTIPROCESSING(self) -> None:
        """
        Computes Hamming distances for all databases in parallel using multiprocessing.
        """
        self.config.reset_before_analysis()
        self.config.logger.info("Computing Hamming distances for all databases using multiprocessing.")
        for db_index in range(len(self.config.data_info)):
            self.find_hamming_distances_for_single_database_MULTIPROCESSING(db_index) 



    def process_chunk(self, query_chunk, original_indices, data_sequences, database_index):
        """
        Processes a chunk of queries in parallel.
        Ensures original query sequence indices are preserved.

        Args:
            query_chunk (np.array): Chunk of query sequences.
            original_indices (np.array): Original indices of the query sequences.
            data_sequences (np.array): Array of database sequences.
            database_index (int): Index of the database being processed.

        Returns:
            list: List of tuples containing (original query index, matching database index).
        """
        result = []
        for i, query_seq in enumerate(query_chunk):
            distances = np.array([self.__find_hamming_distance(query_seq, d_seq) for d_seq in data_sequences])
            valid_matches = np.where(distances <= self.config.max_hamming_distance)[0]
            result.extend([(original_indices[i], j) for j in valid_matches])
        return result
