import pandas as pd
from CustomException import CustomException
from tkinter import messagebox

def vsd_cont_mappin_yes(cli,row_dictionary,key):
    if((len(row_dictionary['vsd-domain']) == 0) or (row_dictionary['vsd-domain'] == "TempNA")):
        raise CustomException(" VSD Domain Missing!",f"Kindly Check 'VPLS ID' Column for 'VPLS' Section in {key} node in selected workbook!")

    else:
        cli = f"{cli}\
            vpls {row_dictionary['VPLS ID']} name {row_dictionary['VPLS Name']} customer 1 create\n"
        
        if((len(row_dictionary['allow-ip-int-bind']) > 0) and (row_dictionary['allow-ip-int-bind'] != "TempNA")):
            cli = f"{cli}\
                allow-ip-int-bind\n\
                    {row_dictionary['allow-ip-int-bind']}\n\
                        exit\n"
        
        if((len(row_dictionary['BGP']) > 0) and (row_dictionary['BGP'] != "TempNA")):
            cli = f"{cli}\
                bgp\n"

            if((len(row_dictionary['vsi-export']) > 0) and (row_dictionary['vsi-export'] != "TempNA")):
                cli = f"{cli}\
                        vsi-export {row_dictionary['vsi-export']}\n"
            
            if((len(row_dictionary['vsi-import']) > 0) and (row_dictionary['vsi-import'] != "TempNA")):
                cli = f"{cli}\
                    vsi-import {row_dictionary['vsi-import']}\n"
            
            cli = f"{cli}\
                        exit\n"
        
        if(row_dictionary['bgp-evpn'].upper() == "YES"):
            cli = f"{cli}\
                    bgp-evpn\n\
                        exit\n"
        
        if((len(row_dictionary['bgp-evpn']) > 0) and ((row_dictionary['bgp-evpn'].strip().upper() != "YES") and (row_dictionary['bgp-evpn'] != "TempNA"))):
            cli = f"{cli}\
                bgp-evpn\n\
                    {row_dictionary['bgp-evpn']}\n\
                        no shutdown\n\
                            exit\n\
                                exit\n"

        if((len(row_dictionary['stp']) > 0) and (row_dictionary['stp'] != "TempNA")):
            cli = f"{cli}\
                stp\n\
                    {row_dictionary['stp']}\n\
                        exit\n"
        
        if((len(row_dictionary['vsd-domain']) > 0) and (row_dictionary['vsd-domain'] != "TempNA")):
            cli = f"{cli}\
                vsd-domain {row_dictionary['vsd-domain']}\n"
        
        cli = f"{cli}\
            shutdown\n\
                exit\n"
    
        return cli
        
