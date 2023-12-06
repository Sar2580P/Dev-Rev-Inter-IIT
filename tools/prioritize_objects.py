from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class Prioritize(BaseTool):
    name = "Prioritize"
    description = '''Returns a list of objects sorted by
                priority. The logic of what constitutes priority for a given
                object is an internal implementation detail.
                '''
    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside Prioritize_objects Tool , query is : \n' , query)
        li = []
        x = {
            'argument_name': 'objects',
            'argument_value': query,
        }
        li.append(x)
        return li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")