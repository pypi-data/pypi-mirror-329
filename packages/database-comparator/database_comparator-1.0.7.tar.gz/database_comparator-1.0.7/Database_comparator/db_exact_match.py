from .config_class import cfg
import pandas as pd
import numpy as np
import multiprocessing as mp
from joblib import Parallel, delayed  # Efficient parallel processing

class ExactMatch:
    """
    The exact_match class provides methods for performing exact match searches in databases.

    It allows for exact match searches in a single database or across all databases, using both single-core and
    multiprocessing techniques. The class handles the insertion of matching results into the input DataFrame
    based on the provided configuration.
    """
    def __init__(self, config: cfg) -> None:
        """
        Initialize the exact_match class with a configuration.

        Args:
            config (cfg): An instance of the configuration class.

        Note:
            This constructor sets up the exact_match class with the provided configuration.
        """
        self.config = config
        self.query_sequences = np.array(
            self.config.input_df[self.config.input_file_info["sequence_column_name"]].tolist(), dtype=object
        )
        self.data_df = None  # Placeholder for the loaded database DataFrame
        self.original_indices = self.config.input_df.index.values  # Store original indices to preserve mapping

        self.config.logger.info("Exact Match class initialized.")

    def exact_match_search_in_single_database(self, database_index: int, parallel=False) -> None:
        """
        Perform an exact match search in a single database.

        Args:
            database_index (int): Index of the database to perform the search on.
            parallel (bool): Whether to use parallel processing (default is False).

        Returns:
            pd.DataFrame: The input DataFrame with matching results.

        Note:
            This method performs an exact match search in a single database and can optionally use parallel processing.
            Matching results are inserted into the input DataFrame using the configuration settings.
        """

        self.config.logger.info(f"Performing exact match search in database {database_index}.")
        if parallel:
            self.config.logger.info("Switching to multiprocessing mode.")
            self.exact_match_search_in_single_database_MULTIPROCESSING(database_index=database_index)
            return

        self.data_df = self.config.load_database(database_index=database_index, engine="python")
        data_sequences = np.array(self.data_df[self.config.data_info[database_index]["sequence_column_name"]], dtype=object)


        for i, query_seq in enumerate(self.query_sequences):
            matches = np.where(data_sequences == query_seq)[0]
            for j in matches:
                self.config.insert_match_to_input_df(
                    data_df=self.data_df,
                    database_index=database_index,
                    input_sequence_index=i,
                    output_sequence_index=j
                )

        self.config.logger.info(f"Exact match search in database {database_index} completed.")


    def exact_match_search_in_all_databases(self, parallel=False) -> None:
        """
        Finds exact matches for query sequences across all databases.
        """
        self.config.reset_before_analysis()
        self.config.logger.info("Performing exact match search in all databases.")
        for db_index in range(len(self.config.data_info)):
            self.exact_match_search_in_single_database(database_index=db_index, parallel=parallel)


    def exact_match_search_in_single_database_MULTIPROCESSING(self, database_index: int) -> None:
        """
        Perform an exact match search in a single database using multiprocessing.

        Args:
            database_index (int): Index of the database to perform the search on.

        Note:
            This method performs an exact match search in a single database using multiprocessing.
            Matching results are inserted into the input DataFrame using the configuration settings.
        """

        self.config.logger.info(f"Performing exact match search in database {database_index} using multiprocessing.")
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

        self.config.logger.info("Procesing output chunks...")
        for result in results:
            for i, j in result:
                self.config.insert_match_to_input_df(
                    data_df=self.data_df,
                    database_index=database_index,
                    input_sequence_index=i,
                    output_sequence_index=j
                )

        self.config.logger.info(f"Exact match search in database {database_index} completed using multiprocessing.")

    def exact_match_search_in_all_databases_MULTIPROCESSING(self) -> None:
        """
        Finds exact matches for query sequences across all databases in parallel.
        """
        self.config.reset_before_analysis()
        self.config.logger.info("Performing exact match search in all databases using multiprocessing.")
        for db_index in range(len(self.config.data_info)):
            self.exact_match_search_in_single_database_MULTIPROCESSING(db_index) 

    def process_chunk(self, query_chunk, original_indices, data_sequences, database_index):
        """
        Processes a chunk of queries in parallel, ensuring original sequence indices are preserved.

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
            matches = np.where(data_sequences == query_seq)[0]
            result.extend([(original_indices[i], j) for j in matches])
        return result

