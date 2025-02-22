import pandas as pd
import pyreadr as pr
import os
import warnings
from pathlib import Path
import numpy as np

import logging
from Bio import Align

from typing import Literal

warnings.simplefilter(action='ignore', category=FutureWarning)

StopCodon = "#"
class cfg:
    """
    Initialize the configuration class for a bioinformatics sequence analysis program.

    Args:
        config_file (str): Path to the configuration file.

    Note:
        This constructor initializes various parameters and loads settings from the
        specified configuration file to customize the behavior of the program.
    """
    def __init__(self, config_file=None, show_log_in_console:bool = False, log_write_append: Literal["w", "a"] = "w") -> None:
        """
        Initialize the configuration class for a bioinformatics sequence analysis program.

        Args:
            config_file (str): Path to the configuration file.

        Note:
            This constructor initializes various parameters and loads settings from the
            specified configuration file to customize the behavior of the program.
        """
        # Logging

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        log_file = "DB_comparator_run.log"
        file_handler = logging.FileHandler(log_file, mode=log_write_append)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Define log format
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(log_format)
        
        
        if show_log_in_console: console_handler.setFormatter(log_format)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        if show_log_in_console: self.logger.addHandler(console_handler)

        self.logger.info("Initializing configuration class.")

        # Paths
        self.input_file_path:str = None
        self.blast_database_path:str = "BLAST_database"
        self.blast_query_files_path:str = "Query_files"

        # Input data_info 
        self.input_file_info:dict = None
        
        # Databases info list
        self.data_info: list = []

        # Report switches
        self.show_report_while_inserting_match_to_input_df: bool = False
        self.show_alignments: bool = False

        # Smith–Waterman algorithm
        self.aligner: Align.PairwiseAligner = Align.PairwiseAligner()
        self.tolerance: float = 0.93

        # Blastp Algorithm
        self.e_value: float = 0.05
        self.blast_database_name: str = "clip_seq_db"
        self.blast_database_full_name: str = self.blast_database_path + "//" + self.blast_database_name
        self.blast_output_name: str = "blastp_output.txt"
        self.blast_default_input_query: str = self.blast_query_files_path + "//QUERY.fasta"

        self.in_blast_database: list = self.data_info
        self.blast_outfmt: str = "6 qseqid sseqid qseq sseq bitscore score"

        # Hamming distance
        self.max_hamming_distance: int = 1

        # Multiprocessing
        self.number_of_processors: int = 1

        # dataframe of input file
        self.repair_input_df: bool = True
        self.input_df: pd.DataFrame = None
        self.separator_of_results_in_input_df = "\n"


        # Config file - supported .txt and .xlsx
        config_file_suffix: str = Path(config_file).suffix

        if config_file_suffix not in [".txt", ".xlsx"]: 
            self.logger.error(f"Unsupported config file format: {config_file_suffix}. Supported formats: .txt, .xlsx")
            raise Exception(f"Unsupported config file format: {config_file_suffix}. Supported formats: .txt, .xlsx")
        
        if config_file_suffix == ".xlsx": self.__load_config_xlsx(config_file)
        else:
            self.logger.warning("Loading configuration from .txt file. Consider using .xlsx for better readability.")
            self.__load_config_txt(config_file)

        # Check if the number of processors is valid
        if self.number_of_processors < 1:
            self.logger.error("Number of processors must be at least 1") 
            raise Exception("Number of processors must be at least 1")
        
        if self.number_of_processors > os.cpu_count(): 
            self.logger.error(f"Number of processors must be at most {os.cpu_count()}")
            raise Exception(f"Number of processors must be at most {os.cpu_count()}")
        
        if self.number_of_processors == os.cpu_count(): 
            self.logger.warning(f"Number of processors is set to maximum: {os.cpu_count()}. This may slow down your computer.")

        self.logger.info("Configuration class initialized.")
        self.__load_input_df()

    def __str__(self) -> str:
        """
        Return a formatted string representation of the configuration settings.
        """
        sections = [
            ("General Configuration", [
                f"Input file path: {self.input_file_path}",
                f"Input file info: {self.input_file_info}",
                f"Separator of results in input df: {self.separator_of_results_in_input_df}"
            ]),
            ("Database Information", [
                f"Data info: {self.data_info}"
            ]),
            ("Alignment Settings", [
                f"Aligner: {self.aligner}",
                f"Tolerance: {self.tolerance}"
            ]),
            ("BLAST Settings", [
                f"E-value: {self.e_value}",
                f"BLAST database name: {self.blast_database_name}",
                f"BLAST output name: {self.blast_output_name}",
                f"BLAST database full name: {self.blast_database_full_name}",
                f"BLAST default input query: {self.blast_default_input_query}",
                f"BLAST output format: {self.blast_outfmt}"
            ]),
            ("Hamming Distance", [
                f"Max hamming distance: {self.max_hamming_distance}"
            ]),
            ("Performance Settings", [
                f"Number of processors: {self.number_of_processors}"
            ]),
            ("Input Data", [
                f"DataFrame: {self.input_df}"
            ])
        ]

        output = []
        for title, items in sections:
            output.append(f"{'-'*50}\n{title}:\n")
            output.extend(items)

        return "\n".join(output)

    def __load_config_txt(self, config_file):
        """
        Load configuration settings from the specified file.

        Args:
            config_file (str): Path to the configuration file.

        Note:
            This method reads and interprets settings from the provided configuration file
            and populates the class properties accordingly.
        """
        if config_file is None:
            print("A configuration file was not provided. Please provide the configuration file and restart the program")
            print("See the documentation for more information: https://pypi.org/project/Database-comparator")

            self.logger.error("Configuration file was not provided.")
            raise Exception("Configuration file was not provided")
        
        file = open(config_file, 'r')
        for line in file:
            line = line.split()
            if len(line) == 0:
                continue
            

            if line[0].upper() == "DB":
                try:
                    data = {
                        "path": line[1],
                        "sequence_column_name": line[2],
                        "results_column": line[1],
                        "identifier_of_seq": "".join(line[3:]).strip('][').split(',')
                    }
                    self.data_info.append(data)
                except: 
                    self.logger.error(f"line: {line}... Database path, sequence column name or results column name is missing. Please check your config file.")
                    raise Exception(f"line: {line}... Database path, sequence column name or results column name is missing. Please check your config file.")

            elif line[0].upper() == "QUERY":
                try:
                    self.input_file_path = line[1]
                    self.input_file_info = {
                        "path": self.input_file_path,
                        "sequence_column_name": line[2],
                        "starting_row": 0
                    }
                except:
                    self.logger.error(f"line: {line}... Input file path or sequence column name is missing. Please check your config file.")
                    raise Exception(f"line: {line}... Input file path or sequence column name is missing. Please check your config file.")
                
            elif line[0].upper() == "SWA_tolerance".upper(): 
                try: self.tolerance = float(line[1])
                except: 
                    self.logger.error(f"line: {line}... Tolerance must be float")
                    raise Exception(f"line: {line}... Tolerance must be float")

            elif line[0].upper() == "SWA_gap_score".upper():
                try: 
                    self.aligner.open_gap_score = float(line[1])
                    self.aligner.extend_gap_score = float(line[1])

                except: 
                    self.logger.error(f"line: {line}... Gap score must be float")   
                    raise Exception(f"line: {line}... Gap score must be float")
                
            elif line[0].upper() == "SWA_mismatch_score".upper():
                try: self.aligner.mismatch_score = float(line[1])
                except: 
                    self.logger.error(f"line: {line}... Mismatch score must be float")
                    raise Exception(f"line: {line}... Mismatch score must be float")

            elif line[0].upper() == "SWA_match_score".upper():
                try: self.aligner.match_score = float(line[1])
                except: 
                    self.logger.error(f"line: {line}... Match score must be float")
                    raise Exception(f"line: {line}... Match score must be float")

            elif line[0].upper() == "BLAST_e_value".upper():
                try: self.e_value = float(line[1])
                except: 
                    self.logger.error(f"line: {line}... E-value must be float")
                    raise Exception(f"line: {line}... E-value must be float")

            elif line[0].upper() == "BLAST_database_name".upper():
                try: self.blast_database_name = line[1]
                except: 
                    self.logger.error(f"line: {line}... BLAST database name must be string")
                    raise Exception(f"line: {line}... BLAST database name must be string")

            elif line[0].upper() == "BLAST_output_name".upper():
                try: self.blast_output_name = line[1]
                except: 
                    self.logger.error(f"line: {line}... BLAST output name must be string")
                    raise Exception(f"line: {line}... BLAST output name must be string")

            elif line[0].upper() == "HD_max_distance".upper():
                try: self.max_hamming_distance = int(line[1])
                except: 
                    self.logger.error(f"line: {line}... Max hamming distance must be integer")
                    raise Exception(f"line: {line}... Max hamming distance must be integer")

            elif line[0].upper() == "number_of_processors".upper():
                try: self.number_of_processors = int(line[1])
                except: 
                    self.logger.error(f"line: {line}... Number of processors must be integer")
                    raise Exception(f"line: {line}... Number of processors must be integer")

            elif line[0].upper() == "SWA_matrix".upper():
                if not line[1] in Align.substitution_matrices.load():
                    err = f"Substitution matrix not found. Substitution matrices: {Align.substitution_matrices.load()}"
                    self.logger.error(err)
                    raise Exception(err) 
                self.aligner.substitution_matrix = Align.substitution_matrices.load(line[1])
            elif line[0].upper() == "SWA_mode".upper():
                if not line[1].lower in ["local", "global"]:
                    err = "Mode not found. Please use only global/local"
                    self.logger.error(err)
                    raise Exception(err)
                self.aligner.mode = line[1].lower()

            elif line[0].upper() == "separator".upper():
                prohibited_characters = [",", ";", ":", "\t", " "]
                if line[1] in prohibited_characters and line[2].upper() != "BRUTEFORCE":
                    err = f"Separator cannot be {line[1]}. Prohibited characters: {prohibited_characters}. If you want to use one of these characters, please use the following format: <SEPARATOR prohibited_char BRUTEFORCE>"
                    self.logger.error(err)
                    raise Exception(err)
                try: 
                    self.separator_of_results_in_input_df = line[1]
                    if  line[1] in prohibited_characters and line[2].upper() == "BRUTEFORCE":
                        print("Bruteforce mode is on. This mode is not recommended for large datasets.")
                except: 
                    self.logger.error(f"line: {line}... Separator not valid")
                    raise Exception(f"line: {line}... Separator not valid")

            elif line[0].upper() == "#".upper():
                pass

            else:
                self.logger.error(f"line: {line}... Error in config file.")
                raise Exception(f"line: {line}... Error in config file.")
        
        file.close()

        self.logger.info("Configuration from txt file loaded successfully.")

    def __load_config_xlsx(self, config_file):
        def transform_dataframe(df):
            df = df.T.reset_index(drop=True)
            df.columns = df.iloc[0]
            df = df.iloc[1:, :].reset_index(drop=True)

            return df


        try:
            df = pd.read_excel(config_file, sheet_name="Query")
            self.logger.info("Query sheet loaded successfully.")
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_file}")
            raise Exception(f"Configuration file not found: {config_file}")
        except Exception as e:
            self.logger.error(f"Error loading Excel file: {e}")
            raise Exception(f"Error loading Excel file: {e}")
        
        

        # -------------- Query --------------
        query_table = df.iloc[0:2].dropna(how="all", axis=1).reset_index(drop=True)
        query_table.columns = query_table.iloc[0]
        query_table = query_table.iloc[1:, 1:]
        query_table = query_table.reset_index(drop=True)

        self.input_file_path = query_table["Path"][0]
        self.input_file_info = {
            "path": self.input_file_path,
            "sequence_column_name": query_table["Sequence_column"][0],
            "starting_row": 0
        }

        # -------------- Databases --------------
        database_table = df.iloc[4:24].dropna(how="all", axis=1).reset_index(drop=True)
        database_table.columns = database_table.iloc[0]
        database_table = database_table.iloc[1:, 1:]
        database_table = database_table.reset_index(drop=True)
        
        for i in range(len(database_table)):
            if pd.isnull(database_table["Path"][i]): break

            identifier_columns_values = database_table.iloc[i, 2:].dropna().tolist()

            data = {
                "path": database_table["Path"][i],
                "sequence_column_name": database_table["Sequence_column"][i],
                "results_column": database_table["Path"][i],
                "identifier_of_seq": identifier_columns_values
            }

            self.data_info.append(data)

        # -------------- Settings --------------
        settings_table = df.iloc[25:27].dropna(how="all", axis=1).reset_index(drop=True)
        settings_table = transform_dataframe(settings_table)

        if not pd.isnull(settings_table["Separator"][0]):     
            self.separator_of_results_in_input_df = settings_table["Separator"][0]
            if self.separator_of_results_in_input_df == "\\n": self.separator_of_results_in_input_df = "\n"
        if not pd.isnull(settings_table["Number_of_processors"][0]): self.number_of_processors = int(settings_table["Number_of_processors"][0])


        # -------------- Aligner --------------

        try:
            Aligner_info = pd.read_excel(config_file, sheet_name="Aligner")
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_file}")
            raise Exception(f"Configuration file not found: {config_file}")
        except Exception as e:
            self.logger.error(f"Error loading Excel file: {e}")
            raise Exception(f"Error loading Excel file: {e}")

        Aligner_info = transform_dataframe(Aligner_info)

        if not pd.isnull(Aligner_info["SWA_tolerance"][0]): self.tolerance = float(Aligner_info["SWA_tolerance"][0])
        if not pd.isnull(Aligner_info["SWA_gap_score"][0]):
            self.aligner.open_gap_score = float(Aligner_info["SWA_gap_score"][0])
            self.aligner.extend_gap_score = float(Aligner_info["SWA_gap_score"][0])

        if not pd.isnull(Aligner_info["SWA_mismatch_score"][0]): self.aligner.mismatch_score = float(Aligner_info["SWA_mismatch_score"][0])
        if not pd.isnull(Aligner_info["SWA_match_score"][0]): self.aligner.match_score = float(Aligner_info["SWA_match_score"][0])

        try:
            if not pd.isnull(Aligner_info["SWA_matrix"][0]): self.aligner.substitution_matrix = Align.substitution_matrices.load(Aligner_info["SWA_matrix"][0])

        except Exception as e:
            err = f"Substitution matrix not found. Substitution matrices: {Align.substitution_matrices.load()}"
            self.logger.error(err)
            raise Exception(err)
        
        if not pd.isnull(Aligner_info["SWA_mode"][0]):
            if not Aligner_info["SWA_mode"][0].lower() in ["local", "global"]:
                err = "Mode not found. Please use only global/local"
                self.logger.error(err)
                raise Exception(err)
            self.aligner.mode = Aligner_info["SWA_mode"][0].lower()


        # -------------- Hamming distance --------------
        try:
            Hamming_info = pd.read_excel(config_file, sheet_name="Hamming_distance")
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_file}")
            raise Exception(f"Configuration file not found: {config_file}")
        except Exception as e:
            self.logger.error(f"Error loading Excel file: {e}")
            raise Exception(f"Error loading Excel file: {e}")
        
        Hamming_info = transform_dataframe(Hamming_info)

        if not pd.isnull(Hamming_info["Max_hamming_distance"][0]): self.max_hamming_distance = int(Hamming_info["Max_hamming_distance"][0])


        # -------------- Blast --------------
        try:
            Blast_info = pd.read_excel(config_file, sheet_name="BLAST")
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_file}")
            raise Exception(f"Configuration file not found: {config_file}")
        except Exception as e:
            self.logger.error(f"Error loading Excel file: {e}")
            raise Exception(f"Error loading Excel file: {e}")
        
        Blast_info = transform_dataframe(Blast_info)

        if not pd.isnull(Blast_info["BLAST_e_value"][0]): self.e_value = float(Blast_info["BLAST_e_value"][0])
        if not pd.isnull(Blast_info["BLAST_database_name"][0]): self.blast_database_name = Blast_info["BLAST_database_name"][0]
        if not pd.isnull(Blast_info["BLAST_output_name"][0]): self.blast_output_name = Blast_info["BLAST_output_name"][0]

        self.logger.info("Configuration from xlsx file loaded successfully.")

    def __load_input_df(self):
        """
        Load input data from a file and prepare it for processing.

        Note:
            This method loads data from the input file, performs data cleaning and
            preprocessing tasks, and stores the resulting DataFrame in the class.
        """
        supported_formats = [".csv", ".tsv" ".xlsx", ".xls", ".RData", ".Rbin", ".RDATA"]
        path = self.input_file_info["path"]
        if Path(path).suffix == ".csv":
            try:
                self.input_df = pd.DataFrame(pd.read_csv(self.input_file_info["path"]))
            except Exception as e:
                self.logger.error(f"Error loading csv file: {e}")
                raise Exception(f"Error loading csv file: {e}")
        elif Path(path).suffix in [".xlsx", ".xls"]:
            try:
                self.input_df = pd.DataFrame(pd.read_excel(self.input_file_info["path"]))
            except Exception as e:
                self.logger.error(f"Error loading Excel file: {e}")
                raise Exception(f"Error loading Excel file: {e}")
        elif Path(path).suffix in [".RData", ".Rbin", ".RDATA"]:
            try:
                data = pr.read_r(path)
                self.input_df = data[os.path.splitext(path)[0]]
            except Exception as e:
                self.logger.error(f"Error loading R file: {e}")
                raise Exception(f"Error loading R file: {e}")
        elif Path(path).suffix == ".tsv":
            try:
                self.input_df =  pd.DataFrame(pd.read_csv(self.input_file_info["path"], sep="\t"))
            except Exception as e:
                self.logger.error(f"Error loading tsv file: {e}")
                raise Exception(f"Error loading tsv file: {e}")
        else:
            self.logger.error(f"File format is not supported. Supported formats: {supported_formats}")
            raise Exception(f"File format is not supported. Supported formats: {supported_formats}")
        
        if self.repair_input_df:
            self.__repair_input_df()

        self.logger.info("Input DataFrame loaded successfully.")

    def reset_before_analysis(self, bruteforce = False):
        """
        Reset the class to default values before running a new analysis.

        Args:
            bruteforce (bool): Whether to use brute force mode (default is False).

        Note:
            This method resets the class to default values before running a new analysis.
        """
        if self.__check_if_input_df_changed():
            print("#"*200)
            print("Resetting dataframes to default values before running a new analysis")
            if bruteforce:
                self.input_df = None
                self.__load_input_df()
                print("Input dataframe was reloaded - BRUTEFORCE mode is on")

            else: self.input_df[[db["results_column"] for db in self.data_info]] = np.nan
                

            print("Reset was successfuly done")
            print("Analysing the data...")
            print("#"*200)

    def __check_if_input_df_changed(self) -> bool:
        """
        Check if the input DataFrame has been changed.

        Returns:
            bool: True if the input DataFrame has been changed, False otherwise.

        Note:
            This method is used to check if the input DataFrame has been changed since
            the last analysis.
        """

        return not all([pd.isnull(self.input_df[self.data_info[i]["results_column"]]).all() for i in range(len(self.data_info))])

    def __repair_input_df(self):
        """
        Perform data cleaning and preprocessing on the input DataFrame.

        Note:
            This method cleans the input data, removing unwanted characters and filtering
            out sequences with stop codons, and ensures that the DataFrame is in a suitable
            format for analysis.
        """
        # deleting string (pre-)filtered from seq column
        self.input_df[self.input_file_info["sequence_column_name"]] = self.input_df[self.input_file_info["sequence_column_name"]].str.replace("(pre-)filtered", "")
        self.input_df[self.input_file_info["sequence_column_name"]] = self.input_df[self.input_file_info["sequence_column_name"]].str.replace(" ", "")
        # deleting sequences with stop codon
        self.input_df = self.input_df[~self.input_df[self.input_file_info["sequence_column_name"]].fillna("").str.contains(StopCodon)]
        self.input_df = self.input_df.reset_index(drop=True)
        self.input_df[self.input_file_info["sequence_column_name"]].fillna(value="********", inplace=True)

        for db in self.data_info:
            self.input_df[db["results_column"]] = np.nan

        self.logger.info("Input DataFrame repaired.")
        
    def fill_Nans(self, database_index: int):
        """
        Fill missing values in the input DataFrame with "False" for a specified database.

        Args:
            database_index (int): Index of the database to fill missing values for.

        Note:
            This method is used to fill missing values in the DataFrame when analyzing
            data from a specific database.
        """
        result_column_name = self.data_info[database_index]["results_column"]
        self.input_df[result_column_name].fillna(value="False", inplace=True)

    @staticmethod
    def merge_all_identifiers(data_df: pd.DataFrame, identifier_column_names: list, output_sequence_index: int) -> str:
        """
        Merge all identifiers for a sequence in the output data.

        Args:
            data_df (pd.DataFrame): The data DataFrame.
            identifier_column_names (list): List of column names containing identifiers.
            output_sequence_index (int): Index of the sequence in the output data.

        Returns:
            str: A merged string of identifiers.

        Note:
            This static method is used to merge multiple identifiers associated with a
            sequence in the output data.
        """
        full_identifier = ""
        for identifier_column_name in identifier_column_names:
            identifier = data_df[identifier_column_name][output_sequence_index]
            full_identifier += f" ({identifier_column_name}: {identifier})"

        return full_identifier
    
    def insert_match_to_input_df(self, data_df: pd.DataFrame, database_index: int, input_sequence_index: int, output_sequence_index: int):
        """
        Insert a match from the output data into the input DataFrame.

        Args:
            data_df (pd.DataFrame): The output data DataFrame.
            database_index (int): Index of the database being analyzed.
            input_sequence_index (int): Index of the sequence in the input DataFrame.
            output_sequence_index (int): Index of the sequence in the output data.

        Note:
            This method is used to insert a matching result from the output data into the
            input DataFrame for further analysis and reporting.
        """
        
        input_df = self.input_df
        identifier_column_names = self.data_info[database_index]["identifier_of_seq"]

        filename, _ = os.path.splitext(self.data_info[database_index]["path"])
        sseq = data_df[self.data_info[database_index]["sequence_column_name"]][output_sequence_index]

        if identifier_column_names is None:
            identifier = os.path.basename(filename)

        else: identifier = self.merge_all_identifiers(data_df=data_df, identifier_column_names=identifier_column_names,output_sequence_index=output_sequence_index)

        identifier = ";".join(set(identifier.split(sep=";")))
        if pd.isnull(input_df.loc[input_sequence_index, self.data_info[database_index]["results_column"]]):
            input_df.loc[input_sequence_index, self.data_info[database_index]["results_column"]] = f"[seq: {sseq}{identifier}]" + self.separator_of_results_in_input_df
        else:
            input_df.loc[input_sequence_index, self.data_info[database_index]["results_column"]] = str(input_df[self.data_info[database_index]["results_column"]][input_sequence_index]) \
                                                                                                        + f"[seq: {sseq}{identifier}]" + self.separator_of_results_in_input_df

        if self.show_report_while_inserting_match_to_input_df:
            input_sequence = input_df[self.input_file_info["sequence_column_name"]][input_sequence_index]
            output_sequence = data_df[self.data_info[database_index]["sequence_column_name"]][output_sequence_index]
            print(f"Match found in {os.path.basename(filename)}", flush=True)
            print(f"inp sequence: {input_sequence}", flush=True)
            print(f"out sequence: {output_sequence}", flush=True)
            print(f"Identifier: {identifier}", flush=True)
            print("-"*200)
            
    def load_datafiles_names_from_stored_path(self, database_index: int) -> list:
        """
        Load the names of data files from the specified database path.

        Args:
            database_index (int): Index of the database being analyzed.

        Returns:
            list: A list of file names from the specified database path.

        Note:
            This method is used to retrieve file names from the database path for further
            analysis.
        """
        front = []
        path_to_data = self.data_info[database_index]["path"]
        if os.path.isdir(path_to_data):
            for file in os.listdir(path_to_data):
                front.append(os.path.join(path_to_data, file))
        else:
            front.append(path_to_data)
        return front

    def find_database_index(self, filename: str) -> int:
        """
        Find the index of a database based on a filename.

        Args:
            filename (str): Name of the file to search for.

        Returns:
            int: Index of the database (if found), or -1 if not found.

        Note:
            This method is used to locate a database by searching for a specific filename.
        """
        for i, db in enumerate(self.data_info):
                if filename in db["path"]: return i
        raise ValueError(f"Database file '{filename}' not found in config.")

    def load_database(self, database_index = None, engine=None) -> pd.DataFrame:

        if database_index is None: raise Exception("Database index needs to be specified")
        if database_index >= len(self.data_info): raise Exception(f"Database index out of range. Max index: {len(self.data_info) - 1}")
        
        path = self.data_info[database_index]["path"]
        suffix = Path(path).suffix
        supported_formats = [".csv", ".tsv" ".xlsx", ".xls", ".RData", ".Rbin", ".RDATA"]

        columns = self.data_info[database_index]["identifier_of_seq"] + [self.data_info[database_index]["sequence_column_name"]]
        self.logger.info(f"Loading database: {os.path.basename(path)}, index: {database_index}")

        if suffix == ".csv":
            try:
                db = pd.DataFrame(pd.read_csv(path, engine=engine, usecols=columns, dtype=str))
            except Exception as e:
                self.logger.error(f"Error loading csv file: {e}")
                raise Exception(f"Error loading csv file: {e}")

        elif suffix in [".xlsx", ".xls"]:
            try:
                db = pd.DataFrame(pd.read_excel(path, engine=engine, usecols=columns, dtype=str))
            except Exception as e:
                self.logger.error(f"Error loading Excel file: {e}")
                raise Exception(f"Error loading Excel file: {e}")
            
        elif suffix == ".tsv":
            try:
                db = pd.DataFrame(pd.read_csv(path, sep="\t", engine=engine, usecols=columns, dtype=str))
            except Exception as e:
                self.logger.error(f"Error loading tsv file: {e}")
                raise Exception(f"Error loading tsv file: {e}")
            
        elif suffix in [".RData", ".Rbin", ".RDATA"]:
            try:
                data = pr.read_r(path, use_objects=columns)
                db = data[os.path.splitext(path)[0]]
            except Exception as e:
                self.logger.error(f"Error loading R file: {e}")
                raise Exception(f"Error loading R file: {e}")
        
        else:
            err = f"File format is not supported for database. Supported formats: {supported_formats}"
            self.logger.error(err)
            raise Exception(err)
        
        self.logger.info(f"Database loaded successfully: {os.path.basename(path)}")
        return db
