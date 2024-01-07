import pandas
import sys
from PySide6.QtCore import Qt, QCoreApplication
from GUI.database_model import DataModel
from PySide6.QtWidgets import QWidget, QApplication
from GUI.ui_Main_Application import Ui_Main_Application_Window


class App_Main_Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.table_model = None
        self.cli_preparation_status_label_color = None
        self.filtered_dataframe = None
        self.main_window_ui = Ui_Main_Application_Window()

        self.main_window_ui.setupUi(self)

        self.vendor_selected = ''
        self.task_dictionary = {'Template Checks': self.main_window_ui.template_checks_label,
                                'Running Config Pre Checks': self.main_window_ui.running_config_pre_checks_label,
                                'CLI Preparation': self.main_window_ui.cli_preparation_status_label,
                                'Running Config Post Checks': self.main_window_ui.running_config_post_checks_label}

        self.task_color_dictionary = {'Template Checks': self.main_window_ui.template_checks_label_color,
                                      'Running Config Pre Checks': self.main_window_ui.running_config_pre_checks_label_color,
                                      'CLI Preparation': self.main_window_ui.cli_preparation_status_label_color,
                                      'Running Config Post Checks': self.main_window_ui.running_config_post_checks_label_color}

        self.color_dictionary = {'Unsuccessful': 'rgb(255,0,0)',
                                 'Successful': 'rgb(0,255,0)',
                                 'In Progress': 'rgb(255,255,255)'}

        self.data = pandas.DataFrame()

    def current_vendor(self, _) -> str:
        """Gets Selected Vendor by the User

        Args:
            _ (_type_): _description_ : Empty argument for getting the connection signal
        """
        self.vendor_selected = self.main_window_ui.vendor_details_selection_combobox.currentText()
        return self.vendor_selected

    def combobox_clearer(self) -> None:
        """Clears the combobox
        """
        self.main_window_ui.vendor_details_selection_combobox.clear()

    def combobox_data_items_adder(self, vendor_list: list) -> None:
        """Adds the Items in the combobox

        Args:
            vendor_list (list): _description_ : list of items to be added in the combobox
        """
        self.main_window_ui.vendor_details_selection_combobox.addItems(vendor_list)

    def status_label_updater_from_table(self, data: pandas.DataFrame, vendor: str) -> None:
        """Updates the label of the tasks based on the data from table in \'Existing Session\'

        Args:
            data (pandas.DataFrame): _description_ : DataFrame containing the data of the existing session
            vendor (str): _description_ : Contains the vendor details
        """

        # Running the current_vendor method to get the latest selected vendor
        self.current_vendor("")

        self.filtered_dataframe = data[data["Vendor"] == vendor]

        if len((self.filtered_dataframe.iloc[
            0, self.filtered_dataframe.columns.get_loc('Template_Checks')]).strip()) > 0:
            self.main_window_ui.template_checks_label_text.setText(QCoreApplication.translate("Main_Application_Window",
                                                                                              self.filtered_dataframe.iloc[
                                                                                                  0, self.filtered_dataframe.columns.get_loc(
                                                                                                      'Template_Checks')],
                                                                                              None))

        if len((self.filtered_dataframe.iloc[
            0, self.filtered_dataframe.columns.get_loc('Running_Config_Pre_Checks')]).strip()) > 0:
            self.main_window_ui.running_config_pre_checks_label_text.setText(
                QCoreApplication.translate("Main_Application_Window", self.filtered_dataframe.iloc[
                    0, self.filtered_dataframe.columns.get_loc('Running_Config_Pre_Checks')], None))

        if len((self.filtered_dataframe.iloc[
            0, self.filtered_dataframe.columns.get_loc('CLI_Preparation')]).strip()) > 0:
            self.main_window_ui.cli_preparation_status_label.setText(
                QCoreApplication.translate("Main_Application_Window", self.filtered_dataframe.iloc[
                    0, self.filtered_dataframe.columns.get_loc('CLI_Preparation')], None))

        if len((self.filtered_dataframe.iloc[
            0, self.filtered_dataframe.columns.get_loc('Running_Config_Post_Checks')]).strip()) > 0:
            self.main_window_ui.running_config_post_checks_label_text.setText(
                QCoreApplication.translate("Main_Application_Window", self.filtered_dataframe.iloc[
                    0, self.filtered_dataframe.columns.get_loc('Running_Config_Post_Checks')], None))

    def task_method_status_updater(self, task: str, status: str) -> None:

        self.task_dictionary[task].setText(QCoreApplication.translate("Main_Application_Window", status, None))

        if task == 'Sheet Creater':
            self.main_window_ui.sheet_creater_task_status_label.setStyleSheet(u"#sheet_creater_task_status_label{\n"
                                                                              "text-align:center;\n"
                                                                              f"color:{self.color_dictionary[status]};\n"
                                                                              "}")

        if task == 'Template Checks':
            self.main_window_ui.template_checks_label.setStyleSheet(u"#template_checks_label{\n"
                                                                    f"color: {self.color_dictionary[status]};\n"
                                                                    "}")

        if task == 'Running Config Pre Checks':
            self.main_window_ui.running_config_pre_checks_label.setStyleSheet(u"#running_config_pre_checks_label{\n"
                                                                              f"color: {self.color_dictionary[status]}; \n"
                                                                              "}")

        if task == 'CLI Preparation':
            self.main_window_ui.cli_preparation_status_label.setStyleSheet(u"#cli_preparation_status_label{ \n"
                                                                           f"color: {self.cli_preparation_status_label_color}; \n"
                                                                           "}")

    def table_view_data_loader(self, data: pandas.DataFrame|None) -> None:
        if isinstance(data, pandas.DataFrame):
            self.data = data

        self.table_model = DataModel(self.data)
        self.main_window_ui.task_database_tableview.setModel(self.table_model)

        # self.main_window_ui.task_database_tableview.resizeRowsToContents()
        # self.main_window_ui.task_database_tableview.verticalHeader().setStretchLastSection(True)

    def task_buttons_status_label_refresher(self, data: pandas.DataFrame):
        if ((len(self.main_window_ui.vendor_details_selection_combobox.currentText()) > 0) and (
                (self.main_window_ui.vendor_details_selection_combobox.currentText()).strip() != 'Select Vendor')):
            pass
