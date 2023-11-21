# **Template Checks**

## General Checks

1. Check for all the vendor specific input workbooks present in the same path hierarchy where the host details workbook is located.
2. Check for all the node ip sheets are present in the host details workbook worksheet for selected vendor (Don't raise exception, raise warning messagebox.)
3. If count for the unique node ips are different raise warning message pop-up(no exception), else proceed without any pop-ups.
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

1. VPLS ID must be non blank
2. VPLS Name should be non-blank for Action '*A:Add*'
3. VPLS ID should be unique for Action '*A:Add*'
4. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice-versa.

#### 2. VPLS - 2

1. VPLS ID must be non blank
2. VPLS Name should be non-blank for Action '*A:Add*'
3. VPLS ID should be unique for Action '*A:Add*'
4. List of unique elements (VPLS ID) of Action '*A:Add*' Cases should not match with unique elements of Action '*A:Modify/Delete*' cases and vice-versa.
5. Check whether any of the entry for the  'VSD Controller Mapping' is left empty or not.
6. If 'VSD Controller Mapping' Input is '*Yes*', then 'VSD Domain Name', 'VSD description' and 'VSD Type' should be non-blank. If Input is '*No*' then respective parameter should be blank.
7. Character length for the input should not exceed 32-characters for the fields '*rt-export*', '*rt-import*', '*VSI-Export*' and '*VSI-Import*'.


# Node Checks

#### 1. VPLS - 1

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- **vpls '`<VPLS ID>`'  **
2. Check for ""vpls*name `<vpls name>`"" regular expression in running node configuration from 'VPLS Name'
3. If field for '*Mesh-sdp*' is non-blank, check for '*sdp `<variable>`*' where variable comes for '*Mesh-sdp*' field in the form like --> '*mesh-sdp 42:3019*', here variable = 42.

#### 2. VPLS - 2

1. All list of elements for '*VPLS ID*' in action '*Add*' dataframe need to be checked in running node configuration (.txt file)-- **vpls '`<VPLS ID>`'  **
2. Check for ""vpls*name `<vpls name>`"" regular expression in running node configuration from 'VPLS Name'
3. If '*VSD Controller Mapping*' value is '*Yes*', check for ""domain "`<Vsd-domain Name>`""" in running node configuration from '*Vsd-domain Name*'.
4. Check for 'route-distinguisher `<int>`:`<int>`' from 'BGP' field in running node configuration.
5. If '*VSI-Export*' or '*VSI-Import*' field is non-blank, then message to be displayed 'To ensure it's configuration as prerequisite'.
