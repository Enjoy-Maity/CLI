# **GUI**

1. Ask the user for the Host details workbook at first and get the unique vendor list.
2. Show message for the user regarding the Session ===> 'Do you want to proceed the old session or start a new session?' and create buttons for the new session.

# Database Manager

1. Create a database manager for creating the sessions and managing the status of tasks.
2. It should be able to delete the old session older than 15 hours.
3. Create a database with dynamic number of columns for sheet creater (The columns are dynamic according to vendor).
4. Put the status related to tasks in the session database.
5. There will be 4 columns "Vendor, Template Checks, Node Checks, CLI Preparation" and three possible values for "Template Checks, Node Checks, CLI Preparation", that are "Unsuccessful, Successful, Blank Space"

# Sheet Creater

1. First check for the the pickle creation of pickle file for host detail with the creation date.
2. If there is any pickle present and it is of today's date and check for the data with current selected data.
3. If the pickle is not of today's date, then delete the pickle and create the new pickle.
4. If there is new session either organically or user induced new session then
   * If the session is the first session of the day, then delete the older pickle
   * If the session is new and user induced, then check for the host details
     * If there is any Formal session existing then delete the existing session to start a new
5. Block the running of the sheet creater if any of the template checks is successful.
6. Raise exceptions in case all of the host details in the uploaded sheet does not match the loaded pickle.
7. Raise exception if there is any sheet extra present in the '*Input Design Sheet*' but not in uploaded host details.
8. The templates must be kept in folder "{Parent folder of parent folder of uploaded Host Details}/Design_Templates".

# **Template Checks**

Template Checks performs all the checks in the design input workbooks

## General Checks

1. Check for all the vendor specific input workbooks present in the same path hierarchy where the host details workbook is located.
2. Check for all the node ip sheets are present in the host details workbook worksheet for selected vendor (raise exception, don't raise warning messagebox.)
3. If count for the unique node ips are different raise exception message pop-up(no warning), else proceed without any pop-ups.
4. Check for the presence of input data for atleast one section for the selected worksheet, if not present for some worksheet then raise exception.
5. Check for blanks for the 'Action' column for each section.
6. If there are no banks found in 'Action' column for any of the section of the selected node ip input worksheet, then check for the value to in range of the list *['A:Add', 'A:Delete', 'A:Modify']*.
7. Created the Pickle for the structure :-
8. { node_ip : {Section: df}}

##### The structure for the error handling is :

{ node_ip : {

    section : [list of serial numbers where there is any error found]}

    }

## Checks for the present nodes in selected vendor input workbook

### Nokia Checks

#### Error Handling Structure

The error handling is handled via the structure given below :

{
	node_ip : 	{
			Section1:  "Could Not Parse the data for Specific Template Checks",
			Section2 :   {reason : [list of serial numbers pertaining the errors]
		}
	}
}

#### 1. VPLS - 1

1. VPLS ID,  Sequence, 'MPBN Node Type' must be non blank
2. VPLS Name should not have spaces in between
3. VPLS Name should be non-blank for Action '*A:Add*'
4. VPLS ID should be unique for Action '*A:Add*'
5. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice-versa.

#### 2. VPLS - 2

1. VPLS ID must be non blank
2. '*VPLS Controller Mapping*' should be non-blank
3. VPLS Name and Vsd-domain Name should not have spaces in between.
4. VPLS Name should be non-blank for Action '*A:Add*'
5. VPLS ID should be unique for Action '*A:Add*'
6. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice-versa.
7. Check whether any of the entry for the  'VSD Controller Mapping' is left empty or not.
8. If 'VSD Controller Mapping' Input is '*Yes*', then 'VSD Domain Name', 'VSD description' and 'VSD Type' should be non-blank. If Input is '*No*' then respective parameter should be blank.
9. Character length for the input should not exceed 32-characters for the fields '*rt-export*', '*rt-import*', '*VSI-Export*' and '*VSI-Import*'.
10. 

# Node Checks

Node Checks performs all the Node related checks from the Running_Config_Backups for the mentioned Nodes in uploaded Host Details.

## General Checks

1. 'Running_Config_Backup' folder to be present and all the host name pre config backups must be present.

#### 1. VPLS - 1

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- **vpls {***VPLS ID***}**
2. Check for ""vpls name {*vpls name}*"" regular expression in running node configuration from 'VPLS Name'
3. If field for '*Mesh-sdp*' is non-blank, check for '*sdp `<variable>`*' where variable comes for '*Mesh-sdp*' field in the form like --> '*mesh-sdp 42:3019*', here variable = 42.

#### 2. VPLS - 2

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- ***vpls** {VPLS ID}*
2. Check for ""vpls name {*vpls name}*"" regular expression in running node configuration from 'VPLS Name'
3. If '*VSD Controller Mapping*' value is '*Yes*', check for ""domain {*Vsd-domain Name*}""" in running node configuration from '*Vsd-domain Name*'.
4. Check for 'route-distinguisher *{int}:{int}*' from 'BGP' field in running node configuration.
5. If '*VSI-Export*' or '*VSI-Import*' field is non-blank, then message to be displayed 'To ensure it's configuration as prerequisite'.
