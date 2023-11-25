from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class SearchObjectByName(BaseTool):
    name = "search_object_by_name"
    description = '''
    Use this tool when the query contains name of the object. 

    Instructions:
    Name only contains letters, numbers, and spaces. Not special characters like !@#$%^&*()_+|:"<>?[]\;',./
    
    Given a search string, returns the id of a matching object in the system of record.
    If multiple matches are found, it returns the one where the confidence is highest.
    '''

    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside search_object_by_name tool , query is : \n' , query) 
        x = {
            'argument_name': 'query',
            'argument_value': query,
        }
        return x 
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
