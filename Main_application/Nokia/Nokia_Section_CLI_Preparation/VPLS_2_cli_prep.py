import logging
import numpy as np
import pandas as pd


def vsd_domain_creation_cli_func(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for vsd domain creation
    :param dataframe: dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """
    result_cli = "configure service vsd\n"

    i = 0
    while i < dataframe.shape[0]:
        temp_cli = ""
        domain_name_var = dataframe.iloc[i, dataframe.columns.get_loc("Vsd-domain Name")]
        domain_type_var = dataframe.iloc[i, dataframe.columns.get_loc("Vsd-domain Type")]
        domain_description = dataframe.iloc[i, dataframe.columns.get_loc("Vsd-domain Description")]
        temp_cli = (f"{temp_cli}domain \"{domain_name_var}\" type {domain_type_var} create\n" +
                    f"\tdescription \"{domain_description}\"\n" +
                    "\tno shutdown\n" +
                    "exit\n")
        result_cli = f"{result_cli}{temp_cli}\n"
        i += 1

    result_cli = (f"{result_cli}exit all\n" +
                  "admin save\n")

    return result_cli


def add_action_cli_for_vsd_controller_mapping_as_yes(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for action add for vsd controller mapping as yes
    :param dataframe: Dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """
    result_cli = ""

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float).astype(int)
    logging.info(
        f"{ip_node}: - unique vpls ids\n"
        f"{', '.join([str(x) for x in unique_vpls_ids])}"
    )

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe["VPLS ID"] == selected_vpls]
        selected_vpls_name = temp_df.iloc[0, temp_df.columns.get_loc("VPLS Name")]
        logging.info(
            f"{ip_node}: - selected vpls {selected_vpls}\n"
            f"{temp_df.to_markdown()}"
        )

        bgp_var = dataframe.iloc[0, dataframe.columns.get_loc("BGP")]
        vsi_export_var = dataframe.iloc[0, dataframe.columns.get_loc("VSI-Export")]
        vsi_import_var = dataframe.iloc[0, dataframe.columns.get_loc("VSI-Import")]

        temp_cli = f"\t\tvpls {selected_vpls} name \"{selected_vpls_name}\" customer 1 create\n"

        additional_commands_array = np.array(temp_df["Additional Command"])

        if additional_commands_array.size > 0:
            j = 0
            while j < additional_commands_array.size:
                if str(additional_commands_array[j]) != "TempNA":
                    if not str(additional_commands_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t{str(additional_commands_array[j]).strip().lower()}\n"

                    if str(additional_commands_array[j]).strip().__contains__(","):
                        additional_commands_array_list = str(additional_commands_array[j]).strip().split(",")
                        k = 0
                        while k < len(additional_commands_array_list):
                            temp_cli = f"{temp_cli}\t\t\t{additional_commands_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1

        allow_ip_int_bind_array = np.array(temp_df["allow-ip-int-bind"])

        if allow_ip_int_bind_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tallow-ip-int-bind\n"
            j = 0
            while j < allow_ip_int_bind_array.size:
                if str(allow_ip_int_bind_array[j]).strip().upper() == "YES":
                    j += 1
                    continue

                if str(allow_ip_int_bind_array[j]) != "TempNA":
                    if not str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t\t{str(allow_ip_int_bind_array[j]).strip().lower()}\n"

                    if str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        allow_ip_int_bind_array_list = str(allow_ip_int_bind_array[j]).strip().split(",")
                        k = 0
                        while k < len(allow_ip_int_bind_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{allow_ip_int_bind_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1
            temp_cli = f"{temp_cli}\t\t\texit\n"

        if str(bgp_var).strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tbgp\n"
            if str(bgp_var).strip().upper() == "YES":
                pass

            if str(bgp_var).strip().upper() != "YES":
                temp_cli = f"{temp_cli}\t\t\t\t{str(bgp_var).strip().lower()}\n"

                if str(vsi_export_var).strip() != "TempNA":
                    if not str(vsi_export_var).strip().__contains__("vsi-export"):
                        temp_cli = f"{temp_cli}\t\t\t\tvsi-export \"{str(vsi_export_var).strip()}\"\n"

                    if str(vsi_export_var).strip().__contains__("vsi-export"):
                        temp_cli = f"{temp_cli}\t\t\t\t\"{str(vsi_export_var).strip()}\"\n"

                if str(vsi_import_var).strip() != "TempNA":
                    if not str(vsi_import_var).strip().__contains__("vsi-import"):
                        temp_cli = f"{temp_cli}\t\t\t\tvsi-import \"{str(vsi_import_var).strip()}\"\n"

                    if str(vsi_import_var).strip().__contains__("vsi-import"):
                        temp_cli = f"{temp_cli}\t\t\t\t{str(vsi_import_var).strip()}\n"

            temp_cli = f"{temp_cli}\t\t\texit\n"

        bgp_evpn_series_array = np.array(temp_df["BGP-Evpn"])

        if bgp_evpn_series_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tbgp-evpn\n"
            j = 0
            while j < bgp_evpn_series_array.size:
                if str(bgp_evpn_series_array[j]) != "TempNA":
                    if not str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        if str(bgp_evpn_series_array[j]).strip().upper() == "YES":
                            j += 1
                            continue

                        if str(bgp_evpn_series_array[j]).strip() != "YES":
                            temp_cli = f"{temp_cli}\t\t\t\t{str(bgp_evpn_series_array[j]).strip().lower()}\n"

                    if str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        bgp_evpn_series_array_list = str(bgp_evpn_series_array[j]).strip().split(",")
                        k = 0
                        while k < len(bgp_evpn_series_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{bgp_evpn_series_array_list[k].strip().lower()}\n"
                            k += 1
                j += 1

            temp_cli = f"{temp_cli}\t\t\texit\n"

        stp_var = str(temp_df.iloc[0, temp_df.columns.get_loc("STP")])
        if stp_var.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tstp\n"
            if str(stp_var).strip().upper() == "YES":
                pass
            if str(stp_var).strip().upper() != "YES":
                temp_cli = f"{temp_cli}\t\t\t\t{str(stp_var).strip().lower()}\n"
            temp_cli = f"{temp_cli}\t\t\texit\n"

        vsd_domain_name = str(temp_df.iloc[0, temp_df.columns.get_loc("Vsd-domain Name")])
        if vsd_domain_name.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tvsd-domain-name \"{str(vsd_domain_name).strip()}\"\n"

        vpls_status = str(temp_df.iloc[0, temp_df.columns.get_loc("VPLS Status")]).strip().lower()

        if vpls_status != 'tempna':
            temp_cli = (f"{temp_cli}\t\t\t{vpls_status}\n"
                        "\t\texit\n")

        if vpls_status == 'tempna':
            temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                        "\t\texit\n")
        result_cli = f"{result_cli}{temp_cli}"
        i += 1

    return result_cli


def add_action_cli_for_vsd_controller_mapping_as_no(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Add action CLI for VSD controller mapping as no.
    :param dataframe: The input pandas DataFrame.
    :param ip_node: The IP address of the node.
    :return: A string representing the result of the action.
    """

    result_cli = ""

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float).astype(int)
    logging.info(
        f"{ip_node}: - unique vpls ids\n"
        f"{', '.join([str(x) for x in unique_vpls_ids])}"
    )

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe["VPLS ID"] == selected_vpls]
        selected_vpls_name = temp_df.iloc[0, temp_df.columns.get_loc("VPLS Name")]
        logging.info(
            f"{ip_node}: - selected vpls {selected_vpls}\n"
            f"{temp_df.to_markdown()}"
        )

        temp_cli = f"\t\tvpls {selected_vpls} name \"{selected_vpls_name}\" customer 1 create\n"

        additional_commands_array = np.array(temp_df["Additional Command"])

        if additional_commands_array.size > 0:
            j = 0
            while j < additional_commands_array.size:
                if str(additional_commands_array[j]) != "TempNA":
                    if not str(additional_commands_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t{str(additional_commands_array[j]).strip().lower()}\n"

                    if str(additional_commands_array[j]).strip().__contains__(","):
                        additional_commands_array_list = str(additional_commands_array[j]).strip().split(",")
                        k = 0
                        while k < len(additional_commands_array_list):
                            temp_cli = f"{temp_cli}\t\t\t{additional_commands_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1

        allow_ip_int_bind_array = np.array(temp_df["allow-ip-int-bind"])

        if allow_ip_int_bind_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tallow-ip-int-bind\n"
            j = 0
            while j < allow_ip_int_bind_array.size:
                if str(allow_ip_int_bind_array[j]).strip().upper() == "YES":
                    j += 1
                    continue

                if str(allow_ip_int_bind_array[j]) != "TempNA":
                    if not str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t\t{str(allow_ip_int_bind_array[j]).strip().lower()}\n"

                    if str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        allow_ip_int_bind_array_list = str(allow_ip_int_bind_array[j]).strip().split(",")
                        k = 0
                        while k < len(allow_ip_int_bind_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{allow_ip_int_bind_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1
            temp_cli = f"{temp_cli}\t\texit\n"

        vxlan_var = str(temp_df.iloc[0, temp_df.columns.get_loc("VXLAN Instance")])
        vni_var = str(temp_df.iloc[0, temp_df.columns.get_loc("VNI ID")])

        if (vxlan_var != "TempNA") and (vni_var != "TempNA"):
            temp_cli = (f"{temp_cli}\t\t\tvxlan instance {int(float(vxlan_var))} vni {int(float(vni_var))} create\n"
                        "\t\t\texit\n")
        bgp_var = str(temp_df.iloc[0, temp_df.columns.get_loc("BGP")])
        rt_export_var = str(temp_df.iloc[0, temp_df.columns.get_loc("RT-Export")])
        rt_import_var = str(temp_df.iloc[0, temp_df.columns.get_loc("RT-Import")])

        if bgp_var.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tbgp\n"
            if (rt_import_var.strip() != "TempNA") and (rt_export_var.strip() != "TempNA"):
                temp_cli = f"{temp_cli}\t\t\t\t{bgp_var}\n\t\t\t\troute-target export {rt_export_var}\n\t\t\t\troute-target import {rt_import_var}\n"

            elif (rt_export_var.strip() != "TempNA") and (rt_import_var.strip() == "TempNA"):
                temp_cli = f"{temp_cli}\t\t\t\t{bgp_var}\n\t\t\t\troute-target export {rt_export_var}\n"

            elif (rt_export_var.strip() == "TempNA") and (rt_import_var.strip() != "TempNA"):
                temp_cli = f"{temp_cli}\t\t\t\t{bgp_var}\n\t\t\t\troute-target import {rt_import_var}\n"

            temp_cli = f"{temp_cli}\t\t\texit\n"


        bgp_evpn_series_array = np.array(temp_df["BGP-Evpn"])

        if bgp_evpn_series_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tbgp-evpn\n"
            j = 0
            while j < bgp_evpn_series_array.size:
                if str(bgp_evpn_series_array[j]) != "TempNA":
                    if not str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        if str(bgp_evpn_series_array[j]).strip().upper() == "YES":
                            j += 1
                            continue

                        if str(bgp_evpn_series_array[j]).strip() != "YES":
                            temp_cli = f"{temp_cli}\t\t\t\t{str(bgp_evpn_series_array[j]).strip().lower()}\n"

                    if str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        bgp_evpn_series_array_list = str(bgp_evpn_series_array[j]).strip().split(",")
                        k = 0
                        while k < len(bgp_evpn_series_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{bgp_evpn_series_array_list[k].strip().lower()}\n"
                            k += 1
                j += 1

            temp_cli = f"{temp_cli}\t\t\texit\n"

        stp_var = str(temp_df.iloc[0, temp_df.columns.get_loc("STP")])
        if stp_var.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tstp\n"
            if str(stp_var).strip().upper() == "YES":
                pass
            if str(stp_var).strip().upper() != "YES":
                temp_cli = f"{temp_cli}\t\t\t\t{str(stp_var).strip().lower()}\n"
            temp_cli = f"{temp_cli}\t\t\texit\n"

        vpls_status = str(temp_df.iloc[0, temp_df.columns.get_loc("VPLS Status")]).lower().strip()

        if vpls_status != 'tempna':
            temp_cli = (f"{temp_cli}\t\t\t{vpls_status}\n"
                        "\t\texit\n")

        if vpls_status == 'tempna':
            temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                        "\t\texit\n")
        result_cli = f"{result_cli}{temp_cli}"

        i+=1

    return result_cli


def add_action_cli(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for action add
    :param dataframe: Dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """
    temp_cli = ''

    filtered_dataframe_with_add_action_vsd_controller_mapping_as_yes = dataframe.loc[dataframe['VSD Controller Mapping'].str.strip().str.upper().str.upper() == 'YES']
    logging.info(
        f"{ip_node}: - filtered dataframe with add action vsd controller mapping as yes\n"
        f"{filtered_dataframe_with_add_action_vsd_controller_mapping_as_yes.to_markdown()}"
    )

    filtered_dataframe_with_add_action_vsd_controller_mapping_as_no = dataframe.loc[dataframe['VSD Controller Mapping'].str.strip().str.upper().str.upper() == 'NO']
    logging.info(
        f"{ip_node}: - filtered dataframe with add action vsd controller mapping as no\n"
        f"{filtered_dataframe_with_add_action_vsd_controller_mapping_as_no.to_markdown()}"
    )

    if filtered_dataframe_with_add_action_vsd_controller_mapping_as_yes.shape[0] > 0:
        temp_cli = f"{temp_cli}\n{add_action_cli_for_vsd_controller_mapping_as_yes(filtered_dataframe_with_add_action_vsd_controller_mapping_as_yes, ip_node)}"

    if filtered_dataframe_with_add_action_vsd_controller_mapping_as_no.shape[0] > 0:
        temp_cli = f"{temp_cli}\n{add_action_cli_for_vsd_controller_mapping_as_no(filtered_dataframe_with_add_action_vsd_controller_mapping_as_no, ip_node)}"

    return temp_cli

def modify_action_add_sequence_cli_for_vsd_controller_mapping_as_yes(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for action modify sequence add for vsd controller mapping as yes
    :param dataframe: Dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """

    result_cli = ""

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float).astype(int)
    logging.info(
        f"{ip_node}: - unique vpls ids\n"
        f"{', '.join([str(x) for x in unique_vpls_ids])}"
    )

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe["VPLS ID"] == selected_vpls]

        logging.info(
            f"{ip_node}: - selected vpls {selected_vpls}\n"
            f"{temp_df.to_markdown()}"
        )

        bgp_var = dataframe.iloc[0, dataframe.columns.get_loc("BGP")]
        vsi_export_var = dataframe.iloc[0, dataframe.columns.get_loc("VSI-Export")]
        vsi_import_var = dataframe.iloc[0, dataframe.columns.get_loc("VSI-Import")]

        temp_cli = f"\t\tvpls {selected_vpls}\n"

        additional_commands_array = np.array(temp_df["Additional Command"])

        if additional_commands_array.size > 0:
            j = 0
            while j < additional_commands_array.size:
                if str(additional_commands_array[j]) != "TempNA":
                    if not str(additional_commands_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t{str(additional_commands_array[j]).strip().lower()}\n"

                    if str(additional_commands_array[j]).strip().__contains__(","):
                        additional_commands_array_list = str(additional_commands_array[j]).strip().split(",")
                        k = 0
                        while k < len(additional_commands_array_list):
                            temp_cli = f"{temp_cli}\t\t\t{additional_commands_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1

        allow_ip_int_bind_array = np.array(temp_df["allow-ip-int-bind"])

        if allow_ip_int_bind_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tallow-ip-int-bind\n"
            j = 0
            while j < allow_ip_int_bind_array.size:
                if str(allow_ip_int_bind_array[j]).strip().upper() == "YES":
                    j += 1
                    continue

                if str(allow_ip_int_bind_array[j]) != "TempNA":
                    if not str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t\t{str(allow_ip_int_bind_array[j]).strip().lower()}\n"

                    if str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        allow_ip_int_bind_array_list = str(allow_ip_int_bind_array[j]).strip().split(",")
                        k = 0
                        while k < len(allow_ip_int_bind_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{allow_ip_int_bind_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1
            temp_cli = f"{temp_cli}\t\t\texit\n"

        if str(bgp_var).strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tbgp\n"
            if str(bgp_var).strip().upper() == "YES":
                pass

            if str(bgp_var).strip().upper() != "YES":
                temp_cli = f"{temp_cli}\t\t\t\t{str(bgp_var).strip().lower()}\n"

                if str(vsi_export_var).strip() != "TempNA":
                    if not str(vsi_export_var).strip().__contains__("vsi-export"):
                        temp_cli = f"{temp_cli}\t\t\t\tvsi-export \"{str(vsi_export_var).strip()}\"\n"

                    if str(vsi_export_var).strip().__contains__("vsi-export"):
                        temp_cli = f"{temp_cli}\t\t\t\t\"{str(vsi_export_var).strip()}\"\n"

                if str(vsi_import_var).strip() != "TempNA":
                    if not str(vsi_import_var).strip().__contains__("vsi-import"):
                        temp_cli = f"{temp_cli}\t\t\t\tvsi-import \"{str(vsi_import_var).strip()}\"\n"

                    if str(vsi_import_var).strip().__contains__("vsi-import"):
                        temp_cli = f"{temp_cli}\t\t\t\t{str(vsi_import_var).strip()}\n"

            temp_cli = f"{temp_cli}\t\t\texit\n"

        bgp_evpn_series_array = np.array(temp_df["BGP-Evpn"])

        if bgp_evpn_series_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tbgp-evpn\n"
            j = 0
            while j < bgp_evpn_series_array.size:
                if str(bgp_evpn_series_array[j]) != "TempNA":
                    if not str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        if str(bgp_evpn_series_array[j]).strip().upper() == "YES":
                            j += 1
                            continue

                        if str(bgp_evpn_series_array[j]).strip() != "YES":
                            temp_cli = f"{temp_cli}\t\t\t\t{str(bgp_evpn_series_array[j]).strip().lower()}\n"

                    if str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        bgp_evpn_series_array_list = str(bgp_evpn_series_array[j]).strip().split(",")
                        k = 0
                        while k < len(bgp_evpn_series_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{bgp_evpn_series_array_list[k].strip().lower()}\n"
                            k += 1
                j += 1

            temp_cli = f"{temp_cli}\t\t\texit\n"

        stp_var = str(temp_df.iloc[0, temp_df.columns.get_loc("STP")])
        if stp_var.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tstp\n"
            if str(stp_var).strip().upper() == "YES":
                pass
            if str(stp_var).strip().upper() != "YES":
                temp_cli = f"{temp_cli}\t\t\t\t{str(stp_var).strip().lower()}\n"
            temp_cli = f"{temp_cli}\t\t\texit\n"

        vsd_domain_name = str(temp_df.iloc[0, temp_df.columns.get_loc("Vsd-domain Name")])
        if vsd_domain_name.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tvsd-domain-name \"{str(vsd_domain_name).strip()}\"\n"

        vpls_status = str(temp_df.iloc[0, temp_df.columns.get_loc("VPLS Status")]).strip().lower()

        if vpls_status != 'tempna':
            temp_cli = (f"{temp_cli}\t\t\t{vpls_status}\n"
                        "\t\texit\n")

        if vpls_status == 'tempna':
            temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                        "\t\texit\n")
        result_cli = f"{result_cli}{temp_cli}"
        i += 1

    return result_cli


def modify_action_add_sequence_cli_for_vsd_controller_mapping_as_no(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for action modify add sequence for vsd controller mapping as no
    :param dataframe: Dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """
    result_cli = ""

    unique_vpls_ids = dataframe["VPLS ID"].unique().astype(float).astype(int)
    logging.info(
        f"{ip_node}: - unique vpls ids\n"
        f"{', '.join([str(x) for x in unique_vpls_ids])}"
    )

    i = 0
    while i < unique_vpls_ids.size:
        selected_vpls = unique_vpls_ids[i]
        temp_df = dataframe.loc[dataframe["VPLS ID"] == selected_vpls]

        logging.info(
            f"{ip_node}: - selected vpls {selected_vpls}\n"
            f"{temp_df.to_markdown()}"
        )

        temp_cli = f"\t\tvpls {selected_vpls}\n"

        additional_commands_array = np.array(temp_df["Additional Command"])

        if additional_commands_array.size > 0:
            j = 0
            while j < additional_commands_array.size:
                if str(additional_commands_array[j]) != "TempNA":
                    if not str(additional_commands_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t{str(additional_commands_array[j]).strip().lower()}\n"

                    if str(additional_commands_array[j]).strip().__contains__(","):
                        additional_commands_array_list = str(additional_commands_array[j]).strip().split(",")
                        k = 0
                        while k < len(additional_commands_array_list):
                            temp_cli = f"{temp_cli}\t\t\t{additional_commands_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1

        allow_ip_int_bind_array = np.array(temp_df["allow-ip-int-bind"])

        if allow_ip_int_bind_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tallow-ip-int-bind\n"
            j = 0
            while j < allow_ip_int_bind_array.size:
                if str(allow_ip_int_bind_array[j]).strip().upper() == "YES":
                    j += 1
                    continue

                if str(allow_ip_int_bind_array[j]) != "TempNA":
                    if not str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        temp_cli = f"{temp_cli}\t\t\t\t{str(allow_ip_int_bind_array[j]).strip().lower()}\n"

                    if str(allow_ip_int_bind_array[j]).strip().__contains__(","):
                        allow_ip_int_bind_array_list = str(allow_ip_int_bind_array[j]).strip().split(",")
                        k = 0
                        while k < len(allow_ip_int_bind_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{allow_ip_int_bind_array_list[k].strip().lower()}\n"
                            k += 1

                j += 1
            temp_cli = f"{temp_cli}\t\texit\n"

        vxlan_var = str(temp_df.iloc[0, temp_df.columns.get_loc("VXLAN Instance")])
        vni_var = str(temp_df.iloc[0, temp_df.columns.get_loc("VNI ID")])

        if (vxlan_var != "TempNA") and (vni_var != "TempNA"):
            temp_cli = (f"{temp_cli}\t\t\tvxlan instance {int(float(vxlan_var))} vni {int(float(vni_var))} create\n"
                        "\t\t\texit\n")
        bgp_var = str(temp_df.iloc[0, temp_df.columns.get_loc("BGP")])
        rt_export_var = str(temp_df.iloc[0, temp_df.columns.get_loc("RT-Export")])
        rt_import_var = str(temp_df.iloc[0, temp_df.columns.get_loc("RT-Import")])

        if bgp_var.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tbgp\n"
            if (rt_import_var.strip() != "TempNA") and (rt_export_var.strip() != "TempNA"):
                temp_cli = f"{temp_cli}\t\t\t\t{bgp_var}\n\t\t\t\troute-target export {rt_export_var}\n\t\t\t\troute-target import {rt_import_var}\n"

            elif (rt_export_var.strip() != "TempNA") and (rt_import_var.strip() == "TempNA"):
                temp_cli = f"{temp_cli}\t\t\t\t{bgp_var}\n\t\t\t\troute-target export {rt_export_var}\n"

            elif (rt_export_var.strip() == "TempNA") and (rt_import_var.strip() != "TempNA"):
                temp_cli = f"{temp_cli}\t\t\t\t{bgp_var}\n\t\t\t\troute-target import {rt_import_var}\n"

            temp_cli = f"{temp_cli}\t\t\texit\n"

        bgp_evpn_series_array = np.array(temp_df["BGP-Evpn"])

        if bgp_evpn_series_array.size > 0:
            temp_cli = f"{temp_cli}\t\t\tbgp-evpn\n"
            j = 0
            while j < bgp_evpn_series_array.size:
                if str(bgp_evpn_series_array[j]) != "TempNA":
                    if not str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        if str(bgp_evpn_series_array[j]).strip().upper() == "YES":
                            j += 1
                            continue

                        if str(bgp_evpn_series_array[j]).strip() != "YES":
                            temp_cli = f"{temp_cli}\t\t\t\t{str(bgp_evpn_series_array[j]).strip().lower()}\n"

                    if str(bgp_evpn_series_array[j]).strip().__contains__(","):
                        bgp_evpn_series_array_list = str(bgp_evpn_series_array[j]).strip().split(",")
                        k = 0
                        while k < len(bgp_evpn_series_array_list):
                            temp_cli = f"{temp_cli}\t\t\t\t{bgp_evpn_series_array_list[k].strip().lower()}\n"
                            k += 1
                j += 1

            temp_cli = f"{temp_cli}\t\t\texit\n"

        stp_var = str(temp_df.iloc[0, temp_df.columns.get_loc("STP")])
        if stp_var.strip() != "TempNA":
            temp_cli = f"{temp_cli}\t\t\tstp\n"
            if str(stp_var).strip().upper() == "YES":
                pass
            if str(stp_var).strip().upper() != "YES":
                temp_cli = f"{temp_cli}\t\t\t\t{str(stp_var).strip().lower()}\n"
            temp_cli = f"{temp_cli}\t\t\texit\n"

        vpls_status = str(temp_df.iloc[0, temp_df.columns.get_loc("VPLS Status")]).lower().strip()

        if vpls_status != 'tempna':
            temp_cli = (f"{temp_cli}\t\t\t{vpls_status}\n"
                        "\t\texit\n")

        if vpls_status == 'tempna':
            temp_cli = (f"{temp_cli}\t\t\tno shutdown\n" +
                        "\t\texit\n")
        result_cli = f"{result_cli}{temp_cli}"

        i+=1

    return result_cli


def modify_action_cli_for_add_sequence(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for action modify
    :param dataframe: Dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """

    temp_cli = ''

    filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_yes = dataframe.loc[dataframe['VSD Controller Mapping'].str.strip().str.upper().str.upper() == 'YES']
    logging.info(
        f"{ip_node}: - filtered dataframe with modify action vsd controller mapping as yes\n"
        f"{filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_yes.to_markdown()}"
    )

    filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_no = dataframe.loc[dataframe['VSD Controller Mapping'].str.strip().str.upper().str.upper() == 'NO']
    logging.info(
        f"{ip_node}: - filtered dataframe with add action vsd controller mapping as no\n"
        f"{filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_no.to_markdown()}"
    )

    if filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_yes.shape[0] > 0:
        temp_cli = f"{temp_cli}\n{modify_action_add_sequence_cli_for_vsd_controller_mapping_as_yes(filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_yes, ip_node)}"

    if filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_no.shape[0] > 0:
        temp_cli = f"{temp_cli}\n{modify_action_add_sequence_cli_for_vsd_controller_mapping_as_no(filtered_dataframe_with_modify_action_add_sequence_vsd_controller_mapping_as_no, ip_node)}"

    return temp_cli



def modify_action_cli(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Function to add cli for action modify
    :param dataframe: Dataframe containing the input from design_input_workbook
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :return: cli (str): cli containing commands of the design_input_workbook
    """

    add_sequence_filtered_dataframe = dataframe.loc[dataframe['Sequence'].str.strip().str.upper().str.endswith('ADD')]

    logging.info(
        f"{ip_node}: - filtered dataframe with add sequence\n"
        f"{add_sequence_filtered_dataframe.to_markdown()}"
    )
    temp_cli = ''

    if add_sequence_filtered_dataframe.shape[0] > 0:
        temp_cli = f"{temp_cli}{modify_action_cli_for_add_sequence(add_sequence_filtered_dataframe, ip_node)}"

    modify_sequence_filtered_dataframe = dataframe.loc[dataframe['Sequence'].str.strip().str.upper().str.endswith('MODIFY')]

    logging.info(
        f"{ip_node}: - filtered dataframe with modify sequence\n"
        f"{modify_sequence_filtered_dataframe.to_markdown()}"
    )

    if modify_sequence_filtered_dataframe.shape[0] > 0:
        # temp_cli = f"{temp_cli}{modify_action_cli_for_modify_sequence(modify_sequence_filtered_dataframe, ip_node)}"
        pass

    delete_sequence_filtered_dataframe = dataframe.loc[dataframe['Sequence'].str.strip().str.upper().str.endswith('DELETE')]

    logging.info(
        f"{ip_node}: - filtered dataframe with delete sequence\n"
        f"{delete_sequence_filtered_dataframe.to_markdown()}"
    )

    if delete_sequence_filtered_dataframe.shape[0] > 0:
        # temp_cli = f"{temp_cli}{modify_action_cli_for_delete_sequence(delete_sequence_filtered_dataframe, ip_node)}"
        pass

    return temp_cli


def main_func(dataframe: pd.DataFrame, ip_node: str) -> str:
    """
    Main function for VPLS-1 cli preparation
    :param ip_node: ip_node for which the VPLS_ID Cli is being prepared
    :param dataframe: Dataframe containing the input from design_input_workbook
    :return: cli (str): cli containing commands of the design_input_workbook
    """
    try:
        cli = ''

        dataframe = dataframe.where(~dataframe.isna(), "TempNA")

        logging.info(
            f"{ip_node}: - new dataframe after filling NA with \"TempNA\"\n"
            f"{dataframe.to_markdown()}"
        )

        filtered_df_for_vsd_domain_creation = dataframe.loc[(~dataframe['VSD Domain(Exist/New)'].str.strip().str.contains("TempNA")) &
                                                            (dataframe['VSD Domain(Exist/New)'].str.strip().str.upper().str.contains("NEW"))]

        logging.info(
            f"{ip_node}: - filtered df for vsd domain creation\n"
            f"{filtered_df_for_vsd_domain_creation.to_markdown()}"
        )

        if filtered_df_for_vsd_domain_creation.shape[0] > 0:
            cli = f"{cli}{vsd_domain_creation_cli_func(filtered_df_for_vsd_domain_creation, ip_node)}"

        cli = f"{cli}config service\n"
        filtered_df_for_action_add = dataframe.loc[(dataframe['Action'].str.strip() != "TempNA") & (dataframe['Action'].str.strip().str.upper().str.endswith('ADD'))]

        logging.info(
            f"{ip_node}: - filtered df for action add\n"
            f"{filtered_df_for_action_add.to_markdown()}"
        )

        filtered_df_for_action_modify = dataframe.loc[(dataframe['Action'].str.strip() != "TempNA") & (dataframe['Action'].str.strip().str.upper().str.endswith('MODIFY'))]
        logging.info(
            f"{ip_node}: - filtered df for action modify\n"
            f"{filtered_df_for_action_modify.to_markdown()}"
        )

        if filtered_df_for_action_add.shape[0] > 0:
            cli = f"{cli}{add_action_cli(filtered_df_for_action_add, ip_node)}\n"

        if filtered_df_for_action_modify.shape[0] > 0:
            cli = f"{cli}{modify_action_cli(filtered_df_for_action_modify, ip_node)}"

        cli = f"{cli}exit all\n"

        print('\n'.join(cli))
        logging.info(
            "VPLS-2 cli preparation completed successfully!\n" +
            f"{'\n'.join(cli)}"
        )

    except Exception as e:
        import traceback
        logging.error(f"{traceback.format_exc()}\n"
            "Exception occurred!\n"
            f"Title ===> {e.__class__.__name__}\n\t"
            f"Description ===> {str(e)}"
        )
        cli = ""

    finally:
        return cli
