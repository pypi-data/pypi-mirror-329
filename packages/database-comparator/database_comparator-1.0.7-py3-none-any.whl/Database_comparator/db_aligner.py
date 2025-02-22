import pandas as pd
from .config_class import cfg
import multiprocessing as mp
import numpy as np
from joblib import Parallel, delayed  # Efficient parallel processing


class Aligner:
    """
    The Aligner class provides methods for performing sequence alignments using the Smith-Waterman algorithm.
    It allows for single-core and multi-core parallel processing for aligning sequences from the input DataFrame
    with sequences from databases.
    """
    def __init__(self, config: cfg) -> None:
        self.config = config
        self.query_sequences = np.array(
            self.config.input_df[self.config.input_file_info["sequence_column_name"]].tolist(), dtype=object
        )
        self.data_df = None  # Placeholder for the loaded database DataFrame
        self.original_indices = self.config.input_df.index.values  # Store original indices to preserve mapping


        self.config.logger.info("Aligner class initialized.")

    def aligner_search_in_single_database(self, database_index: int, parallel=False) -> None:
        """
        Perform Smith-Waterman algorithm-based match search in a single database.

        """
        self.config.logger.info(f"Performing alignment search in database {database_index}.")
        if parallel:
            self.config.logger.info("Switching to multiprocessing mode.")
            self.aligner_search_in_single_database_MULTIPROCESSING(database_index=database_index)
            return

        self.data_df = self.config.load_database(database_index=database_index, engine="python")
        data_sequences = np.array(self.data_df[self.config.data_info[database_index]["sequence_column_name"]], dtype=object)

        valid_queries = self.query_sequences[self.query_sequences != "*"]
        for i, input_seq in enumerate(valid_queries):
            matches = np.where([self.align_sequences(input_seq, seq) for seq in data_sequences])[0]
            for j in matches:
                self.config.insert_match_to_input_df(
                    data_df=self.data_df,
                    database_index=database_index,
                    input_sequence_index=self.original_indices[i],
                    output_sequence_index=j
                )

        self.config.fill_Nans(database_index)
        self.config.logger.info(f"Alignment search in database {database_index} completed.")


    def aligner_search_in_all_databases(self, parallel=False) -> None:
        """
        Perform Smith-Waterman algorithm-based match search in all databases.
        """
        self.config.reset_before_analysis()
        self.config.logger.info("Performing alignment search in all databases.")
        for db_index in range(len(self.config.data_info)):
            self.aligner_search_in_single_database(database_index=db_index, parallel=parallel)

    def aligner_search_in_single_database_MULTIPROCESSING(self, database_index: int) -> None:
        """
        Perform Smith-Waterman algorithm-based match search in a single database using multiprocessing.
        """

        self.config.logger.info(f"Performing alignment search in database {database_index} using multiprocessing.")
        self.data_df = self.config.load_database(database_index=database_index, engine="python")
        data_sequences = np.array(self.data_df[self.config.data_info[database_index]["sequence_column_name"]], dtype=object)

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

        self.config.logger.info(f"Alignment search in database {database_index} completed.")

    def aligner_search_in_all_databases_MULTIPROCESSING(self) -> None:
        """
        Perform Smith-Waterman algorithm-based match search in all databases using multiprocessing.
        """
        self.config.reset_before_analysis()
        self.config.logger.info("Performing alignment search in all databases using multiprocessing.")
        for i in range(len(self.config.data_info)):
            self.aligner_search_in_single_database_MULTIPROCESSING(database_index=i)

    def process_chunk(self, query_chunk, original_indices, data_sequences, database_index):
        """
        Processes a chunk of query sequences in parallel, ensuring original sequence indices are preserved.
        """
        result = []
        valid_indices = [i for i, seq in enumerate(query_chunk) if "*" not in seq]

        for i in valid_indices:
            query_seq = query_chunk[i]
            matches = np.where([self.align_sequences(query_seq, seq) for seq in data_sequences])[0]
            result.extend([(original_indices[i], j) for j in matches])

        return result

    def align_sequences(self, seqA: str, seqB: str) -> bool:
        """
        Align two sequences and determine whether they match.
        """
        try: score: float = self.config.aligner.score(seqA, seqB)
        except:
            self.config.logger.error(f"Error aligning sequences {seqA} and {seqB}.")
            raise ValueError("Error aligning sequences.")
        max_score: float = (
            max(self.config.aligner.score(seqA, seqA), self.config.aligner.score(seqB, seqB))
            if self.config.aligner.substitution_matrix is not None
            else max(len(seqA), len(seqB))
        )
        return score / max_score >= self.config.tolerance
