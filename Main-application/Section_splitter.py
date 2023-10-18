import pandas as pd
def section_splitter(**kwargs):
    dataframe = kwargs['dataframe']
    string_to_be_found = "#Secti0n_MPBN"
    dataframe = dataframe.fillna("TempNA")
    section_dictionary = {}