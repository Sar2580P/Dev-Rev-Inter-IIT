import re
import ast 
from typing import List, Optional, Any

def keep_digits(string):
    return re.sub(r'[^\d]+', '', string)

def parser(arguments,function_signatures):
    print(arguments)
    if(arguments==-1):
        return arguments
    arguments_dict = ast.literal_eval(arguments)
    for key,values in arguments_dict.copy().items():
        if key not in function_signatures.keys():
            continue
        if values==[]:
            del arguments_dict[key]
            continue
        if values==False and key=='ticket_needs_response':
            del arguments_dict[key]
            continue
        if type(values)==list:
            for i,value in enumerate(values):

                if type(value)==str:
                    if "PREV" in value:
                        arguments_dict[key][i]=f"$$PREV[{keep_digits(value)}]"

                    if function_signatures[key]==str:
                        arguments_dict[key]=value
                    else:
                        arguments_dict[key][i].replace(arguments_dict[key][i],value)
        else:
            if type(values)==str:
                    if "PREV" in values:
                        arguments_dict[key]=f"$$PREV[{keep_digits(values)}]"

                    if function_signatures[key]==List[str]:
                        if type(values)!=list:
                            arguments_dict[key]=[values]

    return arguments_dict

