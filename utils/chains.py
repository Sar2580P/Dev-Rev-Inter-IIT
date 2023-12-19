
from utils.templates_prompts import *
from langchain.chains import LLMChain
from utils.llm_utility import *



llm_critique = LLMChain(llm = llm , prompt=critique_prompt)
sub_task_chain = LLMChain(prompt=sub_task_prompt , llm=llm)
create_tool_experience_chain = LLMChain(llm=llm, prompt=missed_tool_prompt)