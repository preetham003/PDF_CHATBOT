import fitz  # PyMuPDF
import re
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import re
import chromadb
import openai
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI 

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")


# Replace with your OpenAI API key
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
  message_content = response.choices[0].message.content

  return message_content

def answer_user_query(user_query, query_related_text):
  """
  Attempts to answer a user query using the provided related text.

  Args:
      user_query: The user's query (string).
      query_related_text: Text related to the user's query (string).

  Returns:
      A string containing the generated answer or an error message.
  """

  try:
    # Craft a prompt that instructs the AI to find the answer in the text
    prompt_template = PromptTemplate.from_template(
        "The user asked: {query}\n"
        "Find the answer to the question from the following text:\n"
        "{text}\n\n"
        "Answer:"
    )
    # Construct the complete prompt with the user query and related text
    prompt = prompt_template.format(query=user_query, text=query_related_text)
    response = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
              {
                  "role": "user",
                  "content": prompt,
              },
          ]
      )
    return str(response) # converting the response into a string
  except Exception as e:
    # Handle potential errors during answer generation
    error_message = f"An error occurred while generating the answer: {e}"
    return error_message

def extract_text_from_pdf(pdf_path):
    text = ''
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]

        # Extract text from the page
        text += page.get_text()

    # Close the PDF document
    pdf_document.close()

    return text

def justify_text(paragraph, line_width):
    words = paragraph.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        if current_width + len(word) <= line_width:
            current_line.append(word)
            current_width += len(word) + 1  # Include space after word
        else:
            lines.append(current_line)
            current_line = [word]
            current_width = len(word) + 1  # Include space after word

    if current_line:
        lines.append(current_line)

    justified_lines = []
    for line in lines:
        if len(line) > 1:
            total_spaces_needed = line_width - sum(len(word) for word in line)
            space_gaps = len(line) - 1
            spaces_per_gap = total_spaces_needed // space_gaps
            extra_spaces = total_spaces_needed % space_gaps

            justified_line = ''
            for i, word in enumerate(line):
                justified_line += word
                if i < space_gaps:
                    justified_line += ' ' * (spaces_per_gap + (i < extra_spaces))
            justified_lines.append(justified_line)
        else:
            justified_lines.append(line[0])

    return '\n'.join(justified_lines)

def single_line_text(paragraph):
    # Remove line breaks and extra spaces
    single_line = ' '.join(paragraph.split())
    return single_line

pdf_files = ['fess1ps.pdf', 'fess101.pdf','fess102.pdf', 'fess103.pdf', 'fess104.pdf','fess105.pdf']

text=''
# Iterate through each PDF file and extract text
for pdf_file_path in pdf_files:
    extracted_text = extract_text_from_pdf(pdf_file_path)
    justified_paragraph = single_line_text(extracted_text)
    text+=justified_paragraph
    print(justified_paragraph)
    print('-' * 80)

# def get_text_chunks(text):
#   """Splits text into smaller chunks for processing."""
#   text_splitter = CharacterTextSplitter(
#       separator="\n",
#       chunk_size=900,
#       chunk_overlap=0,
#       length_function=len
#   )
#   chunks = text_splitter.split_text(text)
#   return chunks

def get_text_chunks(text):
    """Splits text into smaller chunks of 1000 characters each."""
    chunk_size = 15000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

chunks=get_text_chunks(text)
print("length",len(chunks))
chunks=chunks[:5]
print("chunks::",chunks)
print(type(chunks))
for chunk in chunks:
   print("==="*50)
   print(len(chunk))
   print("==="*50)
   print("summarariesss",generate_text_summary(chunk))

# storings ids
chroma_ids=[]
for i in range(1,len(chunks)+1):
   chroma_ids.append((f"doc_{i}"))

#stroing chunks and theirs indexs 
chroma_metadatas=[]
for txt in chunks:
   d={str(chunks.index(txt)):txt}
   chroma_metadatas.append(d)
print("chroma_metadatas::",chroma_metadatas)

#storing the summaries of text chunks
chroma_documents=[]
for txt in chunks:
   chroma_documents.append(generate_text_summary(txt))
print("chroma_documents::",chroma_documents)

#Add summaries, chunks, ids
collection.add(
    documents=chroma_documents,
    metadatas=chroma_metadatas,
    ids=chroma_ids
)

#Retrieves related text to user query
def get_related_txt(query):
  results = collection.query(
      query_texts=[query],
      n_results=2
  )  
  return results

user_query='Who is Arun Chitkara?'
query_related_text=get_related_txt(user_query)
print("==="*50)
print("Related Text::",query_related_text)
print("==="*50)
result=answer_user_query(user_query, query_related_text)


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