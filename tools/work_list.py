from langchain.tools import BaseTool
from typing import Optional, Type, List
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import sqlite3
from tools.argument_mapping.get_args import fill_signature
import inspect
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm


TEMPLATE = '''
You are good at writing SQL queries. You have a database with the following table : 
{table_name} 

table schema :
{table_schema}

table sample rows :
{table_sample_rows}

You want to query the table with the following arguments :
{columns}


Check that sql query is correct before executing it.
'''
prompt = PromptTemplate(template=TEMPLATE , 
                        input_variables=['table_name' , 'table_schema' , 'table_sample_rows' , 'columns']
                        )
        
syntax_chain = LLMChain(llm = llm, prompt=prompt)

class WorkList(BaseTool):
    name = "works_list"
    description = '''This tool is useful for querying  table : student 
    
        table following columns:
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
    ) -> str:
        
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
        
        table_name = 'student'
        column_args = fill_signature(query,inspect.signature(signature))
        conn = sqlite3.connect('experimental_db\sample_database.db')
        cursor = conn.cursor()
        table_schema ,sample_rows = self.get_table_info(table_name, cursor)

        sql_query = syntax_chain.run({'table_name' : table_name ,
                                      'table_schema' : table_schema , 
                                      'table_sample_rows': sample_rows ,
                                      'columns' : column_args})

        print('\n\n\n' , sql_query , '\n\n\n')
        rows = cursor.execute(sql_query).fetchall()
        print(rows)
        li = []
        for key, value in column_args.items():
          x = {
              'argument_name': key,
              'argument_value': value,
          }
          li.append(x)
        return rows , li
    
    def get_table_info(self, table_name, cursor):
        query = "PRAGMA table_info({table_name})".format(table_name=table_name)
        cursor.execute(query)
        rows = cursor.fetchall()
        table_schema = ''
        sample_rows = ''
        for row in rows:
            table_schema += str(row) + '\n'
        query = "SELECT * FROM {table_name} LIMIT {num_rows_to_fetch};".format(table_name=table_name , 
                                                                                num_rows_to_fetch=3)
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            sample_rows += str(row) + '\n'
        return table_schema , sample_rows


    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
