from typing import List, Optional, Sequence, Any
from langchain.callbacks.base import BaseCallbackManager
from langchain.schema.language_model import BaseLanguageModel
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS, PREFIX
from langchain.prompts import PromptTemplate
from langchain.tools.base import BaseTool
from agent.tool_collection import *
from utils.llm_utility import llm 
from langchain.agents.mrkl.base import ZeroShotAgent
from agent.mistakes_selection import *
from langchain.agents.agent import Agent, AgentOutputParser
from utils.prompts import PAST_MISTAKES ,SUFFIX


class PersonalAgent(ZeroShotAgent):
    
    @classmethod
    def create_prompt(
        cls,
        user_query: str ,
        tools: Sequence[BaseTool] ,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        mistakes :str = PAST_MISTAKES,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
        print("\033[91m {}\033[00m" .format('create_prompt (agent)'))
        
        past_mistakes = analyse(user_query)
        # past_mistakes = 'No mistakes found'
        formatted_mistakes = ''
        if past_mistakes == 'No mistakes found' or past_mistakes == []:
            formatted_mistakes = 'No mistakes found'
        else :
            for mistake in past_mistakes:
                formatted_mistakes += mistake.page_content 

        # tools = get_relevent_tools(user_query)
    
        mistakes = mistakes.format(mistakes = formatted_mistakes)
        if user_query == '':
            mistakes = ''
        #________________________________________________________________________________
        
        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(tool_names=tool_names)
        #________________________________________________________________________________
        template = "\n\n".join([prefix, tool_strings, format_instructions, mistakes, suffix])
        if input_variables is None:
            input_variables = ["input", "agent_scratchpad"]
        
        prompt =  PromptTemplate(template=template, input_variables=input_variables)
        # print('****',prompt.template.format(input=user_query, agent_scratchpad=''))
        return prompt
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
            tools=tools,
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
    