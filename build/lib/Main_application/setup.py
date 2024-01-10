import sys
from setuptools import setup, find_packages

if sys.platform == 'win32':
    base = 'Win32GUI'
setup(name="CLI_Automation_Main_Application",
      version='1.0.0a1',
      packages=find_packages(),
      description="CLI Automation",
      long_description="Automation Tool for CLI Generation",
      author="Enjoy Maity",
      author_email="enjoy.maity@ericsson.com",
      scripts=['temp_Main_GUI'],
      py_modules=['temp_Main_GUI',
                  'GUI.app_Main_Window',
                  'GUI.app_main_application_first_window',
                  'GUI.app_new_session_surity_check',
                  'GUI.app_start_dialog',
                  'GUI.Application_GUI_rc',
                  'GUI.database_model',
                  'GUI.temp_splash_screen',
                  'GUI.ui_app_start_dialog_box',
                  'GUI.ui_Main_Application',
                  'GUI.ui_main_application_first_window',
                  'GUI.ui_new_session_surity_check'
                  'Template_checks',
                  'Sheet_Creater',
                  'MessageBox',
                  'Database_manager',
                  'CustomThread',
                  'file_lines_handler',
                  'CLI_preparation',
                  'Section_splitter',
                  'Running_Config_Checks',
                  'Custom_Exception',
                  'Nokia.Nokia_Running_Config_Checks',
                  'Nokia.Nokia_Template_Checks',
                  'Nokia.Nokia_Section_Template_Checks.VPLS_1_tc',
                  'Nokia.Nokia_Section_Template_Checks.VPLS_2_tc',
                  'Nokia.Nokia_Section_Running_Config_Checks.VPLS_1_nc',
                  'Nokia.Nokia_Section_Running_Config_Checks.VPLS_2_nc'],
      package_dir={
          'Main_application': '.\\',
          'GUI': 'GUI\\',
          'Nokia': 'Nokia\\',
          'Nokia_Section_Running_Config_Checks': 'Nokia\\Nokia_Section_Running_Config_Checks',
          'Nokia_Section_Template_Checks': 'Nokia\\Nokia_Section_Template_Checks'
      }
      )
