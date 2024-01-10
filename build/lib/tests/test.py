# import pytest
import sys
import os
import time
import pandas as pd
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),"Main-application"))

def testone():
    path = r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Switch_1 traditional_backup.txt"
    with open(path, "r") as f:
        lines = f.readlines()
        
    from file_lines_handler import File_lines_handler
    path_for_excel = r"C:\Users\emaienj\Downloads\VPLS_CLI_Design_Documents\VPLS_CLI_Design_Documents\Nokia_Input.xlsx"
    excel = pd.ExcelFile(path_or_buffer=path_for_excel,
                         engine='openpyxl')
    df = pd.read_excel(excel,"172.31.72.93")
    # df.fillna("TempNA",inplace=True)
    # print(df.to_markdown())
    filtered_list = File_lines_handler().file_lines_starter_filter(file_lines_list=lines,
                                                                   start_word="vpls")
    df.dropna(subset=["VPLS ID"],inplace=True)
    start = time.time()
    result = []
    i = 0
    while(i < len(df)):
        selected_vpls_id = int(df.iloc[i,df.columns.get_loc("VPLS ID")])
        f = False
        j = 0
        while(j < len(filtered_list)):
            if(filtered_list[j].startswith(f"vpls {selected_vpls_id} ")):
                result.append(f"{selected_vpls_id}: Found")
                f = True
                break
            j+=1
        
        if(not f):
            result.append(f"{selected_vpls_id}: Not Found")
            
        i+=1
    end =time.time()
    print(end-start)
    print(result)
