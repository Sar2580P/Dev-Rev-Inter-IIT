from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class CreateActionableTasksFromText(BaseTool):
    name = "create_actionable_tasks_from_text"
    description = '''Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item. '''

    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside create_actionable_tasks_from_text tool , query is : \n' , query) 
        li = []
        x = {
            'argument_name': 'text',
            'argument_value': query,
        }
        li.append(x)
        return li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
