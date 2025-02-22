import pandas as pd

from .config_class import cfg
import numpy as np



class hamming_distance:
    """
    The hamming_distance class handles the computation and analysis of Hamming distances
    between sequences in the input data and sequences in different databases.

    It precomputes and stores Hamming distance matrices for each database, enabling efficient
    comparisons. The class can find Hamming distances for a single database or for all databases
    and can optionally analyze and insert matching results into the input DataFrame using the
    configuration settings.
    """
    def __init__(self, config: cfg) -> None:
        """
        Initialize the hamming_distance class with a configuration.

        Args:
            config (cfg): An instance of the configuration class.

        Note:
            This constructor initializes the hamming_distance class with the provided configuration
            and precomputes data structures to store Hamming distance matrices for databases.
        """
        self.config = config
        self.hamming_matrices_for_all_databases = [None for _ in range(len(self.config.data_info))]
        self.query_sequences = (self.config.input_df[self.config.input_file_info["sequence_column_name"]]).tolist()


        self.config.logger.info("Hamming distance class initialized.")
        self.config.logger.warning("Hamming distance class is deprecated and will be removed in future versions. Use the FastHammingDistance class instead. No logging will be provided for this class.")
    # ------------------------------------Hamming distance--------------------------------------------
    def analyze_all_hamming_matrices(self) -> pd.DataFrame:
        """
        Analyze Hamming distance matrices for all databases.

        Note:
            This method iterates over all databases and analyzes their respective Hamming distance matrices.
        """
        self.config.reset_before_analysis()
        for i in range(len(self.hamming_matrices_for_all_databases)):
            if self.hamming_matrices_for_all_databases[i] is None:
                return
            
            data_df = self.config.load_database(database_index=i, engine="python")

            self.analyze_single_hamming_matrix(data_df=data_df, database_index=i)

        return self.config.input_df.copy(deep=True)
    def analyze_single_hamming_matrix(self, data_df: pd.DataFrame, database_index: int):
        """
        Analyze a single Hamming distance matrix for a specific database.

        Args:
            data_df (pd.DataFrame): DataFrame containing the data from the database.
            database_index (int): Index of the database being analyzed.

        Note:
            This method analyzes a Hamming distance matrix for a specific database and inserts matching
            results into the input DataFrame using the configuration settings.
        """

        if self.hamming_matrices_for_all_databases[database_index] is None:
            return

        row_indices, col_indices = np.where(self.hamming_matrices_for_all_databases[database_index] == self.config.max_hamming_distance)
        indices = list(zip(row_indices, col_indices))

        for ids in indices:
            self.config.insert_match_to_input_df(
                data_df=data_df,
                database_index=database_index,
                input_sequence_index=ids[0],
                output_sequence_index=ids[1]
            )
        self.config.fill_Nans(database_index)

    def find_hamming_distances_for_single_database(self, database_index: int, analyze=True):
        """
        Find Hamming distances for a single database.

        Args:
            database_index (int): Index of the database being analyzed.
            analyze (bool): Flag to control whether to analyze the results.

        Note:
            This method computes Hamming distances between query sequences and sequences from a single
            database and stores the results in the appropriate data structures.
        """
        data_df = self.config.load_database(database_index=database_index, engine="python")
        data_sequences = (data_df[self.config.data_info[database_index]["sequence_column_name"]]).tolist()

        max_length = max(len(max(self.query_sequences, key=len)), len(max(data_sequences, key=len)))

        # Pad sequences to the maximum length with a specific character (e.g., '?')
        query_padded = [seq.ljust(max_length, '?') for seq in self.query_sequences]
        data_padded = [seq.ljust(max_length, '?') for seq in data_sequences]

        # Convert padded sequences to NumPy arrays
        query_array = np.array([list(seq) for seq in query_padded])
        data_array = np.array([list(seq) for seq in data_padded])

        hamming_distance_matrix = (query_array[:, None] != data_array).sum(axis=2)
        self.hamming_matrices_for_all_databases[database_index] = hamming_distance_matrix

        if analyze: self.analyze_single_hamming_matrix(data_df, database_index)

    def find_hamming_distances_for_all_databases(self, analyze=True) -> pd.DataFrame:
        """
        Find Hamming distances for all databases.

        Args:
            analyze (bool): Flag to control whether to analyze the results.

        Note:
            This method computes Hamming distances for all databases and can optionally analyze the results.
        """
        self.hamming_matrices_for_all_databases = [None for _ in range(len(self.config.data_info))]
        for i in range(len(self.config.data_info)):
            self.find_hamming_distances_for_single_database(i, analyze=analyze)
        if analyze:
            return self.config.input_df.copy(deep=True)
