from langchain.tools import BaseTool
from typing import Optional, Type, List, Any
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from tools.argument_mapping.get_args import fill_signature
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm
from tools.who_am_i import WhoAmI


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
    primary_prompt_template = '''
        You need to check whether the below mentioned argument can be filled using the given query.
        If yes , then fill the argument with the value extracted from the query.
        If no , then leave the argument empty.

        Argument name : {argument_name}
        Argument description : {argument_description}
        Query : {query}

        Few-shots on how to identify the argument value from the query:
        {few_shots}

'''
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        # if self.get_primary_value(query) in '    ':
        #     return "Hey agent I need value for user_id which is not in query, Try calling who_am_i tool first, then come to me."
        # print('inside worklist , query is : \n' , query) 
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
        return   li

    def get_primary_value(self, query: str) -> str:
        examples = [
                {"Query": "Find blah blah for user Sarvagya", 
                 "Argument_value": "Sarvagya"},
                 {
                "Query": "What are my p0 issues",
                "Argument_value": ""}, 
                {"Query": "Get the p0 issues for user id 123*/Sae@22", 
                 "Argument_value": "123*/Sae@22"},
                {"Query": "Get the high severity tickets for 123/:97//@#12", 
                 "Argument_value": "123/:97//@#12"},
                {"Query": "Get the high severity tickets ",
                 "Argument_value": ""},
                 {"Query": "List all issues that I have created",
                  "Argument_value": ""},
            ]
        example_formatter_template = """
                                        Query: {Query}
                                        Argument_value: {Argument_value}\n
                                    """
        example_prompt = PromptTemplate(
                            input_variables=["Query", "Argument_value"],
                            template=example_formatter_template,
                        )
        few_shot_prompt = FewShotPromptTemplate( 
                            examples=examples,

                            # prompt template used to format each individual example
                            example_prompt=example_prompt,

                            # prompt template string to put before the examples, assigning roles and rules.
                            prefix='''
                                    You need to extract the value for the below argument from the query.
                                    Argument name: {argument_name}

                                    Few-shots on how to extract the value of {argument_name} from the query:

                                ''' , 
                            
                            # prompt template string to put after the examples.
                            suffix=''' As you can see above, if pronouns are present in the query, then leave the argument empty.
                            Now you are given a query below:
                                    Query: {query}
                                    You need to fill the value for above mentioned argument. 
                                    If its value can be extracted from the query, then fill the value. Otherwise leave it empty.
                                
                                    ''',
                            
                            # input variable to use in the suffix template
                            input_variables=["query", "argument_name"],
                            example_separator="\n", 
                        )
        chain = LLMChain(llm=llm, prompt=few_shot_prompt)

        primary_value = chain.run(
            argument_name='primary_value',
            query=query,

        )
        primary_value = primary_value.split(':')[-1]
        print('primary value is : $' , primary_value, '$')
        
        return primary_value

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
