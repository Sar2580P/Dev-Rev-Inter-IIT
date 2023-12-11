from langchain.prompts import PromptTemplate  
from backend_llm.utils import llm, small_llm
from langchain.chains import LLMChain
from typing import List, Union
from langchain.docstore.document import Document
from agent_executor.agent_memory import mistake_memory
import ast
from prompts import MISTAKE_SELECTION


prompt = PromptTemplate(template=MISTAKE_SELECTION, input_variables=["input", "mistake"])
chain = LLMChain(llm=small_llm, prompt=prompt)

def choose_mistake(user_query, mistake):
    x = chain.run({'input':user_query,  'mistake': mistake.page_content})
    y=  ast.literal_eval(x)        
    return y

def analyse(user_query):
    print("\033[91m {}\033[00m" .format('analyse (mistake_selection)'))
    print("\033[91m {}\033[00m" .format('\tPulling mistakes from agent memory... (mistake_selection)'))
    mistakes = mistake_memory.pull(user_query) if user_query != '' else ''
    mistaken_tool_set = set()
    
    if isinstance(mistakes , str) or mistakes == []:
        return 'No mistakes found'
    final_mistakes = [] 
    i=0
    for mistake in mistakes:
        mistaken_tool = mistake.metadata['correct_tool']
        if not mistaken_tool in mistaken_tool_set:
            mistaken_tool_set.add(mistaken_tool)
            ans = choose_mistake(user_query , mistake)
            if ans == 1:
                i+=1
                print("\033[91m {}\033[00m" .format('\tchosen_mistakes : {i} (mistake_selection)'.format(i=i)))
                print("\033[93m {}\033[00m" .format(prompt.template.format(input=user_query , mistake=mistake.page_content)))
                final_mistakes.append(mistake)

    return final_mistakes
