import json

example_str = '{"applies_to_part": "["RiskManagement" , TTTFB ,  $$PREV[0] ]", "issue.priority": ""high"", "ticket.needs_response": ""True""}'


# Remove unnecessary double quotes around keys and values
example_str = example_str.replace('""', '"').replace('":"', '": "')
example_str= example_str.replace(', ', ', "').replace(' ,', '" ,')
example_str = example_str.replace('""', '"').replace('":"', '": "')
print(example_str)