import pandas as pd

class Fasta_maker:
    """
    The Fasta_maker class provides methods for creating FASTA files from data frames and sequences.
    It includes methods for generating FASTA files for all databases and creating a query FASTA file.
    """
    def __init__(self, data_dfs: list[pd.DataFrame], sequence_column_names: list, identifiers: list, result_columns: list, output_file_name="all_databases_fasta_file.fasta", separator="!"):
        """
        Initializes the Fasta_maker object with the provided data and settings.

        Args:
            data_dfs (list[pd.DataFrame]): List of data frames for each database.
            sequence_column_names (list): List of sequence column names for each database.
            identifiers (list): List of identifiers for each database.
            result_columns (list): List of result columns for each database.
            output_file_name (str): Name of the output FASTA file (default is "all_databases_fasta_file.fasta").
            separator (str): Separator to use for combining identifiers (default is "!").
        """
        self.data_dfs = data_dfs
        self.sequence_column_name = sequence_column_names
        self.identifiers = identifiers
        self.result_columns = result_columns
        self.output_file_name = output_file_name
        self.separator = separator

    def __merge_all_identifiers(self, df_index: int, output_sequence_index: int) -> str:
        """
        Merge all identifiers associated with a sequence.

        Args:
            df_index (int): Index of the data frame for the database.
            output_sequence_index (int): Index of the output sequence.

        Returns:
            str: Combined identifiers for the sequence.
        """
        full_identifier = ""
        for identifier_column_name in self.identifiers[df_index]:
            identifier = self.data_dfs[df_index][identifier_column_name][output_sequence_index]
            full_identifier += f"({identifier_column_name}:{identifier})"

        return full_identifier

    @staticmethod
    def __format_as_fasta(index, sequence):
        """
        Format a sequence as FASTA.

        Args:
            index: Index of the sequence.
            sequence: Sequence data.

        Returns:
            str: Formatted FASTA representation of the sequence.
        """
        return f'>seq{index}\n{sequence}'

    def make_file(self):
        """
        Create a FASTA file from the provided data frames and settings.

        Note:
            This method generates a FASTA file that contains sequences from all databases and their associated
            identifiers. It creates the file based on the provided data frames and settings.
        """
        output_fasta_file = open(self.output_file_name, "w")
        for i in range(len(self.data_dfs)):
            self.data_dfs[i].drop_duplicates(inplace=True)
            data_sequences = self.data_dfs[i][self.sequence_column_name[i]]
            for j in range(len(data_sequences)):
                identifier = self.result_columns[i] + self.separator + self.__merge_all_identifiers(i, j)
                output_fasta_file.write(f'>{identifier}\n{data_sequences[j]}\n')
        output_fasta_file.close()

    def make_query(self):
        """
        Create a query FASTA file from the first data frame.

        Note:
            This method generates a query FASTA file based on the sequences in the first data frame. The query file
            is used for conducting searches and alignments.
        """
        fasta_data = [self.__format_as_fasta(index - 1, sequence) for index, sequence in enumerate(self.data_dfs[0][self.sequence_column_name[0]], start=1)]

        with open(self.output_file_name, 'w') as f:
            f.write('\n'.join(fasta_data))
