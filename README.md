# **GUI**

1. Ask the user for the Host details workbook at first and get the unique vendor list.
2. Show a message for the user regarding the Session ===> 'Do you want to proceed the old session or start a new session?' and create buttons for the new session.

# Database Manager

1. Create a database manager for creating the sessions and managing the status of tasks.
2. It should be able to delete the old session older than 15 hours.
3. Create a database with dynamic number of columns for sheet creater (The columns are dynamic, according to vendor).
4. Put the status related to tasks in the session database.
5. There will be 4 columns "Vendor, Template Checks, Node Checks, CLI Preparation" and three possible values for "Template Checks, Node Checks, CLI Preparation," that are "Unsuccessful, Successful, Blank Space"

# Sheet Creater

1. First check for the pickle creation of pickle file for host detail with the creation date.
2. If there is any pickle present and, it is of today's date and check for the data with current selected data.
3. If the pickle is not of today's date, then delete the pickle and create the new pickle.
4. If there is a new session either organically or user induced new session then
   * If the session is the first session of the day, then delete the older pickle
   * If the session is new and user induced, then check for the host details
     * If there is any Formal session existing, then delete the existing session to start a new
5. Block the running of the sheet creater if any of the template checks is successful.
6. Raise exceptions in case all the host details in the uploaded sheet do not match the loaded pickle.
7. Raise exception if there is any sheet extra present in the '*Input Design Sheet*' but not in uploaded host details.
8. The templates must be kept in folder "{Parent folder of parent folder of uploaded Host Details}/Design_Templates."

# **Template Checks**

Template Checks perform all the checks in the design input workbooks

## General Checks

1. Check for all the vendor-specific input workbooks present in the same path hierarchy where the host details workbook is located.
2. Check for all the node ip sheets are present in the host details workbook worksheet for selected vendor (raise exception, don't raise warning messagebox.)
3. If count for the unique node ips are different, raise exception message pop-up(no warning), else proceed without any pop-ups.
4. Check for the presence of input data for at least one section for the selected worksheet, if not present for some worksheet then raise exception.
5. Check for blanks for the 'Action' column for each section.
6. If there are no banks found in 'Action' column for any of the sections of the selected node ip input worksheet, then check for the value to in range of the list *['A:Add', 'A:Delete', 'A:Modify']*.
7. Created the Pickle for the structure: -{ node_ip: {Section: df}}

##### The structure for the error handling is :

{
    node_ip : {
                    section : [list of serial numbers where there is any error found]}
    }

## Checks for the present nodes in selected vendor input workbook

### Nokia Checks

#### Error Handling Structure

The error handling is handled via the structure given below :

{
	node_ip :	{
			Section1: "Could Not Parse the data for Specific Template Checks",
			Section2: {reason : [list of serial numbers pertaining the errors]
		}
	}
}

#### 1. VPLS - 1

1. VPLS ID,  Sequence, 'MPBN Node Type' must be non blank
2. VPLS Name should not have spaces in between
3. VPLS Name should be non-blank for Action '*A:Add*'
4. VPLS ID should be unique for Action '*A:Add*' -----—removed in the latest code
5. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice versa.
6. Filter out the non-blank '_mesh sdp_' inputs from main df & further check if there's any blank input for column - "**_SDP(New/Exist)_**".
   1. sdp details are missing for S.No. -> 

#### 2. VPLS - 2

1. VPLS ID must be non blank
2. '*VPLS Controller Mapping*' should be non-blank
3. VPLS Name and Vsd-domain Name should not have spaces in between.
4. VPLS Name should be non-blank for Action '*A:Add*'
5. VPLS ID should be unique for Action '*A:Add*' -----—removed in the latest code
6. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice versa.
7. Check whether any of the entry for the 'VSD Controller Mapping' is left empty or not.
8. If 'VSD Controller Mapping' Input is '*Yes*', then 'VSD Domain Name', 'VSD description' and 'VSD Type' should be non-blank. If Input is '*No*' then respective parameter should be blank.
9. Character length for the input should not exceed 32-characters for the fields '*rt-export*', '*rt-import*', '*VSI-Export*' and '*VSI-Import*'.
10. 

# Node Checks

Node Checks performs all the Node-related checks from the Running_Config_Backups for the mentioned Nodes in uploaded Host Details.

## General Checks

1. 'Running_Config_Backup' folder to be present and all the host name pre config backups must be present.

## Checks for the present nodes in selected vendor

### Nokia Config Checks

#### 1. VPLS - 1

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- vpls **{***VPLS ID***}**

   * If found then "Action:Add VPLS ID Clash for S.No." ==> ', '.join(list of S.No.)
2. All list of elements for '*VPLS ID*' in action 'Modify/Delete' dataframe need to be checked in running node configuration (.txt file)-- "vpls **{***VPLS ID***}**"

   * If not found then "Action:Modify/Delete VPLS ID not found for S.No." ==> ', '.join(list of S.No.)
3. Check for "vpls name **{*****vpls name****}***" regular expression in running node configuration from 'VPLS Name' from filter for '*Action :Add*' dataframe.

   * "VPLS Name Clash found for S.No." ==> ', '.join(list of S.No.)
4. If field for '*Mesh-sdp*' is non-blank, check for '*sdp **{variable}***' where variable comes for '*Mesh-sdp*' field in the form like --> '*mesh-sdp 42:3019*', here variable = 42.

   Here we need to check, the creation of *sdp*(exists/not exists),then we need to check the given mesh-sdp in running config. If given sdp exists(), then we need to skip that section for CLI creation and if given mesh-sdp exists then we need to add reason to result_dictionary.

   * create a database maintaining sdp existence status.
   * "Given Mesh-SDP clash found for S.No. " ===> ', '.join(list of S.No.)
   * "Given Mesh-SDP not found for S.No. " ===> ', '.join(list of S.No.)
5. If field for '*sap*' is non-blank and given string is not containing *lag,* then check for given port-details existence in running configuration, if port-detail mode is configured as "access", then sap entry should be given with "vlan" as an input in template (check for ':' in the design input) and given sap entry should not be clashed with any other "vpls".

   * "Port-Detail not found or configured as access and wrong Sap entry found in template for S.No." ===> ', '.join(list of S.No.)
   * "Given Sap entry (without LAG) clash found for S.No." ===> ', '.join(list of S.No.)
6. If field for '*sap*' is non-blank and given string contains *lag,* then check for given lag-details existence in running configuration, if lag-detail mode is configured as "access", then sap entry should be given with "vlan" as an input in template and given sap entry should not be clashed with any other "vpls".

   * "Lag not found or configured as access and wrong Sap entry found in template for S.No." ===> ', '.join(list of S.No.)
   * "Given Sap entry (with LAG) clash found for S.No." ===> ', '.join(list of S.No.)

#### 2. VPLS - 2

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- ***vpls** {VPLS ID}*
2. Check for ""vpls name {*vpls name}*"" regular expression in running node configuration from 'VPLS Name'
3. If '*VSD Controller Mapping*' value is '*Yes*', check for ""domain {*Vsd-domain Name*}""" in running node configuration from '*Vsd-domain Name*'.
4. Check for 'route-distinguisher *{int}:{int}*' from 'BGP' field in running node configuration.
5. If '*VSI-Export*' or '*VSI-Import*' field is non-blank, then message to be displayed 'To ensure its configuration as prerequisite'.

# CLI Preparation

## Nokia

#### 1. VPLS -1
