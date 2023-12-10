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
    description = '''
    Use this tool when the query contains name of the object. 
    Consider using when personal nouns are present in the query.

    Instructions:
        1-) Name only contains letters, numbers, and spaces. 
        2-) Name does not special characters like !@#$%^&*()_+|:"<>?[]\;',./

    Example : Prioritize 'p0' issues for customer Ultimate Electronics
    Answer : Ultimate Electronics

    '''

    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('inside search_object_by_name tool , query is : \n' , query) 
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
