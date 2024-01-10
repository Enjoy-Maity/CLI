# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/CLI_Automation/Main_application/temp_Main_Gui.py'],
    pathex=['C:/CLI_Automation/Main_application/', 'C:/CLI_Automation/Main_application/GUI/', 'C:/CLI_Automation/Main_application/Nokia/', 'C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Running_Config_Checks/', 'C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Template_Checks/'],
    binaries=[],
    datas=[('C:/CLI_Automation/Main_application/__init__.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/CLI_preparation.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/Custom_Exception.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/CustomThread.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/Database_manager.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/file_lines_handler.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/MessageBox.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/requirements.txt', 'Main_application/'), ('C:/CLI_Automation/Main_application/Running_Config_Checks.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/Section_splitter.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/setup.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/Sheet_creater.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/temp_Main_Gui.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/Template_checks.py', 'Main_application/'), ('C:/CLI_Automation/Main_application/GUI/__init__.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/app_main_application_first_window.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/app_Main_Window.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/app_new_session_surity_check.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/app_start_dialog.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/app_start_dialog_box.ui', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/Application_GUI.qrc', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/Application_GUI_rc.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/cicso-systems-seeklogo.com.png', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/database_model.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/drop-downarrow.png', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/Ericsson-1.png', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/ericsson-blue-icon-logo.ico', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/huawei-1.png', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/Main_Application.ui', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/main_application_first_window.ui', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/new_session_surity_check.ui', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/nokia-2023-seeklogo.com.png', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/temp_splash_screen.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/ui_app_start_dialog_box.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/ui_Main_Application.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/ui_main_application_first_window.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/ui_new_session_surity_check.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/ui_splash_screen.py', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/GUI/wp3610575-automation-wallpapers-1080x675-copy.png', 'Main_application/GUI/'), ('C:/CLI_Automation/Main_application/Nokia/__init__.py', 'Main_application/Nokia/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Running_Config_Checks.py', 'Main_application/Nokia/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Template_Checks.py', 'Main_application/Nokia/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Running_Config_Checks/__init__.py', 'Main_application/Nokia/Nokia_Section_Running_Config_Checks/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Running_Config_Checks/VPLS_1_nc.py', 'Main_application/Nokia/Nokia_Section_Running_Config_Checks/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Running_Config_Checks/VPLS_2_nc.py', 'Main_application/Nokia/Nokia_Section_Running_Config_Checks/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Template_Checks/__init__.py', 'Main_application/Nokia/Nokia_Section_Template_Checks/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Template_Checks/VPLS_1_tc.py', 'Main_application/Nokia/Nokia_Section_Template_Checks/'), ('C:/CLI_Automation/Main_application/Nokia/Nokia_Section_Template_Checks/VPLS_2_tc.py', 'Main_application/Nokia/Nokia_Section_Template_Checks/')],
    hiddenimports=['jinja2', 'tabulate', 'win32timezone'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CLI Automation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\CLI_Automation\\Main_application\\GUI\\ericsson-blue-icon-logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CLI Automation',
)
