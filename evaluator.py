import json
from icecream import ic
import re
import copy

GT = [{'arguments': [{'argument_name': 'created_by', 'argument_value': ['User123']},
                                  {'argument_name': 'owned_by', 'argument_value': ['User123']},
                                  {'argument_name': 'ticket_severity',
                                   'argument_value': ['Critical']},
                                  {'argument_name': 'type', 'argument_value': ['works_list']}],
                    'tool_name': 'works_list'}]

SP = [{'arguments': [{'argument_name': 'issue.severity',
                             'argument_value': 'Critical'},
                            {'argument_name': 'owned_by', 'argument_value': 'User123'}],
              'tool_name': 'works_list'}]

# # GT = json.loads(GT)
# # SP = json.loads(SP)
# ground_truth = [
#     {
#         "tool_name": "whoami",
#         "arguments": []
#     },
#     {
#         "tool_name": "works_list",
#         "arguments": [
#             {
#                 "argument_name": "issue.priority",
#                 "argument_value": "p0"
#             },
#             {
#                 "argument_name": "owned_by",
#                 "argument_value": "$$PREV[0]"
#             }
#         ]
#     },
#     {
#         "tool_name": "prioritize_objects",
#         "arguments": [
#             {
#                 "argument_name": "objects",
#                 "argument_value": "$$PREV[1]"
#             }
#         ]
#     },
#     {
#         "tool_name": "get_sprint_id",
#         "arguments": []
#     },
#     {
#         "tool_name": "add_work_items_to_sprint",
#         "arguments": [
#             {
#                 "argument_name": "work_ids",
#                 "argument_value": "$$PREV[2]"
#             },
#             {
#                 "argument_name": "sprint_id",
#                 "argument_value": "$$PREV[3]"
#             }
#         ]
#     }
# ]

# sample = [
#     {
#         "tool_name": "whoami",
#         "arguments": []
#     },
#     {
#         "tool_name": "works_list",
#         "arguments": [
#             {
#                 "argument_name": "issue.priority",
#                 "argument_value": "p0"
#             },
#             {
#                 "argument_name": "owned_by",
#                 "argument_value": "$$PREV[0]"
#             }
#         ]
#     },
#     {
#         "tool_name": "prioritize_objects",
#         "arguments": [
#             {
#                 "argument_name": "objects",
#                 "argument_value": "$$PREV[1]"
#             }
#         ]
#     },
#     {
#         "tool_name": "get_sprint_id",
#         "arguments": []
#     },
#     {
#         "tool_name": "add_work_items_to_sprint",
#         "arguments": [
#             # {
#             #     "argument_name": "work_ids",
#             #     "argument_value": "$$PREV[2]"
#             # },
#             # {
#             #     "argument_name": "sprint_id",
#             #     "argument_value": "$$PREV[0]",
#             # }
#         ]
#     }
# ]




def remove_digits(string):
    return re.sub(r'[0-9]+', '', string)

def keep_digits(string):
    return re.sub(r'[^\d]+', '', str(string)) 

def top_nodes(data):
    # ic(data)
    data = [{item['tool_name']: {'value': 1, 'arguments': item['arguments']}} for item in data]
    print()

    for i in range(0, len(data)):
        current_tool_name = next(iter(data[i]))
        current_tool_details = data[i][current_tool_name]
        # ic(current_tool_details)
        # Process each argument for the current tool
        for arg in current_tool_details['arguments']:
            arg_value = arg.get('argument_value', '')
            # arg_value = arg['argument_value']
            arg_value = str(arg_value)
            if arg_value.startswith('$$PREV['):
                # Extract the index from the argument value
                ref_index = int(arg_value[7:-1])
                if ref_index < i:
                    # and current_tool_details['value']>0
                    # Get the referenced tool name
                    ref_tool_name = next(iter(data[ref_index]))
                    # Add the value of the referenced tool to the current tool's value
                    current_tool_details['value'] += data[ref_index][ref_tool_name]['value'] 

    updated_tool_values = [{list(item.keys())[0]: item[list(item.keys())[0]]['arguments']} for item in data if item[list(item.keys())[0]]['value']==1 ]
    converted_list = []
    for item in updated_tool_values:
        for tool_name, arguments in item.items():
            converted_list.append({
                "tool_name": tool_name,
                "arguments": arguments
            })
    return converted_list


def format_arg(arg_list: list):
    s  = ""
    for arg  in arg_list:
        s += '\'' + f'{arg[0]}' + '\'' + ', '
    return s

