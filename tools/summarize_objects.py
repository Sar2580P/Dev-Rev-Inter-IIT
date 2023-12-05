from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class Summarize(BaseTool):
    name = "summarize_objects"
    description = '''This tool is useful for summarizing information.
      It needs a list of objects as input and returns a summary of the objects. 
    '''

    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside SummarizeTool , query is : \n' , query) 
        x = {
            'argument_name': 'objects',
            'argument_value': query,
        }
        return x 
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
