# **Checks for the Template Checks**

1. Check for all the vendor specific input workbooks present in the same path hierarchy where the host details workbook is located.
2. Check for all the node ip sheets are present in the host details workbook worksheet for selected vendor (Don't raise exception, raise warning messagebox.)
3. If count for the unique node ips are different raise warning message pop-up(no exception), else proceed without any pop-ups.
4. Check for the presence of input data for atleast one section for the selected worksheet, if not present for some worksheet then raise exception.

## Checks for the present nodes in selected vendor input workbook

### General Checks

1. Check for blanks for the 'Action' column for each section.
2. If there are no banks found in 'Action' column for any of the section of the selected node ip input worksheet, then check for the value to in range of the list *['A:Add', 'A:Delete', 'A:Modify']*.

Created the Pickle for the structure :-

    { node_ip : {

    Section: df

    }

}

The structure of the dictionary for general

{node_ip : {

    Action: {

    Section: filtered_df }}}}


The structure for the error handling is :

{ node_ip : {

    section : [list of serial numbers where there is any error found]}

}
