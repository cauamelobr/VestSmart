from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
import shutil
from langchain.embeddings.openai import OpenAIEmbeddings  # Corrected import
from langchain.evaluation import load_evaluator # Correct the import statement

embedding_function = OpenAIEmbeddings(openai_api_key="secret")

DATA_PATH = "data/vestibulares"  # Path to the directory containing the documents   
CHROMA_PATH = "chroma"  # Path to the directory where the Chroma database will be saved 

def main():
    generated_data_store()

def generated_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def split_text(documents: list[Document]): # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Split the text into chunks of 1000 characters
        chunk_overlap=500, # Overlap the chunks by 100 characters
        length_function=len, 
        add_start_index=True, 
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")  # Print the text chunks
    
    document = chunks[5]
    print(document)  # Print the chunk
    
    return chunks

def save_to_chroma(chunks: list[Document]):  # Save the chunks to the Chroma database
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents:
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)

    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")

"""embedding_function = OpenAIEmbeddings()
vector = embedding_function.embed_query("Hello, world!")

print(vector)"""

if __name__ == "__main__":
    main()
