import logging
import numpy as np
import pandas as pd


node_type = ""


def modify_action_cli_preparation_add_sequence(dataframe: pd.DataFrame, ip_node: str) -> str:
    """Creates CLI for Add sequence of Modify Action.

    Args:
        dataframe (pd.DataFrame): filtered dataframe with add sequence of modify action.
        ip_node (str): current ip node.

    Returns:
        add_sequence_cli (str): cli prepared.
    """
    add_sequence_modify_cli = ''
    unique_VPLS_IDs = np.array(dataframe['VPLS ID'].unique()).astype(str)
    unique_VPLS_IDs = np.char.strip(unique_VPLS_IDs)
    unique_VPLS_IDs = unique_VPLS_IDs.astype(float).astype(int)
    logging.info(f"Got an array of unique VPLS IDs for {ip_node} for switch:-\n{'\n'.join(unique_VPLS_IDs.astype(str))}")

    i = 0
    while i < unique_VPLS_IDs.size:
        selected_vpls_id = unique_VPLS_IDs[i]
        temp_cli = ''

        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]

        # vpls_name = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Name')]
        vpls_description = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Description')]
        ip_int_bind = temp_df.iloc[0, temp_df.columns.get_loc('allow-ip-int-bind')]
        stp_variable = str(temp_df.iloc[0, temp_df.columns.get_loc('STP')]).strip().lower()
        additional_commands = temp_df.iloc[0, temp_df.columns.get_loc("Additional Command")]
        # svc_sap_type = 'svc-sap-type any'

        # temp_cli = (f"\t\tvpls {selected_vpls_id} customer 1 {svc_sap_type} create\n" +
        #             f"\t\t\tservice-name \"{vpls_name}\"\n" +
        #             f"\t\t\tdescription \"{vpls_description}\"\n")

        temp_cli = f"\t\tvpls {selected_vpls_id}\n"

        if vpls_description != 'TempNA':
            temp_cli = (f"{temp_cli}\t\t\tno description\n" +
                        f"\t\t\tdescription \"{vpls_description}\"\n")

        if ip_int_bind.strip().lower() == 'yes':
            temp_cli = (f"{temp_cli}\t\t\tallow-ip-int-bind\n" +
                        "\t\t\texit\n")
        
        if len(additional_commands) > 0:
            additional_commands_list = [str(command).strip().lower() for command in additional_commands.split(',')]

            if len(additional_commands_list) > 0:
                j = 0
                while j < len(additional_commands_list):
                    if additional_commands_list[j] != 'tempna':
                        temp_cli = f"{temp_cli}\t\t\t{additional_commands_list[j]}\n"
                    j += 1

            if stp_variable != 'tempna':
                temp_cli = (f"{temp_cli}\t\t\tstp\n" +
                            f"\t\t\t\t{stp_variable}\n" +
                            "\t\t\texit\n")
            j = 0
        while j < temp_df.shape[0]:
            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")]).strip().lower()
            mesh_sdp_description_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp Description")])
            mesh_sdp_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh Status")]).strip().lower()
            sap_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]).strip().lower()
            sap_description_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap Description")]
            sap_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap Status")]).strip().lower()
            sap_ingress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Ingress")])
            sap_egress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Egress")])

            if mesh_sdp_variable != "tempna":
                temp_cli = f"{temp_cli}\t\t\t{mesh_sdp_variable} create\n"

                if mesh_sdp_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{mesh_sdp_description_variable}\"\n"

                if mesh_sdp_status_variable != "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\t{mesh_sdp_status_variable}\n"

                if mesh_sdp_status_variable == 'tempna':
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            if sap_variable != "tempna":
                temp_cli = f"{temp_cli}\t\t\t{sap_variable} create\n"

                if sap_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{sap_description_variable}\"\n"

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.strip().upper() != 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                f"\t\t\t\t\t{sap_ingress_variable.strip().lower()}\n" +
                                "\t\t\t\texit\n")

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.upper() == 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.upper() == "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.upper() != "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                f"\t\t\t\t\t{sap_egress_variable.strip().lower()}\n" +
                                "\t\t\t\texit\n")

                if sap_status_variable != "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\t{sap_status_variable}\n"

                if sap_status_variable == "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            j += 1

        temp_cli = (f"{temp_cli}" +
                    "\t\texit\n")

        add_sequence_modify_cli = f"{add_sequence_modify_cli}{temp_cli}"
        i += 1

    logging.info(f"{ip_node}: - Created the Add sequence CLI of VPLS-1 for Modify action=>\n{add_sequence_modify_cli}")

    return add_sequence_modify_cli