def search_similar_node(check_node_index, check_node, top_ground_truth, ground_truth, sample):
    common_nodes = [gt_node for gt_node in top_ground_truth if check_node["tool_name"] == gt_node["tool_name"]]
    # ic(check_node)
    sample_arguments = sorted([(argument['argument_name'], argument['argument_value']) for argument in check_node['arguments']])
    
    if not common_nodes:
        return (False, ("incorrect tool use, should have used " + ' or'.join([remove_digits(gt_node['tool_name']) for gt_node in top_ground_truth]),[]))

    priority = 0
    # a higher priority means, more stages have been cleared by the node that is being compared to
    reason = ""
    
    for gt_node in common_nodes:
        gt_arguments = sorted([(argument['argument_name'], argument['argument_value']) for argument in gt_node['arguments']])
        # ic(gt_arguments)
        # ic(sample_arguments)
        if len(gt_arguments) != len(sample_arguments):
            if priority < 1:
                if(len(sample_arguments) == 0):
                    reason = f"No! arguments are passed, whereas arguments: {format_arg(gt_arguments)} should be passed"
                else:
                    reason = f"arguments passed are \'{', '.join([arg[0] for arg in sample_arguments])}\' but should be {format_arg(gt_arguments)}"
                priority = 1
            continue
        for arg_gt, arg_sample in zip(gt_arguments, sample_arguments):
            #check if argument name is same
            if arg_gt[0] != arg_sample[0]:
                if priority < 2:
                    reason = f"argument name should have been \'{arg_gt[0]}\' but was \'{arg_sample[0]}\'"
                    priority = 2
                break
            if(type(arg_sample[1]) == bool):
                continue
            if "$" in str(arg_gt[1]) and "$" in str(arg_sample[1]):
                index_gt     = int(keep_digits(arg_gt[1]))
                index_sample = int(keep_digits(arg_sample[1]))

                if  ground_truth[index_gt]["tool_name"] != sample[index_sample]["tool_name"]:
                    if priority < 3:
                        reason = f"argument \'{arg_gt[0]}\' refers to the tool \'{remove_digits(sample[index_sample]['tool_name'])}\' but should have referred to \'{remove_digits(ground_truth[index_gt]['tool_name'])}\'"
                        priority = 3
                    break

                if index_sample >= check_node_index:
                    if priority < 4:
                        reason = f"argument \'{arg_gt[0]}\' refers a tool that is called after current tool"
                        priority = 4
                    break
                    
            else:
                #check if argument value is same (if not reference)
                if arg_gt[1] != arg_sample[1]:
                    if priority < 3:
                        reason = f"argument \'{arg_gt[0]}\' should have been \'{arg_gt[1]}\' but \'{arg_sample[1]}\' was passed"
                        priority = 3
                    break
        else:
            return (True, (gt_node,[]))
    correct_args = gt_node["arguments"]
    # ic(correct_args)
    for i, arg in enumerate(correct_args):
        name, val = arg["argument_name"], arg["argument_value"]
        # ic(name, val)
        if type(val) == str and val.startswith("$$"):
            ind = keep_digits(val)
            correct_args[i]["argument_value"] = f"$$PREV[{ind}]"
    print(reason)
    return (False, ("Tool use was correct but "+reason, correct_args))


def validate(ground_truth, sample, additional_tool=None):
    ground_truth = ground_truth.copy()
    sample = sample.copy()
    current_ground_truth = ground_truth.copy()
    current_sample = sample.copy()
    # ic(ground_truth, sample)
    for i, sample_node in enumerate(sample):
        # ic("Ground Truth")
        top_ground_truth = top_nodes(current_ground_truth)
        # ic("Return Schema")
        top_sample = top_nodes(current_sample)
        # ic(sample_node)
        # ic(sample_node)
        if sample_node not in top_sample:
            # return (False, f"Tool is dependant on other tools that have not been called yet")
            return (False, f"Tool \'{sample_node['tool_name']}\'  with arguments: {', '.join([arg['argument_name']+':'+str(arg['argument_value']) for arg in sample_node['arguments']])} is dependant on other tools that have not been called yet", [])
            
        found, (gt_node, correct_args) = search_similar_node(i, sample_node, top_ground_truth, ground_truth, sample)
        if not found:
##            return (False, f"No match found for tool. Reason: {gt_node[0]}", gt_node[1])
            return (False, f"No match found for tool \'{sample_node['tool_name']}\'. Reason: {gt_node}", correct_args)

        current_sample.remove(sample_node)
        modified_sample_node = sample_node.copy()
        modified_sample_node['tool_name'] += str(i)
        sample[i] = modified_sample_node

        # ic(current_ground_truth,gt_node)
        current_ground_truth.remove(gt_node)
        modified_ground_truth_node = copy.deepcopy(gt_node)
        modified_ground_truth_node['tool_name'] += str(i)
        ground_truth[ground_truth.index(gt_node)] = modified_ground_truth_node  


    if additional_tool:
        top_ground_truth = top_nodes(current_ground_truth)
        top_ground_truth_tools = [tool['tool_name'] for tool in top_ground_truth]

        if additional_tool not in top_ground_truth_tools:
            # return (False, f"Your current progress of tool uses is correct however the last tool use should be ...")
            return (False, f"Your current progress of tool uses is correct however the last tool use should be {'or '.join([tool for tool in top_ground_truth_tools])}", [])
            
    return (True, "", [])

