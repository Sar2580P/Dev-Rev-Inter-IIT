from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from utils.llm_utility import llm
from utils.get_args import fill_signature

class WhoAmI(BaseTool):
    name = "who_am_i"
    description = '''
            Use this tool only when pronouns are present in query like "me", "I" , etc. Else don't use this tool.
            This tool will return the user_id which can be used by other tools.
            '''
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside who_am_i tool...') 
        # signature = {
        #                 'ids': List[str],
        #             }
        
        # # TODO
        # arg_description = {
        #     'ids': 'the list of ids of the users',
        # }
        # column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        # li = []
        # for key, value in column_args.items():
        #     x = {
        #         'argument_name': key,
        #         'argument_value': value,
        #     }
        #     li.append(x)
        return   list()


    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")



