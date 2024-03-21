import logging
import numpy as np
import pandas as pd


def modify_action_cli_preparation_router(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Creates CLI for VPLS-1 Section for Action 'Modify'
    :param ip_node: ip_node for which the 'Modify' action data belongs to
    :param dataframe: filtered dataframe with only Modify action
    :return: cli (str) : cli for Modify action data
    """
    pass


def add_action_cli_preparation_router(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Creates CLI for VPLS-1 Section for Action 'Add'
    :param ip_node: ip_node for which the 'Add' action data belongs to
    :param dataframe: filtered dataframe with only Add action
    :return: cli (str): cli for Add action data
    """
    add_action_cli = ''
    unique_VPLS_IDs = np.array(dataframe['VPLS ID'].unique())
    unique_VPLS_IDs = unique_VPLS_IDs.astype(int)
    logging.info(f"Got an array of unique VPLS IDs for {ip_node}:-\n{'\n'.join(unique_VPLS_IDs.astype(str))}")

    i = 0
    while i < unique_VPLS_IDs.size:
        selected_vpls_id = unique_VPLS_IDs[i]
        temp_cli = ''

        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]
        vpls_name = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Name')]
        vpls_description = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Description')]
        ip_int_bind = temp_df.iloc[0, temp_df.columns.get_loc('allow-ip-int-bind')]
        stp_variable = temp_df.iloc[0, temp_df.columns.get_loc('STP')]
        additional_commands = temp_df.iloc[0, temp_df.columns.get_loc("Additional Command")]

        temp_cli = ("configure\n" +
                    "\tservice\n" +
                    f"\t\tvpls {selected_vpls_id} name {vpls_name} customer 1 create\n" +
                    f"\t\t\tdescription \"{vpls_description}\"\n")

        if ip_int_bind.strip().upper() == 'YES':
            temp_cli = (f"{temp_cli}\t\t\tallow-ip-int-bind\n" +
                        "\t\t\texit\n")

        if additional_commands != "TempNA":
            additional_commands_list = additional_commands.split(',')

            j = 0
            while j < len(additional_commands_list):
                temp_cli = f"{temp_cli}\t\t\t{additional_commands_list[j]}\n"
                j += 1

        if stp_variable != "TempNA":
            temp_cli = (f"{temp_cli}\t\t\tstp\n" +
                        f"\t\t\t\t{stp_variable}\n" +
                        "\t\t\texit\n")

        j = 0
        while j < temp_df.shape[0]:
            mesh_sdp_variable = temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")]
            mesh_sdp_description_variable = temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp Description")]
            mesh_sdp_status_variable = temp_df.iloc[j, temp_df.columns.get_loc("Mesh Status")]
            sap_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]
            sap_description_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap Description")]
            sap_status_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap Status")]
            sap_ingress_variable = temp_df.iloc[j, temp_df.columns.get_loc("Ingress")]
            sap_egress_variable = temp_df.iloc[j, temp_df.columns.get_loc("Egress")]

            if mesh_sdp_variable != "TempNA":
                temp_cli = f"{temp_cli}\t\t\t{mesh_sdp_variable} create\n"

                if mesh_sdp_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{mesh_sdp_description_variable}\"\n"

                if mesh_sdp_status_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\t{mesh_sdp_status_variable}\n"

                if mesh_sdp_status_variable == 'TempNA':
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            if sap_variable != "TempNA":
                temp_cli = f"{temp_cli}\t\t\t{sap_variable} create\n"

                if sap_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription {sap_description_variable}\n"

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.strip().upper() != 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                f"\t\t\t\t\t{sap_ingress_variable}\n" +
                                "\t\t\t\texit\n")

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.strip().upper() == 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.strip().upper() == "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.strip().upper() != "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                f"\t\t\t\t\t{sap_egress_variable}\n" +
                                "\t\t\t\texit\n")

                if sap_status_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\t{sap_status_variable}\n"

                if sap_status_variable == "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

            j += 1

        temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                    "\t\texit\n")

        add_action_cli = f"{add_action_cli}{temp_cli}"

        i += 1

    logging.info(f"{ip_node}: - Created the Add action CLI =>\n{add_action_cli}")

    return add_action_cli


def main_func(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Main function for VPLS-1 cli preparation
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :param dataframe: Dataframe containing the input from design_input_workbook
    :return: cli (str): cli containing commands of the design_input_workbook
    """
    cli = ''

    dataframe = dataframe.where(~(dataframe.isna()), 'TempNA')

    logging.info(f"Got the dataframe after replacing NA with TempNA for \'{ip_node}\':-\n{dataframe.to_markdown()}")

    add_action_dataframe = dataframe.loc[dataframe['Action'].str.upper().str.strip().str.endswith('ADD')]
    modify_action_dataframe = dataframe.loc[dataframe['Action'].str.upper().str.strip().str.endswith('MODIFY')]

    logging.info(f"{ip_node}: - Got the add_action_dataframe for add action=>\n{add_action_dataframe.to_markdown()}")
    logging.info(f"{ip_node}: - Got the modify_action_dataframe for add action=>\n{modify_action_dataframe.to_markdown()}")

    node_type = str(dataframe.iloc[0, dataframe.columns.get_loc('MPBN Node Type ( Router/Switch )')])

    if (len(add_action_dataframe) > 0) and (node_type.upper().strip() == 'ROUTER'):
        cli = add_action_cli_preparation_router(dataframe=add_action_dataframe,
                                                ip_node=ip_node)

    if (len(modify_action_dataframe) > 0) and (node_type.upper().strip() == 'ROUTER'):
        modify_action_cli_preparation_router(dataframe=modify_action_dataframe,
                                             ip_node=ip_node)

    cli = f'{cli}\texit all\n'

    logging.debug(f"{ip_node}: - Returning cli :-\n{cli}")

    return cli
