import sys, os
sys.path.append(os.getcwd())
from langchain.vectorstores.chroma import Chroma
from utils.llm_utility import *

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from utils.prompts import PREFIX_MISTAKE_MEMORY, SUFFIX_MISTAKE_MEMORY, CORRECT_TRAJECTORY_TILL_NOW
from memory.memory import Memory


#__________________________________________________________________________________________________________________________

V_db = Chroma(embedding_function = embedding_func, persist_directory= 'database/mistakes_db' , 
                                relevance_score_fn='similarity_search_with_score')
mistake_memory = Memory(k=5,vector_db=V_db)

#__________________________________________________________________________________________________________________________
example_prompt = PromptTemplate(
    input_variables=["tool_name", "tool_input" , "tool_reasoning"],
    template=CORRECT_TRAJECTORY_TILL_NOW,
)

#__________________________________________________________________________________________________________________________

def build_experience(x):
  
    examples = x['correct_trajectory']

    few_shot_prompt = FewShotPromptTemplate( 
    examples=examples,

    # prompt template used to format each individual example
    example_prompt=example_prompt,

    # prompt template string to put before the examples, assigning roles and rules.
    prefix=PREFIX_MISTAKE_MEMORY,
    
    # prompt template string to put after the examples.
    suffix= SUFFIX_MISTAKE_MEMORY,
    
    # input variable to use in the suffix template
    input_variables=["query", "correct_tool" , "correct_tool_description" , 
                     "wrong_tool" , "wrong_tool_description" ],
    example_separator="\n", 
)
    chain = LLMChain(llm=llm, prompt=few_shot_pormpt)
    print("\033[91m {}\033[00m" .format('build_experience (agent_memory)'))
    y = chain.run({"query": x['query'] ,  
                  "correct_tool": x['correct_tool'] ,"correct_tool_description": x['correct_tool_description'], 
                   "wrong_tool": x['wrong_tool'] ,"wrong_tool_description": x['wrong_tool_description'] })
    
    if y[0] == '\n':
        y = y[1:]
    return y


























# from transformers import pipeline


# def LLMsummarizer(query, tool_list, tool, signal):

#     ARTICLE = f"""
#     You are a Robot's memory that keep logs of all the Tools you have yet taken.

#     The current task list is as follows:
#     {tool_list}, it represents the tools which have already been used for the provide query.
#     provided query is {query}, this is given to you by the user.
#     at the current moment after using all the above tools from the tool list we try to use the following tool {tool},
#     the use of this tool turned out to be {signal}.
#     Surmmarize this whole scenario in Natural Language.

#     Remmember the output is based on the user evaluation which is '{signal}';.

#     """

#     print(ARTICLE)

#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#     res = summarizer(ARTICLE, max_length=100, min_length=50, do_sample=False)
#     return res

