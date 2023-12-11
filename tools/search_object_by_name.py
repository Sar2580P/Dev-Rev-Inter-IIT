from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm
from tools.argument_mapping.get_args import fill_signature

class SearchObjectByName(BaseTool):
    name = "search_object_by_name"
    description = ''''
    Given a search string, returns the id of a matching object in the system of record. If multiple matches are found, it
    returns the one where the confidence is highest.

    The tool requires the following arguments:
        'query': 'The search string, could be for example customer’s name, part name, username.  
    
    '''

    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside search_object_by_name tool...') 
        signature = {
                        'query': str,
                    }

        arg_description = {
            'query': 'customer name present in the query',
        }
        column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        li = []
        for key, value in column_args.items():
            x = {
                'argument_name': key,
                'argument_value': value,
            }
            li.append(x)
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
