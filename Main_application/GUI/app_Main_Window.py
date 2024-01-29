import logging

import pandas
# import sys
from PySide6.QtCore import QCoreApplication
from GUI.database_model import DataModel
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHeaderView
# from PySide6.QtGui import QBrush, QLinearGradient, QColor, QPalette
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

        if len((self.filtered_dataframe.iloc[0, self.filtered_dataframe.columns.get_loc('Template_Checks')]).strip()) > 0:
            self.main_window_ui.template_checks_label_text.setText(QCoreApplication.translate("Main_Application_Window",
                                                                                              self.filtered_dataframe.iloc[
                                                                                                  0, self.filtered_dataframe.columns.get_loc(
                                                                                                      'Template_Checks')],
                                                                                              None))

        if len((self.filtered_dataframe.iloc[0, self.filtered_dataframe.columns.get_loc('Running_Config_Pre_Checks')]).strip()) > 0:
            self.main_window_ui.running_config_pre_checks_label_text.setText(
                QCoreApplication.translate("Main_Application_Window", self.filtered_dataframe.iloc[
                    0, self.filtered_dataframe.columns.get_loc('Running_Config_Pre_Checks')], None))

        if len((self.filtered_dataframe.iloc[0, self.filtered_dataframe.columns.get_loc('CLI_Preparation')]).strip()) > 0:
            self.main_window_ui.cli_preparation_status_label.setText(
                QCoreApplication.translate("Main_Application_Window", self.filtered_dataframe.iloc[
                    0, self.filtered_dataframe.columns.get_loc('CLI_Preparation')], None))

        if len((self.filtered_dataframe.iloc[0, self.filtered_dataframe.columns.get_loc('Running_Config_Post_Checks')]).strip()) > 0:
            self.main_window_ui.running_config_post_checks_label_text.setText(
                QCoreApplication.translate("Main_Application_Window", self.filtered_dataframe.iloc[
                    0, self.filtered_dataframe.columns.get_loc('Running_Config_Post_Checks')], None))

    def task_method_status_updater(self, task: str, status: str) -> None:
        """Updates the task status of Application Main Window according to the execution status of the task

        :param task: task for which the label needs to be updated
        :param status: status which needs to be updated for the task label for selected vendor
        :returns: None
        """

        if len(status.strip()) > 0:

            if task == 'Sheet Creater':
                self.main_window_ui.sheet_creater_task_status_label.setStyleSheet(u"#sheet_creater_task_status_label{\n"
                                                                                  "text-align:center;\n"
                                                                                  f"color:{self.color_dictionary[status]};\n"
                                                                                  "}")

                logging.debug(
                    f"Setting the cli_preparation label text to {status} and "
                    f"coloring it {self.color_dictionary[status]}"
                )

                self.main_window_ui.sheet_creater_task_status_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

            if task == 'Template Checks':
                self.main_window_ui.template_checks_label.setStyleSheet(
                    u"#template_checks_label{\n"
                    f"color: {self.color_dictionary[status]};\n"
                    "}"
                )

                logging.debug(
                    f"Setting the template_checks label text to {status} and "
                    f"coloring it {self.color_dictionary[status]}"
                )

                self.main_window_ui.template_checks_label.setText(QCoreApplication.translate("Main_Application_Window", status, None))

            if task == 'Running Config Pre Checks':
                self.main_window_ui.running_config_pre_checks_label.setStyleSheet(
                    u"#running_config_pre_checks_label{\n"
                    f"color: {self.color_dictionary[status]}; \n"
                    "}"
                )

                logging.debug(
                    f"Setting the running_config_pre_checks label text to {status} and "
                    f"coloring it {self.color_dictionary[status]}"
                )

                self.main_window_ui.running_config_pre_checks_label.setText(QCoreApplication.translate("Main_Application_Window", status, None))

            if task == 'CLI Preparation':
                self.main_window_ui.cli_preparation_status_label.setStyleSheet(
                    u"#cli_preparation_status_label{ \n"
                    f"color: {self.color_dictionary[status]}; \n"
                    "}"
                )

                logging.debug(
                    f"Setting the cli_preparation label text to {status} and "
                    f"coloring it {self.color_dictionary[status]}"
                )

                self.main_window_ui.cli_preparation_status_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

            if task == 'Running Config Post Checks':
                self.main_window_ui.running_config_post_checks_label.setStyleSheet(
                    u"#running_config_post_checks_label{ \n"
                    f"color: {self.color_dictionary[status]}; \n"
                    "}"
                )

                logging.debug(
                    f"Setting the running_config_post_checks label text to {status} and "
                    f"coloring it {self.color_dictionary[status]}"
                )

                self.main_window_ui.running_config_post_checks_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

        else:
            if task == 'Sheet Creater':
                logging.debug(
                    f"Setting the sheet_creater_task_status_label to {status}"
                )

                self.main_window_ui.sheet_creater_task_status_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

            if task == 'Template Checks':
                logging.debug(
                    f"Setting the template_checks_label to {status}"
                )

                self.main_window_ui.template_checks_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

            if task == 'Running Config Pre Checks':
                logging.debug(
                    f"Setting the running_config_pre_checks_label to {status}"
                )

                self.main_window_ui.running_config_pre_checks_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None
                                               )
                )

            if task == 'CLI Preparation':
                logging.debug(
                    f"Setting the cli_preparation label to {status}"
                )
                self.main_window_ui.cli_preparation_status_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

            if task == 'Running Config Post Checks':
                logging.debug(
                    f"Setting the cli_preparation label to {status}"
                )
                self.main_window_ui.running_config_post_checks_label.setText(
                    QCoreApplication.translate("Main_Application_Window", status, None)
                )

    def table_view_data_loader(self, data: pandas.DataFrame | None) -> None:
        if isinstance(data, pandas.DataFrame):
            self.data = data

        self.table_model = DataModel(self.data)
        self.main_window_ui.task_database_tableview.setModel(self.table_model)
        self.main_window_ui.task_database_tableview.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.main_window_ui.task_database_tableview.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.main_window_ui.task_database_tableview.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        # palette = QPalette()
        # palette.setBrush(QPalette.Window, cr= Qt.BackgroundRole, brush=self.create_gradient_brush())
        # self.main_window_ui.task_database_tableview.horizontalHeader().setBackgroundRole(palette)
        # print(self.main_window_ui.task_database_tableview.horizontalHeader().palette())
        # self.main_window_ui.task_database_tableview.resizeRowsToContents()
        # self.main_window_ui.task_database_tableview.verticalHeader().setStretchLastSection(True)
        self.main_window_ui.task_database_tableview.setStyleSheet(u"#task_database_tableview{\n"
                                                                  "color:black;\n"
                                                                  "	background-color: rgb(190, 190, 190);\n"
                                                                  "	alternate-background-color: rgb(210, 210, 210);\n"
                                                                  "border-radius:8px;\n"
                                                                  "border:1px solid;\n"
                                                                  "gridline-color: rgb(0,0,0);\n"
                                                                  "border:1px solid;\n"
                                                                  "font:10pt 'Ericsson Hilda';\n"
                                                                  "}\n"
                                                                  "QHeaderView::section{\n"
                                                                  "color:black;\n"
                                                                  "background-color:rgb(221, 211, 255);\n"
                                                                  "border: 1px solid;\n"
                                                                  "border-collapse:collapse;"
                                                                  "font:700 12pt 'Ericsson Hilda'"
                                                                  "}\n"
                                                                  "QHeaderView::section:first{\n"
                                                                  "border-top-left-radius:8px;\n"
                                                                  "}\n"
                                                                  "QHeaderView::section:last{\n"
                                                                  "border-top-right-radius:8px;\n"
                                                                  "}")
        self.main_window_ui.task_database_tableview.setShowGrid(True)                       # Shows the gridlines in table
