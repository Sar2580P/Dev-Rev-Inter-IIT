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
    print("\033[91m {}\033[00m" .format('choose_mistake (mistake_selection)'))
    formatted_mistakes = ''
    formatted_mistakes += 'mistake_highlight : {x}\n'.format(x = mistake.page_content) 
    
    formatted_mistakes += 'correct_tool : {y}\n'.format(y = mistake.metadata['correct_tool'])
    formatted_mistakes += 'correct_reasoning : {z}\n'.format(z = mistake.metadata['correct_reasoning'])
    
    x = chain.run({'input':user_query, 'mistake':formatted_mistakes})
    return ast.literal_eval(x)


def analyse(user_query):
    print("\033[91m {}\033[00m" .format('analyse (mistake_selection)'))
    mistakes = mistake_memory.pull(user_query) if user_query != '' else ''
    
    if isinstance(mistakes , str) or mistakes == []:
        return 'No mistakes found'
    final_mistakes = [] 
    for mistake in mistakes:

        ans = choose_mistake(user_query , mistake)
        
        # print(ans)
        if ans == 1:
            final_mistakes.append(mistake)

    return final_mistakes
