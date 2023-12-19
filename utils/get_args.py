import sys , os
sys.path.append(os.getcwd())
from typing import List, Union, Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.llm_utility import llm
from memory.tool_memory import retrieve_tool_experience
from utils.templates_prompts import TOOLS_PROMPT_EXAMPLES, ARG_FILTER_PROMPT
import re, ast
from utils.tool_output_parser import parser
from icecream import ic

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.output_parsers import OutputFixingParser

#-------------------------------------------------------------------------------------------------------------------------------------------------
# response_schemas = [
#     ResponseSchema(name="argument name", description="the name of the argument"),
#     ResponseSchema(name="argument value", description="The value of the argument extracted from the query. Don't write anything else here.")
# ]
# output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


arg_extraction_prompt = PromptTemplate(template=TOOLS_PROMPT_EXAMPLES , 
                        input_variables=['arg_description','arg_dtype' ,'user_query'] ,   # ,'memory_examples'
                        # partial_variables= {"format_instructions" : output_parser.get_format_instructions()}
                        )

signature_chain = LLMChain(llm = llm, prompt = arg_extraction_prompt , verbose=False)


arg_filter_prompt = PromptTemplate(template=ARG_FILTER_PROMPT,
                                   input_variables=['query', 'arg_name', 'arg_description'],
                                   )
arg_filter = LLMChain(llm = llm, prompt = arg_filter_prompt , verbose=False)
# new_parser = OutputFixingParser.from_llm(parser=output_parser, llm=llm)

#-------------------------------------------------------------------------------------------------------------------------------------------------

def fill_signature(query:str, arg_name:str , arg_dtype: dict , arg_descr :dict, tool_name:str)->Dict[str,Any] :

    extracted_args = signature_chain.run({'arg_description':arg_descr,'arg_dtype':arg_dtype, 'user_query':query})
    return extracted_args.strip('\n').strip(' ')
    