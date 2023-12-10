from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm
from tools.argument_mapping.get_args import fill_signature

class LogicTool(BaseTool):
    name = "logic_tool"
    description = '''A special code block tool that is ONLY allowed to operate on the output of other tools,
                    that must be passed as arguments'''
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        
        signature = {'python_code': str,
                    'arg_0': None ,
                    'arg_1': None ,
                    'arg_2': None ,}
        
        arg_description = {
            'python_code': """a definition of a python function that takes the arguments arg_0, arg_1, arg_2 of the format:
                              def func(arg_0, arg_1, arg_2, ...):
                                  (...)
                                  return (...)
                              the function is supposed to perform logical operations on its inputs like
                              addition, subtraction, while loops, conditional statements, iterate over lists etc.
                              
                              ex. def func(arg_0, arg_1):
                                      return arg_0 + arg_1
                              can be a special use of the function to add two numbers""",
            'arg_0': 'the input argument arg_0 to the function defined by "python_code" MUST BE A REFERENCE ($$PREV[..])',
            'arg_1': 'the input argument arg_1 to the function defined by "python_code" MUST BE A REFERENCE ($$PREV[..])',
            'arg_2': 'the input argument arg_2 to the function defined by "python_code" MUST BE A REFERENCE ($$PREV[..])',
        }
        column_args = fill_signature(query,function_signatures= signature , arg_description=arg_description,tool_name=self.name)
        li = []
        for key, value in column_args.items():
          x = {
              'argument_name': key,
              'argument_value': value,
          }
          li.append(x)
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
