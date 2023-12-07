from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm
from tools.argument_mapping.get_args import fill_signature

class GetSimilarWorkItems(BaseTool):
    name = "get_similar_work_items"
    description = '''Use this tool when you want to get similar work_items for a given work_id'''

    # def _run(
    #     self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    # ) -> str:
    #     print('inside get_similar_work_items tool , query is : \n' , query) 
    #     li = []
    #     x = {
    #         'argument_name': 'work_id',
    #         'argument_value': query,
    #     }
    #     li.append(x)
    #     return li 
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('inside get_similar_work_items tool , query is : \n' , query) 
        signature = {
                        'work_id': str,
                    }
        # TODO
        arg_description = {
            'work_id': 'A list of work item IDs to be added to the sprint',
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
