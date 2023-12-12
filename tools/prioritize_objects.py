from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm
from tools.argument_mapping.get_args import fill_signature

class Prioritize(BaseTool):
    name = "prioritize_objects"
    description = '''Use this tool when asked to prioritize the objects. '''
                
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside Prioritize_objects tool...') 
        signature = {
                        'objects': List[str],
                    }

        arg_description = {
            'objects': 'the list of objects to be prioritized',
        }
        column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        li = []
        for key, value in column_args.items():
            x = {
                'argument_name': key,
                'argument_value': value,
            }
            li.append(x)
        # li = [{
        #     'argument_name': 'objects',
        #     'argument_value':query,
        #     }]
        return   li

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")