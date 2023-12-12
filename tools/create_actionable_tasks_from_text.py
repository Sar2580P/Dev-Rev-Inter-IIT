from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from utils.llm_utility import llm
from utils.get_args import fill_signature

class CreateActionableTasksFromText(BaseTool):
    name = "create_actionable_tasks_from_text"
    description = '''Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item. '''
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside create_actionable_tasks_from_text tool...') 
        signature = {
                        'text': str,
                    }

        arg_description = {
            'text': 'The text from which the actionable insights need to be created.',
        }
        column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        li = []
        # for key, value in column_args.items():
        #     x = {
        #         'argument_name': key,
        #         'argument_value': value,
        #     }
        #     li.append(x)
        li.append({'argument_name': 'text', 'argument_value': query})
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
