from typing import List, Optional, Sequence, Any
from langchain.callbacks.base import BaseCallbackManager
from langchain.schema.language_model import BaseLanguageModel
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain.prompts import PromptTemplate
from langchain.tools.base import BaseTool
from agent_executor.tool_collection import *
from backend_llm.utils import llm, small_llm
from langchain.agents.mrkl.base import ZeroShotAgent
from agent.mistakes_selection import *
from langchain.agents.agent import Agent, AgentOutputParser
from prompts import PAST_MISTAKES


class PersonalAgent(ZeroShotAgent):
    
    query_specific_mistakes : List = []
    @classmethod
    def create_prompt(
        cls,
        tools: Sequence[BaseTool],
        user_query: str , 
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        mistakes :str = PAST_MISTAKES,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
        print("\033[91m {}\033[00m" .format('create_prompt (agent)'))

        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(tool_names=tool_names)

        #________________________________________________________________________________
        past_mistakes = analyse(user_query)
        formatted_mistakes = ''
        if past_mistakes == 'No mistakes found' or past_mistakes == []:
            formatted_mistakes = 'No mistakes found'
        else :
            for mistake in past_mistakes:
                formatted_mistakes += 'query : {q}\n'.format(q = mistake.metadata['query'])
                formatted_mistakes += 'mistake_highlight : {x}\n'.format(x = mistake.page_content) 
                formatted_mistakes += 'correct_tool : {y}\n'.format(y = mistake.metadata['correct_tool'])
                formatted_mistakes += 'correct_reasoning : {z}'.format(z = mistake.metadata['correct_reasoning'])
                formatted_mistakes += '\n\n'

        mistakes = mistakes.format(mistakes = formatted_mistakes)
        #________________________________________________________________________________
        template = "\n\n".join([prefix, tool_strings, format_instructions, mistakes ,suffix])
        if input_variables is None:
            input_variables = ["input", "agent_scratchpad"]
        
        return   PromptTemplate(template=template, input_variables=input_variables)
    #________________________________________________________________________________________________________________________________
    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        user_query: str = '',
        callback_manager: Optional[BaseCallbackManager] = None,
        output_parser: Optional[AgentOutputParser] = None,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Agent:
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)
        prompt = cls.create_prompt(
            tools,
            prefix=prefix,
            user_query=user_query,
            suffix=suffix,
            format_instructions=format_instructions,
            input_variables=input_variables,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        _output_parser = output_parser or cls._get_default_output_parser()
        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )
    