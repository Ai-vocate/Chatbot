# -*- coding: utf-8 -*-
"""Copy of Embeddings_LangChain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C3S9A7shAI5pNwhqIp1r8FJibsJwV8ZS

# Install necessary library
"""

!pip install langchain
!pip install huggingface_hub
!pip install sentence_transformers

"""#Get HUGGINGFACEHUB_API_KEY
This part is setting huggingface API.
Huggingface is a platform for ML engineers to use model easily.</br>
The api code(starting with "hf_") should be your unique one.</br></br>
You can find your API code at [huggingface website](https://huggingface.co).</br>
After signing in(if you dob't have your hugging face account, signing up is free), go to right top profile icon in the website and then click the icon.</br>
You will see the meun at leftside, and go to "Access Token".
Click "New Token" button and you will get your API code.
"""

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

"""# Test run with a text File
This section is test-run to measure performance of this model.</br>
You can just disregard it.
"""

import requests

url = "https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt"
res = requests.get(url)
with open("state_of_the_union.txt", "w") as f:
  f.write(res.text)

# Document Loader
from langchain.document_loaders import TextLoader
loader = TextLoader('./state_of_the_union.txt')
documents = loader.load()

documents

"""# Text preprocessing
This code eliminates unncessary characters of text.</br>
This part is the most basic part model training.
"""

import textwrap

def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text

print(wrap_text_preserve_newlines(str(documents[0])))

# Text Splitter
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

docs[0]

"""# Embeddings
Embedding means vectorization of text data, and vectorization of text data means changing text data(sentences) into numerical values.</br>
Without veterization, model can't understand what text means since computer only understands numbers.</br></br>
The code in this section just importing embedding library, and you don't have to fully understand detailed algorithm of embedding since this is work for CS researchers like Phds.
"""

# Embeddings
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings()

"""#Simiarity
This section imports and executes simiarity metric</br>.
Although there is a built-in simiarity mesurement function at Langchain library, I chose this because it's faster.
"""

!pip install faiss-cpu

# Vectorstore: https://python.langchain.com/en/latest/modules/indexes/vectorstores.html
from langchain.vectorstores import FAISS

db = FAISS.from_documents(docs, embeddings)

#Test-run
#This code doesn't give appropriate answer for query.
#Instead, it will fetch a part from document where a certain word in query occurs most frequently
#In this case, the certain word is "Supreme Court"
query = "What did the president say about the Supreme Court"
docs = db.similarity_search(query)

print(wrap_text_preserve_newlines(str(docs[0].page_content)))

"""# Test1: Create QA Chain
This test-run is conducted with the state_of_the_union.txt file(the document at "Test run with a text file section).
"""

from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

llm=HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature":0, "max_length":512})

chain = load_qa_chain(llm, chain_type="stuff")

query = "Who is the president of the United States?"
docs = db.similarity_search(query)
chain.run(input_documents=docs, question=query) #chain({"input_documents": docs, "question": query}, return_only_outputs=True)

"""# (MAIN PART) Working with PDF Files
Before run the codes below, make sure you run all of the codes above</br>.

"""

!pip install unstructured
!pip install chromadb
!pip install Cython
!pip install tiktoken
!pip install unstructured[local-inference]

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator

# connect your Google Drive
#This code will fetch pdf file from your google drive
from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

pdf_folder_path = '/content/gdrive/MyDrive/Immigration'
os.listdir(pdf_folder_path)

#It will list pdf files in your google drive
loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]
loaders

import nltk
nltk.download('punkt')

#This part will take a lot of time
index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)).from_loaders(loaders)

#Fetching model from Huggingface platform. We will use "Flan-T5"
#Temperature is consistency of answer, and max_length is total length of the answer.
llm=HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature":0, "max_length":512})

from langchain.chains import RetrievalQA
chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=index.vectorstore.as_retriever(),
                                    input_key="question")

"""##Ask question to model"""

chain.run('What should I do if i want to get SSN?')

chain.run("List few things that alien can't do in the US")

chain.run('')

