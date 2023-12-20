from langchain.agents.agent import *
import sys, os
sys.path.append(os.getcwd())
from utils.llm_utility import *
from agent.tool_collection import *
from langchain.agents import AgentExecutor
from langchain.agents.loading import AGENT_TO_CLASS
import json, copy
from evaluator import *
from memory.tool_memory import build_tool_experience
# from wandb.integration.langchain import WandbTracer
from utils.llm_utility import llm
from utils.chains import *
from utils.parsers import critique_parser
from agent.agent import agent_obj
from langchain.output_parsers import OutputFixingParser

# agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
# agent_cls = AGENT_TO_CLASS[agent]
# agent_obj = agent_cls.from_llm_and_tools(
#             llm, task_tools,  
#         )

class CustomAgentExecutor(AgentExecutor):
    return_schema :List[Dict] = []   # added by me
    tool_count : int = 0             # added by me
    train_mode : bool = True      # added by me
    checkpoints = {}                 # added by me
    true_tools : List[str] = None                 # added by me
    correct_trajectory : List[Dict] = []            # added by me
    ground_truth : List[Dict] = []
    thought_execution_chain : List[Dict] = []   # added by me
    tool_gate : int = 0
    web_schema: List[Dict] = []
    
    #_______________________________________________________________________________________________
    def eval(self):
        self.train_mode = False
    def train(self):
        self.train_mode = True

    def get_tool_lists(self , ground_truth:str):
        ground_truth = json.loads(ground_truth)
        self.ground_truth = ground_truth
        self.true_tools = [tool['tool_name'] for tool in ground_truth]
    
    #_______________________________________________________________________________________________
    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        
        """Run text through and get agent response."""
        if self.tool_count == 0:        
            self.return_schema = []        
            intermediate_steps = []   
            self.correct_trajectory = []    
            self.checkpoints = {}   
            self.thought_execution_chain = []  
            self.web_schema = []  

        # Check if the query is valid
        answerable_with_tools, reason = self._check_if_answerable_with_tools(inputs['input'])
        if not answerable_with_tools :
            self.thought_execution_chain.append(reason)
            next_step_output = AgentFinish(return_values = {'output':'dvdvsdd'} ,
                                         log ='I now know the final answer.\nFinal Answer : sarvagya')
            return self._return(
                    next_step_output, [], run_manager=run_manager
                )                             
        
        
        # Construct a mapping of tool name to tool for easy lookup
        name_to_tool_map = {tool.name: tool for tool in self.tools}
        # We construct a mapping from each tool to a color, used for logging.
        color_mapping = get_color_mapping(
            [tool.name for tool in self.tools], excluded_colors=["green", "red"]
        )
        intermediate_steps: List[Tuple[AgentAction, str]] = []
        # Let's start tracking the number of iterations and time elapsed

        iterations = 0
        time_elapsed = 0.0
        start_time = time.time()
        
        # We now enter the agent loop (until it returns something).
        print("\033[1;35;40m {} \033[0m" .format('updating agent prompt with mistakes'))
        # self.agent.llm_chain.prompt = self.agent.create_prompt(tools = self.tools, 
        #                                                        user_query=inputs['input'])
        
        
        self.agent.llm_chain.prompt = self.agent.create_prompt(tools = self.tools, 
                                                               user_query=inputs['input'] , tool_task = '')
        

        while self._should_continue(iterations, time_elapsed):
            self.tool_gate += 1
            if(self.tool_gate&1 != 0):
                self.agent.llm_chain.prompt = self.agent.create_prompt(tools = self.tools, 
                                                               user_query=inputs['input'] , tool_task = '')
            
            next_step_output = self._take_next_step(
                                                    name_to_tool_map,
                                                    color_mapping,
                                                    inputs,
                                                    intermediate_steps,
                                                    run_manager=run_manager,
                                                )
            if next_step_output == None:
                continue

            if isinstance(next_step_output, AgentFinish):
                self.tool_count = 0             
                print("\033[1;35;40m {} \033[0m" .format('checkpoints ---> '))
                print("\033[1;35;40m {} \033[0m" .format(self.checkpoints))


                return self._return(
                    next_step_output, intermediate_steps, run_manager=run_manager
                )
            
            self.tool_count += 1            # added by me

            intermediate_steps.extend(next_step_output)
            if len(next_step_output) == 1:
                next_step_action = next_step_output[0]
                # See if tool should return directly
                tool_return = self._get_tool_return(next_step_action)
                if tool_return is not None:
                    return self._return(
                        tool_return, intermediate_steps, run_manager=run_manager
                    )
            iterations += 1
            time_elapsed = time.time() - start_time
        output = self.agent.return_stopped_response(
            self.early_stopping_method, intermediate_steps, **inputs
        )
        return self._return(output, intermediate_steps, run_manager=run_manager)
    #_______________________________________________________________________________________________
    def _check_if_answerable_with_tools(self , query:str) -> bool:
        is_query_valid = llm_critique.run({'query' : query , 'tools' : "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])})
        print('CRITIQUE : ' , is_query_valid)

        try : 
            output = critique_parser.parse(is_query_valid)
            if int(output['answer']) ==1 :
                return True, output['reason']
            return False, output['reason']

        except OutputParserException as e:
            print('CRTIQUE ERROR : failed to check query validity')
            return True, None

    #________________________________________________________________________________________________
    def create_sub_task(self, input):
        '''
        On train mode, if agent executor picks wrong tool, we replace its choice with the correct one.
        This function decides what should become the tool input for the correct tool provided to agent in case of wrong choice.
        '''
        # print(input)

        answer = sub_task_chain.run({'query': input['query'] , "intermediate_steps" : input['intermediate_thoughts'] ,  
                                     "tool_name" : input["correct_tool"] , "tool_description" : input["correct_tool_description"]})
        # print('sub_task :' ,answer)
        print("\033[91m {}\033[00m" .format('sub_task (auxiliary_executor)'))
        
        try :
            new_subtask = sub_task_parser.parse(answer)
            return new_subtask
        except Exception as e :
            new_parser = OutputFixingParser.from_llm(parser=sub_task_parser, llm=llm)

            new_subtask = new_parser.parse(answer)
            # new_subtask = {"tool_input" : '' , "reason" : 'Failed to create sub-task for correct picked tool ...'}
            return new_subtask
    #_________________________________________________________________________________________________

    def _return(
        self,
        output: AgentFinish,
        intermediate_steps: list,
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        if run_manager:
            run_manager.on_agent_finish(output, color="green", verbose=self.verbose)
        final_output = output.return_values
        if self.return_intermediate_steps:
            final_output["intermediate_steps"] = intermediate_steps
        return final_output
    #_______________________________________________________________________________________________
    def _take_next_step(
        self,
        name_to_tool_map: Dict[str, BaseTool],
        color_mapping: Dict[str, str],
        inputs: Dict[str, str],
        intermediate_steps: List[Tuple[AgentAction, str]],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Union[AgentFinish, List[Tuple[AgentAction, str]]]:
        """Take a single step in the thought-tool-observation loop.

        Override this to take control of how the agent makes and acts on choices.
        """
        try:
            intermediate_steps = self._prepare_intermediate_steps(intermediate_steps)
            # ic(intermediate_steps)

            # Call the LLM to see what to do.
            output = self.agent.plan(
                intermediate_steps,
                callbacks=run_manager.get_child() if run_manager else None,
                **inputs,
            )
            # ic(inputs , intermediate_steps , output , self.train_mode)
            print("\033[1;35;40m {} \033[0m" .format('inside _take_next_step , agent.plan completed ...'))


            ## Added:
            # ic(self.tool_gate)
            # ic(self.agent.llm_chain.prompt)

            if not self.train_mode and not isinstance(output,AgentFinish):
                self.agent.llm_chain.prompt = self.agent.create_prompt(tools = self.tools, 
                                                                user_query=inputs['input'], tool_task = output.log, wrong_tool_name=output.tool)

                if(self.tool_gate&1 != 0):
                    # print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
                    return None




            if self.train_mode :   # added by me

                if self.tool_count == len(self.true_tools):
                    output = AgentFinish(return_values = {'output':'Agent trying to use more tools than in ground truth.\nHence, Aborting Agent Execution ...'} ,
                                         log ='I now know the final answer.\nFinal Answer : sarvagya')
                    
                if isinstance(output ,AgentAction):
                #==============================================================================================================
                    current_schema = copy.deepcopy(self.return_schema)
                    current_schema.append({                        
                        'tool_name': output.tool,
                        'arguments': [],
                    })
                    try:
                        is_right_decision, analogy, correct_arg = validate(self.ground_truth, current_schema[:-1], output.tool)  # added by me , evaluator
                    except:
                        is_right_decision, analogy = self.true_tools[self.tool_count] == output.tool, " "  # added by me , evaluator

                    ic(is_right_decision)
                #==============================================================================================================
                    if not is_right_decision:
                        print("\033[1;35;40m {} \033[0m" .format('agent planned wrongly, picked tool : {} ...'.format(output.tool)))
                        curr_step = {
                                    'correct_tool': self.true_tools[self.tool_count],
                                    'correct_tool_description': name_to_tool_map[self.true_tools[self.tool_count]].description,
                                    'wrong_tool': output.tool,
                                    'wrong_tool_description': name_to_tool_map[output.tool].description,
                                    'thought': output.log.split('\n')[0]
                            }
                        print("======================================================================")
                        # ic(output.tool,self.true_tools[self.tool_count])
                        self.checkpoints[self.tool_count] = curr_step
                        
                        input = {
                            'correct_tool' : self.true_tools[self.tool_count] ,
                            'correct_tool_description' : name_to_tool_map[self.true_tools[self.tool_count]].description ,
                            'query' : inputs['input'] ,
                            'intermediate_thoughts' : self.thought_execution_chain ,
                        }

                        print("\033[1;35;40m {} \033[0m".format('\ncalling auxiliary_executor ...\nCreating sub task for tool : {} '.format(self.true_tools[self.tool_count])))
                        answer = self.create_sub_task(input)   
                        tool_input, log = answer['tool_input'], answer['reason']                     
                        
                        if tool_input == '':
                            print('^^^^^^^^^^^^^^^^^^')
                            return AgentFinish(
                                return_values = {'output':'Stopping Further Agent Execution ...'} ,
                                         log ='I now know the final answer.\nFinal Answer : sarvagya'
                            )
                        
                        # updating the next tool, tool_input and log with that provided by auxiliary llm
                        output.tool = self.true_tools[self.tool_count]
                        output.tool_input = tool_input
                        # ic(output.tool , output.tool_input)
                        output.log = log + "\n" + analogy +"\nAction: {tool}\nAction Input:{tool_input}".format(tool=output.tool, 
                                                                                              tool_input=output.tool_input)
                    
                    self.correct_trajectory.append({
                        'tool_name': output.tool,
                        'tool_input': output.tool_input,
                        'log': output.log.split('\n')[0]
                    })
    
            self.thought_execution_chain.append(output.log)
            
        except OutputParserException as e:
            if isinstance(self.handle_parsing_errors, bool):
                raise_error = not self.handle_parsing_errors
            else:
                raise_error = False
            if raise_error:
                raise ValueError(
                    "An output parsing error occurred. "
                    "In order to pass this error back to the agent and have it try "
                    "again, pass `handle_parsing_errors=True` to the AgentExecutor. "
                    f"This is the error: {str(e)}"
                )
            text = str(e)
            if isinstance(self.handle_parsing_errors, bool):
                if e.send_to_llm:
                    observation = str(e.observation)
                    text = str(e.llm_output)
                else:
                    observation = "Invalid or incomplete response"
            elif isinstance(self.handle_parsing_errors, str):
                observation = self.handle_parsing_errors
            elif callable(self.handle_parsing_errors):
                observation = self.handle_parsing_errors(e)
            else:
                raise ValueError("Got unexpected type of `handle_parsing_errors`")
            output = AgentAction("_Exception", observation, text)
            if run_manager:
                run_manager.on_agent_action(output, color="green")
            tool_run_kwargs = self.agent.tool_run_logging_kwargs()
            observation = ExceptionTool().run(
                output.tool_input,
                verbose=self.verbose,
                color=None,
                callbacks=run_manager.get_child() if run_manager else None,
                **tool_run_kwargs,
            )
            return [(output, observation)]
        # If the tool chosen is the finishing tool, then we end and return.
        if isinstance(output, AgentFinish):
            return output
        
        actions: List[AgentAction]
        if isinstance(output, AgentAction):
            actions = [output]
        else:
            actions = output
        result = []
        for agent_action in actions:
            if run_manager:
                run_manager.on_agent_action(agent_action, color="green")
            # Otherwise we lookup the tool
            if agent_action.tool in name_to_tool_map:
                tool = name_to_tool_map[agent_action.tool]
                return_direct = tool.return_direct
                color = color_mapping[agent_action.tool]
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                if return_direct:
                    tool_run_kwargs["llm_prefix"] = ""
                # We then call the tool on the tool input to get an observation
                arguments = tool.run(
                    agent_action.tool_input,
                    verbose=False,
                    color=color,
                    callbacks=run_manager.get_child() if run_manager else None,
                    **tool_run_kwargs,
                )
                observation = "$$PREV[{i}]".format(i=self.tool_count)
               
                #==============================================================================================================
                tool_schema = {      
                    'tool_name': tool.name,
                    'arguments': arguments,       
                }
                web_schema = {      
                    'thought': output.log.split('\n')[0] ,
                    'tool': {
                        'tool_name': tool.name,
                        'arguments': arguments,
                    }                 
                }

                # if self.train_mode :
                #     print("\033[1;35;40m {} \033[0m".format('Checking Argument Correctness... (agent_executor)'))
                #     response, correct_arguments = build_tool_experience(self.ground_truth, self.return_schema+[tool_schema])
                #     if response is False:
                #         tool_schema["arguments"] = correct_arguments

                self.return_schema.append(tool_schema)
                self.web_schema.append(web_schema)

                #==============================================================================================================

            else:
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                observation = InvalidTool().run(
                    {
                        "requested_tool_name": agent_action.tool,
                        "available_tool_names": list(name_to_tool_map.keys()),
                    },
                    verbose=self.verbose,
                    color=None,
                    callbacks=run_manager.get_child() if run_manager else None,
                    **tool_run_kwargs,
                )
            result.append((agent_action, observation))
        return result
    
    

#____________________________________________________________________________________________________

agent_executor = CustomAgentExecutor(
                                agent=agent_obj ,
                                tools=task_tools,
                                verbose=True,
                                return_intermediate_steps=True,
                                handle_parsing_errors=True,
                                )


#____________________________________________________________________________________________________

# ground = '''
# [ 
#  { 
#  "tool_name":  "search_object_by_name", 
#  "arguments":  [ 
#  { 
#  "argument_name":  "query", 
#  "argument_value":  "UltimateCustomer" 
#  } 
# ] 
#  }, 
#  { 
#  "tool_name":  "works_list", 
#  "arguments":  [ 
#  { 
#  "argument_name":  "ticket.rev_org", 
#  "argument_value":  "$$PREV[0]" 
#  } 
#  ] 
#  }, 
#  { 
#  "tool_name":  "summarize_objects", 
#  "arguments":  [ 
#  { 
#  "argument_name":  "objects", 
#  "argument_value":  "$$PREV[1]" 
#  } 
#  ] 
#  } 
#  ]
# '''
# from langchain.callbacks import get_openai_callback

# "For customer 'CustomerA', summarize all high-severity issues and check if similar issues exist in other parts."
# agent_executor.train()
# agent_executor.get_tool_lists(ground)
# with get_openai_callback() as cb:

#     x = agent_executor({"input":'Summarize high severity tickets from the customer UltimateCustomer'})
#     print(x)
#     print('\n\n\n\n' , agent_executor.return_schema)

#     print('\n\n\n\n\n' ,cb.total_cost)

