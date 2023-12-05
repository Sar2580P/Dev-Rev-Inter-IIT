from typing import List, Optional, Sequence, Union
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain.prompts import PromptTemplate
from langchain.tools.base import BaseTool
from tools.tool_collection import *
from backend_llm.utils import llm
from langchain.agents.mrkl.base import ZeroShotAgent
from agent_executor.memory import mistake_memory
from langchain.docstore.document import Document
from mistakes_selection import choose_mistake

suffix_tempalate = '''
Begin!

Question: {input}
Thought:{agent_scratchpad}

Before proceeding further, below I have mentioned common mistakes made by you while using the tools.
Please go through them carefully and try to avoid them in future.
{mistakes}

'''



class PersonalAgent(ZeroShotAgent):
    query_specific_mistakes = None
    @classmethod
    def create_prompt(
        cls,
        tools: Sequence[BaseTool],
        user_query: str = '',
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
        
        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(tool_names=tool_names)

        #________________________________________________________________________________
        past_mistakes = mistake_memory.pull(user_query) if user_query != '' else ''
        mistakes = cls.analyse(user_query, past_mistakes)
        formatted_mistakes = ''
        if mistakes == 'No mistakes found':
            formatted_mistakes = mistakes
        else :
            for mistake in mistakes:
                formatted_mistakes += 'mistake_highlight : {x}\n'.format(x = mistake.page_content) 
                formatted_mistakes += 'correct_tool : {y}\n'.format(y = mistake.metadata['correct_tool']),
                formatted_mistakes += 'correct_reasoning : {z}'.format(z = mistake.metadata['correct_reasoning']),
                formatted_mistakes += '\n\n'
                
        suffix = suffix_tempalate.format(mistakes = formatted_mistakes)
        #________________________________________________________________________________
        template = "\n\n".join([prefix, tool_strings, format_instructions, suffix])
        if input_variables is None:
            input_variables = ["input", "agent_scratchpad"]
        return PromptTemplate(template=template, input_variables=input_variables)

    @classmethod
    def analyse(cls, user_query , mistakes: Union[str , List[Document]]):
        if cls.query_specific_mistakes is not None:
            return cls.query_specific_mistakes
        if isinstance(mistakes , str):
            return 'No mistakes found'
        final_mistakes = [] 
        for mistake in mistakes:
            highlight = mistake.page_content
            correct_tool  = mistake.metadata['correct_tool'] 
            correct_tool_input =  mistake.metadata['correct_tool_input'] , 
            correct_reasoning = mistake.metadata['correct_reasoning']

            ans = choose_mistake(user_query , highlight , correct_tool , correct_tool_input , correct_reasoning)
            print('in analyse (agent) : ' , ans)
            if ans == 1:
                final_mistakes.append(mistake)
        cls.query_specific_mistakes =  final_mistakes