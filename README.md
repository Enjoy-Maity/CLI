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

   * sdp details are missing for S.No. ->
7. Filter out the non-blank '_mesh sdp_' inputs from main df & further filter out dataframe for **sdp** New/Exist cases using "**_SDP(New/Exist)_**".  Now,

   ```
   If length of dataframe_sdp_new > 0
   	Then, Check the length of sdp_section_dataframe from NOKIA.pickle
   		if len(sdp_section_df) == 0:
   			raise Error
   		if len(sdp_section_df) != 0:
   			then, further check for the existence of sdp_variable from dataframe_sdp_new in 																																																																				        sdp_section_df
   			if given sdp_variable_not_found:
   				raise Error
   ```
8. Need to add template checks for Action Modify, Sequence: - Delete and Modify -----> (need to be added for delete sequence too)

   * For the sequence Modify we need to add checks for 'Sap Status' and 'Mesh Status', to contain two unique statuses separated with comma (',').
   * For the sequence Delete, we need to check for atleast one entry for field -> 'Mesh-sdp' or 'Sap/Lag' to be non-blank.

#### 2. VPLS - 2

1. VPLS ID must be non blank
2. '*VPLS Controller Mapping*' should be non-blank
3. VPLS Name and Vsd-domain Name should not have spaces in between.
4. VPLS Name should be non-blank for Action '*A:Add*'
5. VPLS ID should be unique for Action '*A:Add*' -----—removed in the latest code --- need to be checked
6. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice versa.
7. Check whether any of the entry for the 'VSD Controller Mapping' is left empty or not.
8. If 'VSD Controller Mapping' Input is '*Yes*', then 'VSD Domain Name', 'VSD description' and 'VSD Type' should be non-blank. If Input is '*No*' then respective parameter should be blank.
9. Character length for the input should not exceed 32-characters for the fields '*rt-export*', '*rt-import*', '*VSI-Export*' and '*VSI-Import*'.
10. Add condition for '*VPLS Controller Mapping*' with 'Yes' should have non-blank entry in column _'VSD Domain(Exist/New)'_  with values only '*New*' or '*Exist*'.
11. 

# **Node Checks**

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

Handling of below mentioned points are developed considering only _Sequence_ "**_ADD_**", irrespective of _Action_.
In future, if handling of _Sequence_ "_**MODIFY**_" and "_**DELETE**_", cases will come then, we need to review development of these points.

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- ***vpls** {VPLS ID}*

   * If found then "Action:Add VPLS ID Clash found for S.No." ==> ', '.join(list of S.No.)


2. All list of elements for '*VPLS ID*' in action 'Modify/Delete' dataframe need to be checked in running node configuration (.txt file)-- "vpls **{***VPLS ID***}**"

   * If not found then "Action:Modify/Delete VPLS ID not found for S.No." ==> ', '.join(list of S.No.)


3. Check for "vpls name {*vpls name}*" regular expression in running node configuration from 'VPLS Name' (Action:Add only).

   * "VPLS Name Clash found for S.No." ==> ', '.join(list of S.No.)


4. If '*VSD Controller Mapping*' value is '*Yes*', check for "domain {*Vsd-domain Name*}" in running node configuration from '*Vsd-domain Name*' by filtering _domain_ and _vsd-domain_ chunk for all Actions.

   * "VSD Domain Name configuration not found for S.No. ==> ', '.join(list of S.No.)" (For "_**domain**_" chunk)
   * "VSD Domain Name binding already found for S.No. ==> ', '.join(list of S.No.)" (For "_**vsd-domain**_" chunk)


5. Check for 'route-distinguisher *{int}:{int}*' from 'BGP' field in running node configuration.
   (For Action:Add only) Filter all the lines starting with 'route-distinguisher' and check for it's non-existence, if found:-

   * "Route-distinguisher Clash found for S.No. ==> ', '.join(list of S.No.)"


