import os
import importlib
import sys
import pickle
import logging
from pathlib import Path
import pandas


def test_add_vpls_1(capsys):
    log_file = os.path.join(os.path.dirname(__file__),  "test_log_files.log")
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.close()
        del f
    logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}/{'%(funcName)s'}): [[Line No. - {'%(lineno)d'}]] {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding="UTF-8",
                        level=logging.DEBUG)
    folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))                #gives the location of CLI_Automation
    test_files_folder = os.path.join(folder, "Files_for_testing","Cli_prep_test_files")

    modify_add_test_file = os.path.join(test_files_folder, 'File_1.xlsx')

    sys.path.append(os.path.join(folder, "Main_application"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Template_Checks"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Running_Config_Checks_Post"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Running_Config_Checks"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_CLI_Preparation"))

    section_splitter = importlib.import_module("Main_application.Section_splitter")
    cli_preparation = importlib.import_module("Main_application.CLI_preparation")
    username = os.popen(cmd= r'cmd.exe /C "echo %username%"').read().strip()
    file_to_be_saved = rf"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\NOKIA.pickle"
    host_details_file_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"

    cli_prep_path = os.path.join(test_files_folder, "File_1_file_folder", "dummy")
    # os.mkdir(os.path.dirname(cli_prep_path))
    Path(os.path.dirname(cli_prep_path)).mkdir(parents= True, exist_ok= True)

    with open(host_details_file_path, 'w') as f:
        f.write(cli_prep_path)
        f.close()
    del f

    excel_reader = pandas.ExcelFile(modify_add_test_file, engine='openpyxl')
    sheets = excel_reader.sheet_names

    dictionary = dict()
    i = 0
    while i < len(sheets):
        dictionary[str(sheets[i])] = section_splitter.section_splitter(pandas.read_excel(io= excel_reader,
                                                                        sheet_name= sheets[i],
                                                                        engine= 'openpyxl'),
                                                                        "")
        i += 1

    with open(file= file_to_be_saved, mode= 'wb') as f:
        pickle.dump(obj= dictionary, file= f)
        f.close()

    del f

    excel_reader.close()
    del excel_reader
    logging.info("Starting the test for test_add_vpls_1")
    # assert cli_preparation.main_func(vendor = 'Nokia') == 'Successful'
    output = cli_preparation.main_func(vendor_selected= 'Nokia')
    out, err = capsys.readouterr()
    # print(output)
    # print(out)
    # print(f"{err = }")
    assert output == 'Successful'



def test_delete_vpls_1(capsys):
    log_file = os.path.join(os.path.dirname(__file__),  "test_log_files.log")
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.close()
        del f
    logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}/{'%(funcName)s'}): [[Line No. - {'%(lineno)d'}]] {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding="UTF-8",
                        level=logging.DEBUG)
    folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))                #gives the location of CLI_Automation
    test_files_folder = os.path.join(folder, "Files_for_testing","Cli_prep_test_files")

    modify_delete_test_file = os.path.join(test_files_folder, 'File_2.xlsx')

    sys.path.append(os.path.join(folder, "Main_application"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Template_Checks"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Running_Config_Checks_Post"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Running_Config_Checks"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_CLI_Preparation"))

    section_splitter = importlib.import_module("Main_application.Section_splitter")
    cli_preparation = importlib.import_module("Main_application.CLI_preparation")
    username = os.popen(cmd= r'cmd.exe /C "echo %username%"').read().strip()
    file_to_be_saved = rf"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\NOKIA.pickle"
    host_details_file_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"

    cli_prep_path = os.path.join(test_files_folder, "File_2_file_folder", "dummy")
    # os.mkdir(os.path.dirname(cli_prep_path))
    Path(os.path.dirname(cli_prep_path)).mkdir(parents= True, exist_ok= True)

    with open(host_details_file_path, 'w') as f:
        f.write(cli_prep_path)
        f.close()
    del f

    excel_reader = pandas.ExcelFile(modify_delete_test_file, engine='openpyxl')
    sheets = excel_reader.sheet_names

    dictionary = dict()
    i = 0
    while i < len(sheets):
        dictionary[str(sheets[i])] = section_splitter.section_splitter(pandas.read_excel(io= excel_reader,
                                                                        sheet_name= sheets[i],
                                                                        engine= 'openpyxl'),
                                                                        "")
        i += 1

    with open(file= file_to_be_saved, mode= 'wb') as f:
        pickle.dump(obj= dictionary, file= f)
        f.close()

    del f

    excel_reader.close()
    del excel_reader

    logging.info("Starting the test for test_add_vpls_1")
    # assert cli_preparation.main_func(vendor = 'Nokia') == 'Succesful'
    # print(f'{cli_preparation.main_func(vendor = 'Nokia') =}')
    output = cli_preparation.main_func(vendor_selected= 'Nokia')
    out, err = capsys.readouterr()
    # print(output)
    # print(out)
    # print(f"{err = }")

    assert output == 'Successful'


