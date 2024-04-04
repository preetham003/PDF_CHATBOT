# from openai import ChatCompletion, Choice

# Assuming you have the ChatCompletion object stored in a variable called chat_completion_obj
result="ChatCompletion(id='chatcmpl-9ADBLeZCkEFY3ByHRleCt6rL0cZRa', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Arun Chitkara is mentioned in the provided text as the Division Chief Production Officer of the Publication Team in the context of the publication of a history textbook for Class VI.', role='assistant', function_call=None, tool_calls=None))], created=1712220979, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_b28b39ffa8', usage=CompletionUsage(completion_tokens=36, prompt_tokens=4386, total_tokens=4422))"
# Assuming you have the ChatCompletion object stored in a variable called chat_completion_obj

# Assuming you have the 'result' variable as described in your question

import re

# Define the regular expression pattern to match the content field
pattern = r"content='([^']*)'"

# Search for the pattern in the result string
match = re.search(pattern, result)

if match:
    # Extract the content from the matched group
    content = match.group(1)
    print("Extracted Content:")
    print(content)
else:
    print("No content found in the result string.")



