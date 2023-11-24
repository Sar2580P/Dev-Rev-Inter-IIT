from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class GetSimilarWorkItems(BaseTool):
    name = "get_similar_work_items"
    description = '''Returns a list of work items that are similar to the given work item'''

    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside get_similar_work_items tool , query is : \n' , query) 
        x = {
            'argument_name': 'work_id',
            'argument_value': query,
        }
        return x 
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