def modify_action_cli_preparation_delete_sequence(dataframe: pd.DataFrame, ip_node: str) -> str:
    """Creates CLI for Delete sequence of Modify Action.

    Args:
        dataframe (pd.DataFrame): filtered dataframe with delete sequence of modify action.
        ip_node (str): current ip node.

    Returns:
        delete_sequence_cli (str): cli prepared.
    """
    delete_sequence_cli = ""

    unique_vpls_id_enteries = np.array(dataframe['VPLS ID'].unique()).astype(str)
    unique_vpls_id_enteries = np.char.strip(unique_vpls_id_enteries)
    unique_vpls_id_enteries = unique_vpls_id_enteries.astype(float).astype(int)

    i = 0
    while i < unique_vpls_id_enteries.size:
        selected_vpls_id = unique_vpls_id_enteries[i]
        temp_df = dataframe.loc[dataframe["VPLS ID"] == selected_vpls_id]
        temp_cli = ''

        temp_cli = f"\t\tvpls {selected_vpls_id}\n"

        j = 0
        while j < temp_df.shape[0]:
            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")]).strip().lower()
            sap_lag_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]).strip().lower()

            if mesh_sdp_variable != 'tempna':
                temp_cli = (f"{temp_cli}\t\t\t{mesh_sdp_variable}\n" +
                            "\t\t\t\tshutdown\n" +
                            "\t\t\texit\n" +
                            f"\t\t\tno {mesh_sdp_variable}\n")

            if sap_lag_variable != 'tempna':
                temp_cli = (f"{temp_cli}\t\t\t{sap_lag_variable}\n" +
                            "\t\t\t\tshutdown\n" +
                            "\t\t\texit\n" +
                            f"\t\t\tno {sap_lag_variable}\n")

            j += 1
        
        temp_cli = f'{temp_cli}\t\texit\n'
        delete_sequence_cli = f"{delete_sequence_cli}{temp_cli}"
        i += 1

    logging.info(f"{ip_node}: - Created CLI for \'DELETE\' sequence of \'MODIFY\' action of VPLS-1 :- \n{delete_sequence_cli}")
    return delete_sequence_cli


