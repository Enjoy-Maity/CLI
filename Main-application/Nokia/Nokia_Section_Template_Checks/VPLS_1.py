import pandas as pd
import logging

log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
Path(log_file_path).mkdir(parents=True,exist_ok=True)

log_file = os.path.join(log_file_path,"Template_checks.log")

logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({os.path.basename(os.path.dirname(__file__))}/{'%(module)s'}): {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding= "UTF-8",
                        level=logging.DEBUG)

def main_func(dataframe : pd.DataFrame, ip_node: str):
    logging.debug(f"Created the empty dictionary for returning as result for IP Node: -{ip_node}")
    
    result_dictionary           = {}
    df                          = dataframe.fillna("TempNA")
    logging.debug(f"Created a copy of dataframe passed for node_ip({ip_node}):-\n{df.to_markdown()}")
    
    df_add                      = df[df['Action'] == 'A:Add']
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Add' for node_ip({ip_node}):-\n{df_add.to_markdown()}")
    
    df_delete_modify            = df[df['Action'].isin(['A:Delete','A:Modify'])]
    logging.debug(f"Created the filtered copy of the Dataframe for Action 'A:Modify/A:Delete' for node_ip({ip_node}):-\n{df_delete_modify.to_markdown()}")

    logging.debug("")
    reason = ''
    i = 0
    while(i < len(df)):
        if(df.iloc[i,'VPLS ID'] == "TempNA"):
            reason = "Blank VPLS ID"
            
            if(not reason in df.keys()):
                result_dictionary[reason] = []
                result_dictionary[reason].append(df.iloc[i,'S.No.'])
            
            else:
                result_dictionary[reason].append(df.iloc[i,'S.No.'])
        i+=1
    