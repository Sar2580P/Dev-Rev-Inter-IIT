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
    description = '''

    USAGE : 
     - Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item. '''
    
    bag_of_words = set(["create actionable tasks", "create tasks", "create insights", "plan tasks", "create tasks from text", "create"])
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
        li = []
        for key, value in signature.items():
            arg_dtype = {
                'argument_name': key,
                'argument_value': value,
            }
            arg_descr = {
                'argument_name': key,
                'argument_value': arg_description[key],
            }
            x = fill_signature(query = query, arg_name = key , arg_dtype = arg_dtype , arg_descr = arg_descr, tool_name = self.name)
            if x is not None:
                li.append({
                    'argument_name': key,
                    'argument_value': x,
                })
       
        print('Extracted arguments are : ',li)
        return   li

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
