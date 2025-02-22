from .db_exact_match import ExactMatch
from .db_aligner import Aligner
from .db_blast import Blast
from .config_class import cfg
from .db_fast_hamming import FastHammingDistance
from .db_hamming import hamming_distance

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from typing import Literal


class DB_comparator:
    """
    The DB_comparator class is responsible for comparing and analyzing databases using various methods.

    It utilizes the provided configuration to perform exact matching, sequence alignment, BLAST searches,
    and calculates Hamming distances between sequences. The class allows for exporting the results to
    different file formats, such as Excel, CSV, and Markdown.
    """
    def __init__(self, config_file, show_log_in_console: bool = False, log_write_append: Literal["w", "a"] = "w") -> None:
        """
        Initialize the DB_comparator class to compare databases based on the provided configuration.

        Args:
            config_file (str): Path to the configuration file.
        Note:
            This constructor initializes various database comparison components based on the
            configuration settings and provides the ability to perform exact matching, alignment,
            and BLAST-based comparisons.
        """

        self.config = cfg(config_file, show_log_in_console=show_log_in_console, log_write_append = log_write_append) # ✅
        self.exact_match = ExactMatch(self.config)  # ✅ 
        self.aligner = Aligner(self.config)   # ✅ 
        self.blast = Blast(self.config)  # ✅ 
        self.hamming_distances = hamming_distance(self.config)  # Deprecated - use fast_hamming_distances instead (✅)
        self.fast_hamming_distances = FastHammingDistance(self.config)  # ✅ 
        # Place for new modules...
        # self.new_module = new_module.NewModule(self.config)
        # TODO: Add fuzzy matching module (e.g., Levenshtein distance)

        self.config.logger.info("All components were successfully initialized.".upper())
            
    def __str__(self) -> str:
        return str(self.config)
    
    def __del__(self):
        self.config.logger.info("DB_comparator class was successfully deleted.".upper())

    def export_data_frame(self, output_file: str="Results_DefaultDbCompareOutputName.xlsx", data_format: Literal["xlsx", "csv", "tsv", "md"] = "xlsx",  control_cell_size: bool = True):
        """
        Export the data frame to a file in the specified format.

        Args:
            output_file (str): Name of the target file for exporting the data frame.
            data_format (str): The data format to which you want to convert the data frame (e.g., "xlsx", "csv", "tsv", "md").
            control (bool): Flag to control the data format and handle long cells.

        Note:
            This method allows for exporting the data frame to a file in various formats (Excel, CSV, Markdown, TSV).
            It can also handle cases where the data frame contains cells with excessive string lengths.
        """
        excel_max_cell_string_len: int = 32767 - 17

        if control_cell_size:
            longest_cell_string = self.config.input_df.applymap(lambda x: len(str(x)) > excel_max_cell_string_len)
            if longest_cell_string.any().any() and data_format == "xlsx":
                self.config.logger.warning("The dataframe has a cell that cannot be saved to an .xlsx file. The dataframe will be also exported as backup_save_ExcelCellLengthError.csv")
                self.config.input_df.to_csv("backup_save_ExcelCellLengthError.csv")

        if data_format == "xlsx":
            try:
                self.config.input_df.to_excel(output_file, index=False)
                self.config.logger.info(f"Data frame was successfully exported to {output_file}.")
            except Exception as e:
                self.config.input_df.to_csv("Backup_save_EXCEPCTION_WHILE_EXPORTING.csv", index=False)
                self.config.logger.error(f"Exception while exporting to Excel: {e}. Backup file was created.")
                raise(f"Exception while exporting to Excel: {e}. Backup file was created.")

        elif data_format == "csv":
            try:
                self.config.input_df.to_csv(output_file, index=False)
                self.config.logger.info(f"Data frame was successfully exported to {output_file}.")
            except Exception as e:
                self.config.logger.error(f"Exception while exporting to CSV: {e}. Backup cannot be created.")
                raise(f"Exception while exporting to CSV: {e}. Backup cannot be created.")
        

        elif data_format == "tsv":
            try:
                self.config.input_df.to_csv(output_file, sep="\t", index=False)
                self.config.logger.info(f"Data frame was successfully exported to {output_file}.")
            except Exception as e:
                self.config.input_df.to_csv("Backup_save_EXCEPCTION_WHILE_EXPORTING.csv", index=False)
                self.config.logger.error(f"Exception while exporting to TSV: {e}. Backup file was created.")
                raise(f"Exception while exporting to TSV: {e}. Backup file was created.")
            
        elif data_format == "md":
            try:
                self.config.input_df.to_markdown(output_file, index=False)
                self.config.logger.info(f"Data frame was successfully exported to {output_file}.")
            except Exception as e:
                self.config.input_df.to_csv("Backup_save_EXCEPCTION_WHILE_EXPORTING.csv", index=False)
                self.config.logger.error(f"Exception while exporting to Markdown: {e}. Backup file was created.")
                raise(f"Exception while exporting to Markdown: {e}. Backup file was created.")
        else:
            self.config.logger.error("Unknown error while exporting the data frame. Please check the provided data format. Exporting to Backup_save_EXCEPCTION_WHILE_EXPORTING.csv")
            self.config.input_df.to_csv("Backup_save_EXCEPCTION_WHILE_EXPORTING.csv", index=False)

        

