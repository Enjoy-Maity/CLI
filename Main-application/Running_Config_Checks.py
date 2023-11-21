def running_config_checks(*args) -> str:
    """
        Calls the vendor specific node checks modules
        
        Arguments : (*args) ==> contains a dynamically long tuple of arguments.
            arg[0] : str
                description =====> contains the information related to the vendor selected
        
        return flag
            flag : str
                description =====> contains 'Unsuccessful' or 'Successful' string corresponding the status of execution completion
    """
    
    