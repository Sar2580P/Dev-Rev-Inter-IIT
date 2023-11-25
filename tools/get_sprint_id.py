from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class GetSprintId(BaseTool):
    name = "get_sprint_id"
    description = '''Returns the ID of the current sprint '''

    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside get_sprint_id tool , query is : \n' , query) 
        x = {
            'argument_name': '',
            'argument_value': list(),
        }
        return x 
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")