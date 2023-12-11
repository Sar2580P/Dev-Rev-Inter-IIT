from langchain.tools import BaseTool
from typing import Optional, Type, List
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from tools.argument_mapping.get_args import fill_signature
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm


class AddWorkItemsToSprint(BaseTool):
    name = "add_work_items_to_sprint"
    description = '''Adds the given work items to the sprint. 
    This tool needs to know the list of work_id and the sprint_id to which the work items should be added.
    '''

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) :
        print('\ninside add_work_items_to_sprint tool ...') 
        signature = {'work_ids': List[str],
                    'sprint_id': str ,
                    }
        
        arg_description = {
            'work_ids': 'A list of work item IDs to be added to the sprint',
            'sprint_id': 'The ID of the sprint to which the work items should be added',
            
        }
        column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        li = []
        for key, value in column_args.items():
            x = {
                'argument_name': key,
                'argument_value': value,
            }
            li.append(x)
        # ans = "The function returns add_work_items_to_sprint"
        return   li

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
