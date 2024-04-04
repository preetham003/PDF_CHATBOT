from openai import OpenAI
import openai
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI 

openai.api_key = "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"

def generate_text_summary(text_to_summarize):
  """
  Summarizes a given text using the OpenAI API and GPT-3.5 model.

  Args:
      text_to_summarize: The text to be summarized (string).

  Returns:
      A string containing the summarized text.
  """

  # Define a clear prompt template
  prompt_template = PromptTemplate.from_template(
      "Can you summarize the following text for me?\n{text}\n\nSummary:"
  )

  # Construct the complete prompt with the user-provided text
  prompt = prompt_template.format(text=text_to_summarize)
  # Use openai.Completion.create for text generation

  response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )

  # Extract the generated summary from the response
  message_content = response.choices[0].message.content

  return message_content

# Example usage
text_to_summarize = """This is a long and informative text that covers various topics.
It includes details, explanations, and examples.
I would like you to summarize the key points of this text."""

summary = generate_text_summary(text_to_summarize)
print(f"Summary: {summary}")