def modify_action_cli_preparation_modify_sequence(dataframe: pd.DataFrame, ip_node: str) -> str:
    """Creates CLI for Modify sequence of Modify Action.

    Args:
        dataframe (pd.DataFrame): filtered dataframe with modify sequence of modify action.
        ip_node (str): current ip_node.

    Returns:
        modify_sequence_cli (str): cli prepared.
    """
    modify_sequence_cli = ""
    unique_vpls_id_array = np.array(dataframe['VPLS ID'].unique()).astype(str)
    unique_vpls_id_array = np.char.strip(unique_vpls_id_array)
    unique_vpls_id_array = unique_vpls_id_array.astype(float).astype(int)
    logging.info(f"{ip_node}: - Got an array of unique VPLS IDs:\n{'\n'.join(unique_vpls_id_array.astype(str))}")

    i = 0
    while i < unique_vpls_id_array.size:
        selected_vpls_id = unique_vpls_id_array[i]
        temp_df = dataframe.loc[dataframe["VPLS ID"] == selected_vpls_id]
        # vpls_description_variable  = str(temp_df.iloc[0, temp_df.columns.get_loc("VPLS Description")])
        # stp_variable = str(temp_df.iloc[0, temp_df.columns.get_loc("STP")]).strip().lower()
        # allow_ip_int_bind_variable = str(temp_df.iloc[0, temp_df.columns.get_loc("allow-ip-int-bind")]).strip()
        temp_cli  = ""

        temp_cli = f"\t\tvpls {selected_vpls_id}\n"

        # if vpls_description_variable != "TempNA":
        #     temp_cli = (f"{temp_cli}\t\t\tno description\n" +
        #                 f"\t\t\tdescription \"{vpls_description_variable}\"\n")

        # if stp_variable != 'TempNA':
        #     temp_cli = (f"{temp_cli}\t\t\tstp\n" +
        #                 f"\t\t\t\t{stp_variable}\n" +
        #                 "\t\t\texit\n")
        
        # if (allow_ip_int_bind_variable != "TempNA") and (allow_ip_int_bind_variable.lower() == 'yes'):
        #     temp_cli = (f"{temp_cli}\t\t\tallow-ip-int-bind\n" +
        #                 "\t\t\texit\n")
        
        # if (allow_ip_int_bind_variable != "TempNA") and (allow_ip_int_bind_variable.lower() == 'no'):
        #     temp_cli = (f"{temp_cli}\t\t\tno allow-ip-int-bind\n" +
        #                 "\t\t\texit\n")
        j = 0
        while j < temp_df.shape[0]:
            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc('Mesh-sdp')]).strip()
            sap_lag_variable  = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]).strip()

            if mesh_sdp_variable != "TempNA":
                # mesh_sdp_description_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp Description")]).strip()
                mesh_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh Status")]).strip().lower()

                temp_cli = f"{temp_cli}\t\t\t{mesh_sdp_variable}\n"

                # if mesh_sdp_description_variable != "TempNA":
                #     temp_cli = (f"{temp_cli}\t\t\t\tno description\n"
                #                 f"\t\t\t\tdescription \"{mesh_sdp_description_variable}\"\n")

                if mesh_status_variable != "TempNA":
                    if (isinstance(mesh_status_variable, str)) and (mesh_status_variable.__contains__(",")):
                        vpls_mesh_statuses = [str(status).strip() for status in mesh_status_variable.split(",")]

                        if len(vpls_mesh_statuses) > 1:
                            if len(vpls_mesh_statuses[1].strip()) > 0:
                                temp_cli = f"{temp_cli}\t\t\t\t{vpls_mesh_statuses[1].strip().lower()}\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            if sap_lag_variable != "TempNA":
                # sap_lag_description_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap Description")]).strip()
                sap_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap Status")]).strip()
                # ingress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Ingress")]).strip().lower()
                # egress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Egress")]).strip().lower()

                temp_cli = f"{temp_cli}\t\t\t{sap_lag_variable}\n"

                # if sap_lag_description_variable != 'TempNA':
                #     temp_cli = (f"{temp_cli}\t\t\t\tno description\n" +
                #                 f"\t\t\t\tdescription \"{sap_lag_description_variable}\"\n")

                # if ingress_variable != "tempna":
                #     temp_cli = f"{temp_cli}\t\t\t\tingress\n"

                #     if ingress_variable != 'yes':
                #         temp_cli = f"{temp_cli}\t\t\t\t\t{ingress_variable}\n"

                #     temp_cli = f"{temp_cli}\t\t\t\texit\n"

                # if egress_variable != "tempna":
                #     temp_cli = f"{temp_cli}\t\t\t\tegress\n"

                #     if egress_variable != 'yes':
                #         temp_cli = f"{temp_cli}\t\t\t\t\t{egress_variable}\n"

                #     temp_cli = f"{temp_cli}\t\t\t\texit\n"

                if (sap_status_variable != 'TempNA') and (sap_status_variable.__contains__(",")):
                    sap_statuses = sap_status_variable.split(",")

                    if len(sap_statuses) > 1:
                        if len(sap_statuses[1].strip()) > 0:
                            temp_cli = f"{temp_cli}\t\t\t\t{sap_statuses[1].strip()}\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            j += 1

        temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                    "\t\texit\n")

        modify_sequence_cli = f"{modify_sequence_cli}{temp_cli}"

        i += 1

    logging.info(f"{ip_node}: - Created the cli of VPLS-1 for modify action modify sequence: -\n{modify_sequence_cli}")

    return modify_sequence_cli


