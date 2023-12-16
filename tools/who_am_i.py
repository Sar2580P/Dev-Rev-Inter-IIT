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
    - Use this tool only when specific keywords like "me", "I", "mine", etc. are present explicitly in the query.
    - This tool will return the user_id which can be used by other tools.
    
    '''
    bag_of_words = set(["my", "me", "mine", "i", "myself", "who am i", "whoami"])

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside who_am_i tool...') 
       
        return   list()


    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")



