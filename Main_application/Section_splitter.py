import pandas as pd
import numpy as np
import logging
from pathlib import Path
import os
import traceback
from tkinter import messagebox

def section_splitter(dataframe,method_called):
    # dataframe = kwargs['dataframe']
    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True,exist_ok=True)

    if(method_called == 'Template_checks'):
        log_file = os.path.join(log_file_path,"Template_checks.log")
    if(method_called == 'Node_checks'):
        log_file = os.path.join(log_file_path,"Node_checks.log")

    logging.basicConfig(filename=log_file,
                             filemode="a",
                             format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
                             datefmt='%d-%b-%Y %I:%M:%S %p',
                             encoding= "UTF-8",
                             level=logging.DEBUG)
    try:
        string_to_be_found = "#Secti0n_MPBN"
        # dataframe = dataframe.fillna("TempNA")
        dataframe = dataframe.where(~dataframe.isna(),"TempNA")
        section_dictionary = {}
        
        logging.debug(f"Starting splitting of the node sheet")
        i = 0
        while(i < len(dataframe)):
            if(str(dataframe.iloc[i,0]).strip().__contains__(string_to_be_found)):
                section = dataframe.iloc[i,0].split(string_to_be_found)[0]
                unrefind_columns = dataframe.loc[i+1].tolist()
                columns = []

                # Getting required columns for the section dataframe creation.
                j = 0
                while(j < len(unrefind_columns)):
                    if(unrefind_columns[j].strip() == "TempNA"):
                        break
                    else:
                        columns.append(unrefind_columns[j].strip())
                    j+=1
                
                j = i+2
                dictionary_for_columns = {}

                # Creating an empty list for all the column data to be entered
                k = 0
                while(k < len(columns)):
                    dictionary_for_columns[columns[k]] = []
                    k+=1

                while(j<len(dataframe)):
                    # If either we have reached the last row of the dataframe or encountered another row with special section string
                    # we are breaking the loop
                    if(((j+2) < len(dataframe)) and (str(dataframe.iloc[j+2,0]).strip().__contains__(string_to_be_found))):
                        break

                    else:
                        # Entering the data for the corresponding row and column in the column list at that particular index
                        # corresponding to the row number
                        k = 0
                        while(k<len(columns)):
                            dictionary_for_columns[columns[k]].append(dataframe.iloc[j,k])
                            k+=1
                    j+=1
                
                i=j+2

                # Creating the section df and assigning it 
                section_dictionary[section] = pd.DataFrame(dictionary_for_columns,columns=columns)
                section_dictionary[section].drop_duplicates(keep = "first", inplace = True)
                section_dictionary[section].replace("TempNA",np.nan,inplace=True)
                section_dictionary[section].dropna(how="all",inplace=True)
                section_dictionary[section].reset_index(drop = True,inplace = True)
            
            else:
                i+=1
        
        logging.debug("Checking for sections with empty dataframes")
        sections = list(section_dictionary.keys())
        i = 0
        while(i<len(sections)):
            if((len(section_dictionary[sections[i]]) == 0)):
                del section_dictionary[sections[i]]
            i+=1
        
        return section_dictionary
    
    except Exception as e:
        logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
        messagebox.showerror("Exception Occurred!",e)