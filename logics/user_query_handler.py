import os
from openai import OpenAI
from helper_functions import llm
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import tiktoken
import json

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_KEY

# Data1 = IDA 
loader1 = PyPDFLoader('C:/Users/Justin Chong/Desktop/PERSONAL/AI BOOTCAMP MATERIALS/Project Type C Assignment/data/Infectious Diseases Act 1976.pdf')
pages1 = loader1.load()

# Data2 = List of Infectious Diseases under IDA
loader2 = PyPDFLoader('C:/Users/Justin Chong/Desktop/PERSONAL/AI BOOTCAMP MATERIALS/Project Type C Assignment/data/list-of-legally-notifiable-infectious-diseases.pdf')
pages2 = loader2.load()
pages = [pages1, pages2]

# Function 1: identify nature of query
def determine_query(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with user queries. \
    The user's query will be enclosed in the pair of {delimiter}.

    Decide if the query is relevant to Infectious Disease Act (IDA) or the List of Diseases within the IDA.
    {pages}

    If query is not relevant, kindly inform the user with the following statement:
    'Sorry, Please try again'.
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    identified_query_str = llm.get_completion_by_messages(messages)
    identified_query_str = identified_query_str.replace("'", "\"")
    identified_query = identified_query_str
    return identified_query

# Function 2: embedding_retrieval
def embedding_retrieval(pages, embeddings_model='text-embedding-3-small'):
    for page in pages:
            text_splitter = RecursiveCharacterTextSplitter(
                 separators=["\n\n", "\n", " ", ""],\
                 chunk_size=50,
                 chunk_overlap=10
            )

            splitted_documents = text_splitter.split_text(page)
            
    vector_store = Chroma.from_documents(
                collection_name=page,
                documents=splitted_documents,
                embedding=embeddings_model,
            )       
    peekaboo = vector_store._collection.peek()

    return peekaboo

# Function 3: generate_response_based_on_course_details
def generate_response_based_on_query(user_message, peekaboo):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is asking about Infectious Disease Act (IDA), \
    extract the information within the pdf. 
    You must only rely on the facts or information in the stated file.
    Your response should be as detail as concise as possible and \
    only provide the most useful information for user to better understand the IDA.:
    {peekaboo}

    Step 2:{delimiter} If the user is asking about List of Infectious Disease within IDA, \
    extract the information within the pdf. 
    You must only rely on the facts or information in the stated file.
    Your response should be as detail as concise as possible and \
    only provide the most useful information for user to better understand the IDA.:
    {peekaboo}

    Step 3:{delimiter} Use the information from pages to \
    generate the answer for the user's query.
    You must only rely on the facts or information in the disease information.
    Your response should be as detail as possible and \
    include information that is useful for user to better understand the complex content.

    Step 4:{delimiter}: Answer the customer in a friendly tone.
    Make sure the statements are factually accurate.
    Your response should be comprehensive and informative to help the \
    the customers to make their decision.
    Use Neural Linguistic Programming to construct your response.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 reasoning>
    Step 4:{delimiter} <step 4 response to user>

    Make sure to include {delimiter} to separate every step.
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_user = llm.get_completion_by_messages(messages)
    response_to_user = response_to_user.split(delimiter)[-1]
    return response_to_user

# Function 4: process_user_message
def process_user_message(user_input):
    delimiter = "```"

    # Process 1: If information is available, look them up
    identified_query = determine_query(user_input)
    print("identified_query : ", identified_query)

    # Process 2: Get the IDA Details or List of Diseases within IIDA
    ida_details = embedding_retrieval(identified_query)

    # Process 3: Generate Response based on Course Details
    reply = generate_response_based_on_query(user_input, ida_details)
    
    return reply, ida_details