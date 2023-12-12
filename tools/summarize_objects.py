from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm
from tools.argument_mapping.get_args import fill_signature

class Summarize(BaseTool):
    name = "summarize_objects"
    description = '''This tool is useful for summarizing information.
      It needs a list of objects as input and returns a summary of the objects. 
    '''
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside SummarizeTool tool...') 
        signature = {
                        'objects': List[object],
                    }

        arg_description = {
            'objects': 'the query to be summarized',
        }
        column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        li = []
        for key, value in column_args.items():
            x = {
                'argument_name': key,
                'argument_value': value,
            }
            li.append(x)
        # li.append({
        #     'argument_name': 'objects',
        #     'argument_value': query,
        # })
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
