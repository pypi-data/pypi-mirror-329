import db_compare as db_compare


if __name__ == "__main__":
    db_comp = db_compare.DB_comparator("C:\\Users\\Tomas\\Desktop\\CLIP_database_project\\Database_comparator\\DEFAULT_config_file.xlsx", show_log_in_console=True)
    db_comp.fast_hamming_distances.find_hamming_distances_for_single_database(0, parallel=True)
    #db_comp.exact_match.exact_match_search_in_single_database(0, parallel=True)
    #db_comp.aligner.aligner_search_in_single_database(0, parallel=True)
    #print(db_comp)
    db_comp.export_data_frame()