def test_modify_vpls_1(capsys):
    log_file = os.path.join(os.path.dirname(__file__),  "test_log_files.log")
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.close()
        del f
    logging.basicConfig(filename=log_file,
                        filemode="a",
                        format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}/{'%(funcName)s'}): [[Line No. - {'%(lineno)d'}]] {'%(message)s'}",
                        datefmt='%d-%b-%Y %I:%M:%S %p',
                        encoding="UTF-8",
                        level=logging.DEBUG)
    folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))                #gives the location of CLI_Automation
    test_files_folder = os.path.join(folder, "Files_for_testing","Cli_prep_test_files")

    modify_modify_test_file = os.path.join(test_files_folder, 'File_3.xlsx')

    sys.path.append(os.path.join(folder, "Main_application"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Template_Checks"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Running_Config_Checks_Post"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_Running_Config_Checks"))
    sys.path.append(os.path.join(folder, "Main_application", "Nokia", "Nokia_Section_CLI_Preparation"))

    section_splitter = importlib.import_module("Main_application.Section_splitter")
    cli_preparation = importlib.import_module("Main_application.CLI_preparation")
    username = os.popen(cmd= r'cmd.exe /C "echo %username%"').read().strip()
    file_to_be_saved = rf"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\NOKIA.pickle"
    host_details_file_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"

    cli_prep_path = os.path.join(test_files_folder, "File_3_file_folder", "dummy")
    # os.mkdir(os.path.dirname(cli_prep_path))
    Path(os.path.dirname(cli_prep_path)).mkdir(parents= True, exist_ok= True)

    with open(host_details_file_path, 'w') as f:
        f.write(cli_prep_path)
        f.close()
    del f

    excel_reader = pandas.ExcelFile(modify_modify_test_file, engine='openpyxl')
    sheets = excel_reader.sheet_names

    dictionary = dict()
    i = 0
    while i < len(sheets):
        dictionary[str(sheets[i])] = section_splitter.section_splitter(pandas.read_excel(io= excel_reader,
                                                                        sheet_name= sheets[i],
                                                                        engine= 'openpyxl'),
                                                                        "")
        i += 1

    with open(file= file_to_be_saved, mode= 'wb') as f:
        pickle.dump(obj= dictionary, file= f)
        f.close()

    del f

    excel_reader.close()
    del excel_reader

    logging.info("Starting the test for test_add_vpls_1")
    # assert cli_preparation.main_func(vendor = 'Nokia') == 'Successful'
    # print(f'{cli_preparation.main_func(vendor = 'Nokia') =}')
    output = cli_preparation.main_func(vendor_selected= 'Nokia')
    out, err = capsys.readouterr()
    # print(output)
    # print(out)
    # print(f"{err = }")

    assert output == 'Successful'
