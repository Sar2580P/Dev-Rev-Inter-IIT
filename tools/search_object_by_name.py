from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from utils.llm_utility import llm
from utils.get_args import fill_signature

class SearchObjectByName(BaseTool):
    name = "search_object_by_name"
    description = '''
    - This tool is useful for searching an object by its name. It returns the id of the object.
   - Given a search string,it is used to return the identity (id), whenever a name of a customer/user/person is present.
   - If multiple matches are found, it returns the one where the confidence is highest.  
    '''

    bag_of_words = set(["customer", "customer name", "username", "user", "part name"])
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside search_object_by_name tool...') 
        signature = {
                        'query': str,
                    }

        arg_description = {
            'query': 'object or customer name present in the query',
        }
        li = []
        for key, value in signature.items():
            arg_dtype = {
                'argument_name': key,
                'argument_value': value,
            }
            arg_descr = {
                'argument_name': key,
                'argument_value': arg_description[key],
            }
            x = fill_signature(query = query, arg_name = key , arg_dtype = arg_dtype , arg_descr = arg_descr, tool_name = self.name)
            if x is not None:
                li.append({
                    'argument_name': key,
                    'argument_value': x,
                })
       
        print('Extracted arguments are : ',li)
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