def vsd_cont_mappin_no(cli,row_dictionary,key):
    if((len(str(row_dictionary['VNI ID'])) == 0) or (row_dictionary['VNI ID'] == "TempNA")):
        raise CustomException(" VNI ID Missing!",f"Kindly Check 'VNI ID' Column for 'VPLS' Section in {key} node in selected workbook!")
    
    if((len(str(row_dictionary['vxlan instance'])) == 0) or (row_dictionary['vxlan instance'] == "TempNA")):
        raise CustomException(" Vxlan Instance Missing!",f"Kindly Check 'vxlan instance' Column for 'VPLS' Section in {key} node in selected workbook!")

    else:
        cli = f"{cli}\
            vpls {row_dictionary['VPLS ID']} name {row_dictionary['VPLS Name']} customer 1 create\n"
        
        if((len(row_dictionary['allow-ip-int-bind']) > 0) and (row_dictionary['allow-ip-int-bind'] != "TempNA")):
            cli = f"{cli}\
                allow-ip-int-bind\n\
                {row_dictionary['allow-ip-int-bind']}\n\
                    exit\n"
        
        cli = f"{cli}\
                  vxlan instance {row_dictionary['vxlan instance']} vni {row_dictionary['VNI ID']} create\n\
                    exit\n"
        
        if((len(row_dictionary['BGP']) > 0) and (row_dictionary['BGP'] != "TempNA")):
            cli =  f"{cli}\
                      bgp\n\
                        {row_dictionary['BGP']}\n"
            
            if((len(row_dictionary['vsi-export']) > 0) and (row_dictionary['vsi-export'] != "TempNA")):
                cli = f"{cli}\
                        vsi-export {row_dictionary['vsi-export']}\n"
            
            if((len(row_dictionary['vsi-import']) > 0) and (row_dictionary['vsi-import'] != "TempNA")):
                cli = f"{cli}\
                    vsi-import {row_dictionary['vsi-import']}\n"
                
            
            if(((len(row_dictionary['RT-Export']) > 0) and (row_dictionary['RT-Export'] != "TempNA")) and ((len(row_dictionary['RT-Import']) > 0) and (row_dictionary['RT-Import'] != "TempNA"))):
                cli = f"{cli}\
                    route-target export target:{row_dictionary['RT-Export']} import target:{row_dictionary['RT-Import']}\n"
            
            else:
                if((len(row_dictionary['RT-Export']) > 0) and (row_dictionary['RT-Export'] != "TempNA")):
                    cli = f"{cli}\
                            route-target export target:{row_dictionary['RT-Export']}\n"
                
                if((len(row_dictionary['RT-Import']) > 0) and (row_dictionary['RT-Import'] != "TempNA")):
                    cli = f"{cli}\
                        route-target import target:{row_dictionary['RT-Import']}\n"
            
            cli = f"{cli}\
                        exit\n"
        
        if(row_dictionary['bgp-evpn'].strip().upper() == "YES"):
            cli = f"{cli}\
                    bgp-evpn\n\
                        exit\n"
        
        if((len(row_dictionary['bgp-evpn'].strip()) > 0) and ((row_dictionary['bgp-evpn'].strip().upper() != "YES") and (row_dictionary['bgp-evpn'] != "TempNA"))):
            cli = f"{cli}\
                bgp-evpn\n\
                    {row_dictionary['bgp-evpn']}\n\
                        no shutdown\n\
                            exit\n\
                                exit\n"

        if((len(row_dictionary['stp']) > 0) and (row_dictionary['stp'] != "TempNA")):
            cli = f"{cli}\
                stp\n\
                    {row_dictionary['stp']}\n\
                        exit\n"
        if((len(row_dictionary['vsd-domain']) > 0) and (row_dictionary['vsd-domain'] != "TempNA")):
            cli = f"{cli}\
                vsd-domain {row_dictionary['vsd-domain']}\n"

        cli = f"{cli}\
            shutdown\n\
                exit\n"
        
        return cli


def cli_maker(dataframe,key,cli):
    try:
        # cli = "configure service"
        dataframe.fillna("TempNA",inplace = True)

        for i in range(len(dataframe)):
            if((len(str(dataframe.iloc[i]['Action']).strip()) == 0) or (dataframe.iloc[i]['Action'] == "TempNA")):
                raise CustomException(" Action Missing!",f"Kindly Check 'Action' Column for 'VLSM' Section in {key} node in selected workbook!")
            
            if((len(str(dataframe.iloc[i]['VSD Controller Mapping'])) == 0) or (dataframe.iloc[i]['VSD Controller Mapping'] == "TempNA")):
                raise CustomException(" VSD Controller Mapping Missing!",f"Kindly Check 'VSD Controller Mapping' Column for 'VLSM' Section in {key} node in selected workbook!")
            
            if((len(str(dataframe.iloc[i]['VPLS ID'])) == 0) or (dataframe.iloc[i]['VPLS ID'] == "TempNA")):
                raise CustomException(" VPLS ID Missing!",f"Kindly Check 'VPLS ID' Column for 'VPLS' Section in {key} node in selected workbook!")
            
            
        for i in range(len(dataframe)):
            if (dataframe.iloc[i]['VSD Controller Mapping'].upper() == "YES"):
                cli = vsd_cont_mappin_yes(cli,dataframe.iloc[i].to_dict(),key)
            
            if (dataframe.iloc[i]['VSD Controller Mapping'].upper() == "NO"):
                cli = vsd_cont_mappin_no(cli,dataframe.iloc[i].to_dict(),key)
           
        return cli
    
    except CustomException:
        return "Unsuccessful"
    
    except Exception as e:
        import traceback
        messagebox.showerror("  Exception Occured!",f"{traceback.format_exc()}\n\n{e}")
        return "Unsuccessful"
    