6. If '*VSI-Export*' or '*VSI-Import*' field is non-blank, then search for the presence of the field inputs in "echo \"Policy Configuration\" " chunk by further filtering the chunk with starting line *policy-statement {*input variable*}. If match not found then

   * "VSI Export/Import policy is not configured for S.No. ==> ', '.join(list of S.No.)"
   

7. If _VNI ID_ is non-blank then check for presence of _VNI ID_ in "echo \"Service Configuration\" " chunk starting with _**vxlan instance**_ string. If match found then,

   * "VNI ID Clash found for S.No. ==> ', '.join(list of S.No.)"


# **CLI Preparation**

## Nokia

#### 1. VPLS -1

1. The CLI Preparation is divided into Action: Add, Modify, Delete; and for switch and router.


2. For action *Add*, we have to check for the non-empty enteries like description, sap, etc. and make the cli accordingly for node type 'Router' or 'Switch'.


3. For action "_**Action:Modify**_", there are sub-categories of Sequence 'Add', 'Modify' and 'Delete.
   For all the node types 'Switch' or 'Router', the cli is similar.
   1. For sequence 'Add', we can it is almost similar to Action 'Add', only difference is that, for configuring the VPLS, we just need to add 'VPLS ID'.
   2. For sequence 'Modify', we need two enteries for 'Mesh Status' and 'Sap Status', depending upon data provided in 'Mesh-sdp', and 'Sap/Lag' field.
   3. For sequence 'Delete', we need enteries only in 'Mesh-sdp', and 'Sap/Lag' fields.


4. The final vpls status will be determined by the column '**_VPLS Status_**'.


#### 2. VPLS - 2

1. First filter out the section of design input(dataframe) where \"VSD Domain(Exist/New)\" is given as \"**New**\" irrespective of input in \"_Action_\" column.
   1. create the cli for the filtered dataframe with admin save at the end, after cli for all the enteries are created.
2. For \"**Action:Add**\", filter the design input (dataframe):
   1. filter the dataframe for \"**_VSD Controller Mapping_**\" with input as "**Yes**" and create a method to create cli for the filtered dataframe.
      1. create the list of unique vpls id enteries for the filtered dataframe.
      2. iterate through a loop of the unique vpls id enteries and check for non-blank fields and create temp_df for each unique vpls id.
      3. If the \"**_BGP_**\" is non-blank, then take the entry only for first row of the temp_df.
      4. Similarly, when _BGP_ column input is given, take the entry only for first row of the temp_df for columns \"**_VSI-Export_**\" and \"**_VSI-Import_**\" if given, add commands in the cli.
      5. Get all enteries for the column \"**_allow-ip-int-bind_**\" from the temp_df and add commands in the cli.
      6. Get all enteries for the column \"**_BGP-Evpn_**\" from the temp_df and add commands in the cli.
         1. Check if there is "," in each row and split the row on "," and add commands in the cli.
         2. If the value is "Yes" then just enter the _**bgp-evpn**_ hierarchy and make an exit.
      7. Add the command for adding VSD Domain Name binding in the cli.
      8. Add the cli to the result_cli variable.
   2. filter the dataframe for \"**_VSD Controller Mapping_**\" with input as "**No**" and create a method to create cli for the filtered dataframe.
      1. create the list of unique vpls id enteries for the filtered dataframe.
      2. iterate through a loop of the unique vpls id enteries and check for non-blank fields and create temp_df for each unique vpls id.
      3. If the \"**_BGP_**\" is non-blank, then take the entry only for first row of the temp_df.
      4. Similarly, when _BGP_ column input is given, take the entry only for first row of the temp_df for columns \"**_VSI-Export_**\" and \"**_VSI-Import_**\" if given, add commands in the cli.
      5. Get all enteries for the column \"**_allow-ip-int-bind_**\" from the temp_df and add commands in the cli.
      6. Get all enteries for the column \"**_BGP-Evpn_**\" from the temp_df and add commands in the cli.
         1. Check if there is "," in each row and split the row on "," and add commands in the cli.
         2. If the value is "Yes" then just enter the _**bgp-evpn**_ hierarchy and make an exit.
      7. Add the cli to the result_cli variable.
