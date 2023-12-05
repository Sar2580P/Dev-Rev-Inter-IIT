from langchain.prompts import PromptTemplate  
from backend_llm.utils import llm
from langchain.chains import LLMChain

template =  '''
Below you are provided with the user query :
{input}

Below you are provided with one of the mistakes made by another AI agent on some other user query :
{mistake}

Now, the AI agent wants to know whether the above mistake is relevant to the user query or not, i.e, it should be looked into or not while
providing the answer to the user query.

Return 1 if the mistake is relevant to the user query, else return 0.
'''

prompt = PromptTemplate(template=template, input_variables=["input", "mistake"])
chain = LLMChain(llm=llm, prompt=prompt)

def choose_mistake(user_query, mistake):
    formatted_mistakes = ''
    formatted_mistakes += 'mistake_highlight : {x}\n'.format(x = mistake.page_content) 
    formatted_mistakes += 'correct_tool : {y}\n'.format(y = mistake.metadata['correct_tool']),
    formatted_mistakes += 'correct_reasoning : {z}\n'.format(z = mistake.metadata['correct_reasoning']),
    
    x = chain.run({'input':user_query, 'mistake':formatted_mistakes})
    print('inside mistake_selection' , x)
    return x