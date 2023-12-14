from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from langchain.tools import BaseTool
from typing import Optional, Type, List, Any
from utils.llm_utility import llm



# Define your desired data structure.
class WorkList(BaseModel):
    applies_to_part: List[str] = Field(description="part to which issue applies")
    created_by: List[str] = Field(description='name of person who created the issue')
    issue_priority: str = Field(description=' either of types : "p0" , "p1" , "p2" ')
    issue_rev_orgs: List[str] = Field(description='orgs that reviewed issue')
    limit : int = Field(description='maximum number of work-items to return')
    owned_by: List[str] =  Field(description='name of person who owns the issue')
    stage_name: List[str] = Field(description='stage of issue')
    ticket_needs_response: bool =  Field(description='Filters for tickets that need a response, either of types : "True" , "False"')
    ticket_rev_org: List[str] =  Field(description='Filters for tickets associated with any of the provided Rev organizations ')
    ticket_severity: List[str] = Field(description='either of types : blocker , high , medium , low')
    ticket_source_channel: List[str] = Field(description='Filters for tickets with any of the provided source channels') 
    type: List[str] = Field(description='either of types : issues , ticket , task') 
    
    # You can add custom validation logic easily with Pydantic.
    # @validator("setup")
    # def question_ends_with_question_mark(cls, field):
    #     if field[-1] != "?":
    #         raise ValueError("Badly formed question!")
    #     return field


from langchain.output_parsers.json import SimpleJsonOutputParser

parser = PydanticOutputParser(pydantic_object=WorkList)

json_prompt = PromptTemplate.from_template(
    "Fill the arguments of Tool named work_list based on the provided Query: {query}"
)
json_parser = WorkList()
json_chain = json_prompt | llm | json_parser

print(list(json_chain.stream({"query": "List my p0 issues"})))
# Set up a parser + inject instructions into the prompt template.

# prompt = PromptTemplate(
#     template="Fill the arguments of Tool named work_list with the given format and based on the provided Query.\n{format_instructions}\n{query}\n",
#     input_variables=["query"],
#     partial_variables={"format_instructions": parserA.get_format_instructions()},
# )



# # And a query intended to prompt a language model to populate the data structure.
# prompt_and_modelA = promptA | llm
# prompt_and_modelB = promptB | llm
# outputA = prompt_and_modelA.invoke({"query": "what are my p0 issues."})
# outputB = prompt_and_modelB.invoke({"query": "what are my p0 issues."})
# # print(outputA, outputB)
# print(parserA.invoke(outputA))
# print(parserB.invoke(outputB))

