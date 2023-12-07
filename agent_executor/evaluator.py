import json
from icecream import ic

def top_nodes(data):
    data = [{item['tool_name']: {'value': 1, 'arguments': item['arguments']}} for item in data]
    # ic(data)
    for i in range(0, len(data)):
        current_tool_name = next(iter(data[i]))
        current_tool_details = data[i][current_tool_name]
        # ic(current_tool_details)
        # Process each argument for the current tool
        for arg in current_tool_details['arguments']:
            ic(type(arg))
            arg_value = arg.get('argument_value', '')
            print(type(arg_value))
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


def search_similar_node(check_node_index, check_node, top_ground_truth, ground_truth, sample):
    common_nodes = [gt_node for gt_node in top_ground_truth if check_node["tool_name"] == gt_node["tool_name"]]
    sample_arguments = sorted([(argument["argument_name"], argument["argument_value"]) for argument in check_node["arguments"]])
    
    if not common_nodes:
        return (False, "incorrect tool use, should have used " + ' or'.join([gt_node["tool_name"] for gt_node in top_ground_truth]))

    priority = 0
    # a higher priority means, more stages have been cleared by the node that is being compared to
    reason = ""
    
    for gt_node in common_nodes:
        gt_arguments = sorted([(argument["argument_name"], argument["argument_value"]) for argument in gt_node["arguments"]])
        if len(gt_arguments) != len(sample_arguments):
            if priority < 1:
                reason = f"arguments passed are {', '.join([arg[0] for arg in sample_arguments])} but should be {', '.join([arg[0] for arg in gt_arguments])}"
                priority = 1
            continue
        for arg_gt, arg_sample in zip(gt_arguments, sample_arguments):
            #check if argument name is same
            if arg_gt[0] != arg_sample[0]:
                if priority < 2:
                    reason = f"argument name should have been {arg_gt[0]} but was {arg_sample[0]}"
                    priority = 2
                break
            
            if arg_gt[1].startswith("$") and arg_sample[1].startswith("$"):
                index_gt     = int(arg_gt[1][7:-1])
                index_sample = int(arg_sample[1][7:-1])


                if  ground_truth[index_gt]["tool_name"] != sample[index_sample]["tool_name"]:
                    if priority < 3:
                        reason = f"argument {arg_gt[0]} refers to incorrect tool"
                        priority = 3
                    break

                if index_sample >= check_node_index:
                    if priority < 4:
                        reason = f"argument {arg_gt[0]} refers a tool that is called after current tool"
                        priority = 4
                    break
                    
            else:
                #check if argument value is same (if not reference)
                if arg_gt[1] != arg_sample[1]:
                    if priority < 3:
                        reason = f"argument {arg_gt[0]} value mismatch"
                        priority = 3
                    break
        else:
            return (True, gt_node)
    return (False, reason)



def validate(ground_truth, sample, additional_tool=None):
    ic("Hello")
    ground_truth = ground_truth.copy()
    sample = sample.copy()
    current_ground_truth = ground_truth.copy()
    current_sample = sample.copy()
    ic(ground_truth, sample)
    for i, sample_node in enumerate(sample):
        # ic("Ground Truth")
        top_ground_truth = top_nodes(current_ground_truth)
        # ic("Return Schema")
        top_sample = top_nodes(current_sample)
        # ic(sample_node)

        if sample_node not in top_sample:
            return (False, f"{json.dumps(sample_node)} is dependant on other tools that have not been called yet")
            
        found, gt_node = search_similar_node(i, sample_node, top_ground_truth, ground_truth, sample)
        if not found:
            return (False, f"No match found for tool {json.dumps(sample_node)} at index {i}. Reason: {gt_node}")

        current_sample.remove(sample_node)
        modified_sample_node = sample_node.copy()
        modified_sample_node["tool_name"] += str(i)
        sample[i] = modified_sample_node

        current_ground_truth.remove(gt_node)
        modified_ground_truth_node = gt_node.copy()
        modified_ground_truth_node["tool_name"] += str(i)
        ground_truth[ground_truth.index(gt_node)] = modified_ground_truth_node

    if additional_tool:
        top_ground_truth = top_nodes(current_ground_truth)
        top_ground_truth_tools = [tool["tool_name"] for tool in top_ground_truth]

        if additional_tool not in top_ground_truth_tools:
            return (False, f"Your current progress of tool uses is correct however the last tool use should be {'or '.join(top_ground_truth_tools)}")
            
    return (True, "")