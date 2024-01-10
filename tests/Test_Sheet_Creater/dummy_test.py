import os
from pathlib import Path
_username = (os.popen(cmd=r'cmd.exe /C "echo %username%"').read()).strip()

_app_data_local_saved_host_details_path = f"C:\\Users\\{_username}\\AppData\\Local\\CLI_Automation\\host_details_file_path.txt"

print(_app_data_local_saved_host_details_path)
print(f"{os.path.exists(_app_data_local_saved_host_details_path)= }")
print(f"{Path(_app_data_local_saved_host_details_path).exists()= }")