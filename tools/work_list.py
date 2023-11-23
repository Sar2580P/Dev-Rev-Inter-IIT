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


class WorkList(BaseTool):
    name = "works_list"
    description = '''This tool is useful for querying  table : student 
        Don't worry about the syntax , just pass query in natural language 
        
        table has following columns:
            applies_to_part ,
            created_by ,
            issue_priority ,
            issue_rev_orgs ,
            owned_by ,
            stage_name ,
            ticket_needs_response ,
            ticket_rev_org ,
            ticket_severity ,
            ticket_source_channel ,
            type ,
        
    '''

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) :
        print('inside worklist , query is : \n' , query) 
        signature = {'applies_to_part': List[str],
                    'created_by': List[str] ,
                    'issue_priority': List[str] ,
                    'issue_rev_orgs': List[str] ,
                    'owned_by': List[str] ,
                    'stage_name': List[str] ,
                    'ticket_needs_response': bool ,
                    'ticket_rev_org': List[str] ,
                    'ticket_severity': List[str] , 
                    'ticket_source_channel': List[str] ,
                    'type': List[str],}
        
        arg_description = {
            'applies_to_part': 'part to which issue applies',
            'created_by': 'name of person who created the issue',
            'issue_priority': ' either of types : "p0" , "p1" , "p2" ',
            'issue_rev_orgs': 'orgs that reviewed issue',
            'owned_by': 'name of person who owns the issue',
            'stage_name': 'stage of issue',
            'ticket_needs_response': 'whether ticket needs response',
            'ticket_rev_org': 'orgs that reviewed ticket',
            'ticket_severity': 'severity of ticket',
            'ticket_source_channel': 'source channel of ticket',
            'type': 'type of issue',
        }
        column_args = fill_signature(query,function_signatures= signature)
        li = []
        for key, value in column_args.items():
          x = {
              'argument_name': key,
              'argument_value': value,
          }
          li.append(x)
        ans = "The function returns work list"
        return   li

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
