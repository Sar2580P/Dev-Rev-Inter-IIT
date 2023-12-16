import ast

def fix_extra_quotes(text):
  """
  Removes extra inverted commas around the entire string if present.

  Args:
    text: The string to be processed.

  Returns:
    The processed string without extra inverted commas.
  """
  if text.startswith('"') and text.endswith('"'):
    # Remove leading and trailing double quotes
    text = text[1:-1]
  return text

# Example usage
text = '"["Ultimate Customer", "ABC"] "'
fixed_text = fix_extra_quotes(text)
print(fixed_text)
print('***')
try:
  # Use ast.literal_eval after removing extra quotes
  data = ast.literal_eval(fixed_text)
  print(f"Data after removing extra quotes: {data}")
except SyntaxError:
  print(f"Error parsing '{fixed_text}'. Extra quotes might not be the issue.")