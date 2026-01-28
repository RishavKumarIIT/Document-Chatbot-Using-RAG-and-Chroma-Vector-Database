from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from google.genai import Client

import requests
import os
from pathlib import Path
import shutil
from urllib.parse import urlparse


client = Client(api_key="AIzaSyDPk29Tp51F2d6u_tQL0xuw5eti8k88b5Y") 


def recreate_folder(path="./data"):
    folder = Path(path)

    if folder.exists() and folder.is_dir():
        shutil.rmtree(folder)

    folder.mkdir(parents=True, exist_ok=True)

    print(f" Folder ready: {folder}")
    return str(folder)





def download_file(url, folder_path):
    os.makedirs(folder_path, exist_ok=True)

    response = requests.get(url, stream=True)
    response.raise_for_status()
    print("response ",response)

    filename = None
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        for part in content_disposition.split(";"):
            if "filename=" in part:
                filename = part.split("=")[1].strip("\"")
                break

    if not filename:
        filename = os.path.basename(urlparse(url).path)

    if not filename or filename == "uc":
        filename = "downloaded_file"

    save_path = os.path.join(folder_path, filename)

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return save_path




def detect_file_types(folder_path):
    if not os.path.exists(folder_path):
        print("Folder does not exist")
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_name)[1].lower()

            if ext == ".txt":
                print(f"{file_name} → Text file")
                return Load_text(file_path)

            elif ext == ".pdf":
                print(f"{file_name} → PDF file")
                return Load_pdf(file_path)

            elif ext in [".xls", ".xlsx"]:
                print(f"{file_name} → Excel file")

            elif ext == ".csv":
                print(f"{file_name} → CSV file")

            elif ext == ".docx":
                print(f"{file_name} → Word document")

            elif ext in [".jpg", ".jpeg", ".png"]:
                print(f"{file_name} → Image file")

            elif ext in [".mp4", ".avi", ".mkv"]:
                print(f"{file_name} → Video file")

            else:
                print(f"{file_name} → Unknown file type")



def Load_pdf(path):
    loader = PyPDFLoader(path)
    docs = loader.load()
    print("docs:", docs)
    return docs

def Load_text(path):
    loader=TextLoader(path)
    doc=loader.load()
    print("doc ",doc)
    return doc

def splitting(documents):
    text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=500,
       chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)
    print("chunks ",chunks)
    return chunks

def LoadEmbeddingModel():
    embedding_model = HuggingFaceEmbeddings(
       model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedding_model



def Storeingvector(chunks,embedding_model):
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./chroma_db"
    )

    vectorstore.persist()
    return vectorstore

def RetriveSimilarVector(vectorstore,query):
    retrieved_docs = vectorstore.similarity_search(
       query,
       k=3
    )
    return retrieved_docs

def BuildPrompt(retrieved_docs):
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    query=""
    for mes in chat_history:
        query+=f"{mes["role"]}:\n{mes["content"]}\n\n"

    prompt = f"""
    Answer the latest query in chat history using the context below.

    Context:
    {context}

    chat history:
    {query}
    """
    return prompt

def AskLLM(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt
        ]
    )
    return response.text



chat_history=[]

def PrepareData(url):
    data_path=recreate_folder()
    download_file(url,data_path)
    doc=detect_file_types(data_path)
    # doc=LoadDoc("data/test.txt")
    chunks=splitting(doc)
    embedding_model=LoadEmbeddingModel()
    vector_store=Storeingvector(chunks,embedding_model)
    chat_history.clear()
    return vector_store


def Ask(query,vectorstore):
    if vectorstore==None:
        print("quer1y ",query)
    chat_history.append({"role":"user","content":query})
    req_doc=RetriveSimilarVector(vectorstore,query)
    prompt=BuildPrompt(req_doc)
    print("[prompt ",prompt)
    response=AskLLM(prompt)
    print("response ",response)
    chat_history.append({"role":"llm","content":response})
    return response
















    