def modify_action_cli_preparation_router(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Creates CLI for VPLS-1 Section for Action 'Modify'
    :param ip_node: ip_node for which the 'Modify' action data belongs to
    :param dataframe: filtered dataframe with only Modify action
    :return: cli (str) : cli for Modify action data
    """
    sequence_add_modify_df       = dataframe.loc[(dataframe["Sequence"].str.strip() != 'TempNA') & (dataframe["Sequence"].str.strip().str.upper().str.endswith("ADD"))]
    sequence_delete_modify_df    = dataframe.loc[(dataframe["Sequence"].str.strip() != 'TempNA') & (dataframe["Sequence"].str.strip().str.upper().str.endswith("DELETE"))]
    sequence_modify_modify_df    = dataframe.loc[(dataframe["Sequence"].str.strip() != 'TempNA') & (dataframe["Sequence"].str.strip().str.upper().str.endswith("MODIFY"))]

    modify_cli =""

    if sequence_add_modify_df.shape[0] > 0:
        modify_cli = f"{modify_cli}{modify_action_cli_preparation_add_sequence(dataframe= sequence_add_modify_df, ip_node= ip_node)}"

    if sequence_modify_modify_df.shape[0] > 0:
        modify_cli = f"{modify_cli}{modify_action_cli_preparation_modify_sequence(dataframe= sequence_modify_modify_df, ip_node= ip_node)}"

    if sequence_delete_modify_df.shape[0] > 0:
        modify_cli = f"{modify_cli}{modify_action_cli_preparation_delete_sequence(dataframe= sequence_delete_modify_df, ip_node= ip_node)}"

    return modify_cli


def add_action_cli_preparation_switch(dataframe: pd.DataFrame, ip_node: str) -> str:
    """Creates CLI for VPLS-1 Section for Action 'Add' for switch.

    Args:
        dataframe (pd.DataFrame): filtered dataframe with only Add action
        ip_node (str): ip_node for which the 'Add' action data belongs to

    Returns:
        cli (str): cli for Add action data
    """
    add_action_switch_cli = ""
    unique_VPLS_IDs = np.array(dataframe['VPLS ID'].unique()).astype(str)
    unique_VPLS_IDs = np.char.strip(unique_VPLS_IDs)
    unique_VPLS_IDs = unique_VPLS_IDs.astype(float).astype(int)
    logging.info(f"Got an array of unique VPLS IDs for {ip_node} for switch:-\n{'\n'.join(unique_VPLS_IDs.astype(str))}")

    i = 0
    while i < unique_VPLS_IDs.size:
        selected_vpls_id = unique_VPLS_IDs[i]
        temp_cli = ''

        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]

        vpls_name = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Name')]
        vpls_description = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Description')]
        ip_int_bind = temp_df.iloc[0, temp_df.columns.get_loc('allow-ip-int-bind')]
        stp_variable = str(temp_df.iloc[0, temp_df.columns.get_loc('STP')]).strip().lower()
        additional_commands = temp_df.iloc[0, temp_df.columns.get_loc("Additional Command")]
        svc_sap_type = 'svc-sap-type any'

        temp_cli = (f"\t\tvpls {selected_vpls_id} customer 1 {svc_sap_type} create\n" +
                    f"\t\t\tservice-name \"{vpls_name}\"\n" +
                    f"\t\t\tdescription \"{vpls_description}\"\n")

        if ip_int_bind.strip().lower() == 'yes':
            temp_cli = (f"{temp_cli}\t\t\tallow-ip-int-bind\n" +
                        "\t\t\texit\n")

        if len(additional_commands) > 0:
            additional_commands_list = [str(command).strip().lower() for command in additional_commands.split(',')]

            if len(additional_commands_list) > 0:
                j = 0
                while j < len(additional_commands_list):
                    temp_cli = f"{temp_cli}\t\t\t{additional_commands_list[j]}\n"
                    j += 1

            if stp_variable != 'TempNA':
                temp_cli = (f"{temp_cli}\t\t\tstp\n" +
                            f"\t\t\t\t{stp_variable}\n" +
                            "\t\t\texit\n")
            j = 0
        while j < temp_df.shape[0]:
            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")]).strip().lower()
            mesh_sdp_description_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp Description")])
            mesh_sdp_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh Status")]).strip().lower()
            sap_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]).strip().lower()
            sap_description_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap Description")]
            sap_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap Status")]).strip().lower()
            sap_ingress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Ingress")])
            sap_egress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Egress")])

            if mesh_sdp_variable != "tempna":
                temp_cli = f"{temp_cli}\t\t\t{mesh_sdp_variable} create\n"

                if mesh_sdp_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{mesh_sdp_description_variable}\"\n"

                if mesh_sdp_status_variable != "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\t{mesh_sdp_status_variable}\n"

                if mesh_sdp_status_variable == 'tempna':
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            if sap_variable != "tempna":
                temp_cli = f"{temp_cli}\t\t\t{sap_variable} create\n"

                if sap_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{sap_description_variable}\"\n"

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.strip().upper() != 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                f"\t\t\t\t\t{sap_ingress_variable.strip().lower()}\n" +
                                "\t\t\t\texit\n")

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.upper() == 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.upper() == "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.upper() != "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                f"\t\t\t\t\t{sap_egress_variable.strip().lower()}\n" +
                                "\t\t\t\texit\n")

                if sap_status_variable != "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\t{sap_status_variable}\n"

                if sap_status_variable == "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            j += 1

        temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                    "\t\texit\n")

        add_action_switch_cli = f"{add_action_switch_cli}{temp_cli}"
        i += 1

    logging.info(f"{ip_node}: - Created the Add action CLI for switch =>\n{add_action_switch_cli}")

    return add_action_switch_cli


def add_action_cli_preparation_router(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Creates CLI for VPLS-1 Section for Action 'Add' for router.
    :param ip_node: ip_node for which the 'Add' action data belongs to
    :param dataframe: filtered dataframe with only Add action
    :return: cli (str): cli for Add action data
    """
    add_action_cli = ''
    unique_VPLS_IDs = np.array(dataframe['VPLS ID'].unique()).astype(str)
    unique_VPLS_IDs = np.char.strip(unique_VPLS_IDs)
    unique_VPLS_IDs = unique_VPLS_IDs.astype(float).astype(int)
    logging.info(f"Got an array of unique VPLS IDs for {ip_node}:-\n{'\n'.join(unique_VPLS_IDs.astype(str))}")

    i = 0
    while i < unique_VPLS_IDs.size:
        selected_vpls_id = unique_VPLS_IDs[i]
        temp_cli = ''

        temp_df = dataframe.loc[dataframe['VPLS ID'] == selected_vpls_id]
        vpls_name = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Name')]
        vpls_description = temp_df.iloc[0, temp_df.columns.get_loc('VPLS Description')]
        ip_int_bind = temp_df.iloc[0, temp_df.columns.get_loc('allow-ip-int-bind')]
        stp_variable = str(temp_df.iloc[0, temp_df.columns.get_loc('STP')]).strip().lower()
        additional_commands = temp_df.iloc[0, temp_df.columns.get_loc("Additional Command")]

        temp_cli = (f"\t\tvpls {selected_vpls_id} name \"{vpls_name}\" customer 1 create\n" +
                    f"\t\t\tdescription \"{vpls_description}\"\n")

        if ip_int_bind.strip().upper() == 'YES':
            temp_cli = (f"{temp_cli}\t\t\tallow-ip-int-bind\n" +
                        "\t\t\texit\n")

        if additional_commands != "TempNA":
            additional_commands_list = additional_commands.split(',')
            additional_commands_list = [command.strip().lower() for command in additional_commands_list]

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
            mesh_sdp_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp")]).strip().lower()
            mesh_sdp_description_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh-sdp Description")])
            mesh_sdp_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Mesh Status")]).strip().lower()
            sap_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap/Lag")]).strip().lower()
            sap_description_variable = temp_df.iloc[j, temp_df.columns.get_loc("Sap Description")]
            sap_status_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Sap Status")]).strip().lower()
            sap_ingress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Ingress")])
            sap_egress_variable = str(temp_df.iloc[j, temp_df.columns.get_loc("Egress")])

            if mesh_sdp_variable != "tempna":
                temp_cli = f"{temp_cli}\t\t\t{mesh_sdp_variable} create\n"

                if mesh_sdp_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{mesh_sdp_description_variable}\"\n"

                if mesh_sdp_status_variable != "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\t{mesh_sdp_status_variable}\n"

                if mesh_sdp_status_variable == 'tempna':
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

            if sap_variable != "tempna":
                temp_cli = f"{temp_cli}\t\t\t{sap_variable} create\n"

                if sap_description_variable != "TempNA":
                    temp_cli = f"{temp_cli}\t\t\t\tdescription \"{sap_description_variable}\"\n"

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.strip().upper() != 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                f"\t\t\t\t\t{sap_ingress_variable.strip().lower()}\n" +
                                "\t\t\t\texit\n")

                if (sap_ingress_variable != "TempNA") and (sap_ingress_variable.upper() == 'YES'):
                    temp_cli = (f"{temp_cli}\t\t\t\tingress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.upper() == "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                "\t\t\t\texit\n")

                if (sap_egress_variable != "TempNA") and (sap_egress_variable.upper() != "YES"):
                    temp_cli = (f"{temp_cli}\t\t\t\tegress\n" +
                                f"\t\t\t\t\t{sap_egress_variable.strip().lower()}\n" +
                                "\t\t\t\texit\n")

                if sap_status_variable != "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\t{sap_status_variable}\n"

                if sap_status_variable == "tempna":
                    temp_cli = f"{temp_cli}\t\t\t\tno shutdown\n"

                temp_cli = f"{temp_cli}\t\t\texit\n"

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
    cli = ('configure\n' +
           '\tservice\n')

    dataframe = dataframe.where(~(dataframe.isna()), 'TempNA')

    logging.info(f"Got the dataframe after replacing NA with TempNA for \'{ip_node}\':-\n{dataframe.to_markdown()}")

    add_action_dataframe = dataframe.loc[dataframe['Action'].str.upper().str.strip().str.endswith('ADD')]
    modify_action_dataframe = dataframe.loc[dataframe['Action'].str.upper().str.strip().str.endswith('MODIFY')]

    logging.info(f"{ip_node}: - Got the add_action_dataframe for add action=>\n{add_action_dataframe.to_markdown()}")
    logging.info(f"{ip_node}: - Got the modify_action_dataframe for add action=>\n{modify_action_dataframe.to_markdown()}")

    global node_type; node_type = str(dataframe.iloc[0, dataframe.columns.get_loc('MPBN Node Type ( Router/Switch )')])

    if (len(add_action_dataframe) > 0) and (node_type.upper().strip() == 'ROUTER'):
        cli = f'{cli}{add_action_cli_preparation_router(dataframe=add_action_dataframe,
                                                        ip_node=ip_node)}'
    
    if (len(add_action_dataframe) > 0) and (node_type.upper().strip() == 'SWITCH'):
        cli = f'{cli}{add_action_cli_preparation_switch(dataframe=add_action_dataframe,
                                                        ip_node=ip_node)}'

    if (len(modify_action_dataframe) > 0) and (node_type.upper().strip() == 'ROUTER'):
        cli = f"{cli}{modify_action_cli_preparation_router(dataframe=modify_action_dataframe,
                                             ip_node=ip_node)}"
    

    cli = f'{cli}\texit all\n'

    logging.debug(f"{ip_node}: - Returning cli :-\n{cli}")

    return cli