3. For \"**Action:Modify**\", filter the design input (dataframe):
   1. Filter the dataframe for \"**_VSD Controller Mapping_**\" with input as "**Yes**" and create a method to create cli for the filtered dataframe.
      1. Create a list of unique vpls id enteries for the filtered dataframe.
      2. Iterate through a loop of the unique vpls id enteries and check for non-blank fields and create temp_df for each unique vpls id.
         1. If the \"**_BGP_**\" is non-blank, then take the entry only for first row of the temp_df.
         2. Similarly, when _BGP_ column input is given, take the entry only for first row of the temp_df for columns \"**_VSI-Export_**\" and \"**_VSI-Import_**\" if given, add commands in the cli.
         3. Add the cli to the result_cli variable.
# **Post Running Config Checks**

## Nokia

#### 1. VPLS - 1

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in post running node configuration (.txt file)-- vpls **{***VPLS ID***}**

   * If not found then "Action:Add VPLS ID not found for S.No." ==> ', '.join(list of S.No.)
   

2. All list of elements for '*VPLS ID*' in action 'Modify' dataframe need to be checked in post running node configuration (.txt file)-- "vpls **{***VPLS ID***}**"

   * If not found then "Action:Modify VPLS ID not found for S.No." ==> ', '.join(list of S.No.)
   

3. Check for "vpls name ***{vpls name}***" regular expression in post running node configuration from 'VPLS Name' from filter for '*Action :Add*' dataframe. ('VPLS Name' should be bind with respective VPLS ID given as input)

   * "VPLS Name not found for S.No." ==> ', '.join(list of S.No.)
   

4. If field for '*Mesh-sdp*' is non-blank, check for '*sdp* ***{variable}***' where variable comes for '*Mesh-sdp*' field in the form like --> '*mesh-sdp 42:3019*', here variable = 42
   For(sequence Add only), we need to check, the existence of *sdp* in both cases of sdp (exists/new) as per input Template,If given sdp does not exists, then we need to add below reason in result dictionary

   * "Given SDP not found for S.No. " ===> ', '.join(list of S.No.)

   if given mesh-sdp does not exist in respective 'VPLS ID' then we need to add below reason to result_dictionary.

   * "Given Mesh-SDP not found for S.No. " ===> ', '.join(list of S.No.)

   For (sequence 'Modify' only)  we need to check, the existence of *sdp* in both cases of sdp (exists/new) as per input Template,If given sdp does not exists, then we need to add below reason in result dictionary

   * "Given SDP not found for S.No. " ===> ', '.join(list of S.No.)

   if given mesh-sdp does not exist in respective 'VPLS ID' then we need to add below reason to result_dictionary.

   * "Given Mesh-SDP not found for S.No. " ===> ', '.join(list of S.No.)

   For (sequence 'Delete' only)  we need to check, the existence of *sdp* in both cases of sdp (exists/new) as per input Template,If given sdp does not exists, then we need to add below reason in result dictionary

   * "Given SDP not found for S.No. " ===> ', '.join(list of S.No.)

   if given mesh-sdp exists in respective 'VPLS ID' then we need to add below reason to result_dictionary.

   * "Given Mesh-SDP not removed for S.No. " ===> ', '.join(list of S.No.)


5. If field for '*sap*' is non-blank, then check for given sap entry (with or without lag) in respective vpls id. If entry not found then, add below reason in result_dictionary for (sequence add and modify):

   * "Given Sap entry not configured for S.No." ===> ', '.join(list of S.No.)

   if given sap entry exists in respective 'VPLS ID' then we need to add below reason to result_dictionary (for sequence delete only):

   * "Given Sap not removed for S.No. " ===> ', '.join(list of S.No.)
   

6. Given VPLS ID status need to be check for complete main dataframe from additional command output in post running backup config. If '*Opr*' status found to be down, then add below reason to result_dictionary:
   additional command; **show service service-using vpls**

   * "given VPLS id found to be 'Down' state for S.No."===> ', '.join(list of S.No.)
