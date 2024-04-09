from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.pgvecto_rs import PGVecto_rs
import os

def getDbConnection():
    port = os.getenv("DB_PORT", 5432)
    host = os.getenv("DB_HOST", "localhost")
    username = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "mysecretpassword")
    db_name = os.getenv("DB_NAME", "postgres")

    return f"postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}"

def loadFiles(folder):
    # Load PDF files from a folder and split chuncks
    loader = PyPDFDirectoryLoader(folder)
    return loader.load()

def getEmbeddings():
    # Create embeddings for the chunks
    return AzureOpenAIEmbeddings(
                deployment= "text-embedding-ada-002-a",
                azure_endpoint= "https://flow-core-llm-eaus2-ca.openai.azure.com/",
            )

def saveDocuments(documents):
    # Create the VectorStore from the documents
    db = PGVecto_rs.from_documents(
        documents=documents,
        embedding=getEmbeddings(),
        db_url=getDbConnection(),
        collection_name="health_artcles"
    )

def main():
    documents = loadFiles("files_to_load")
    saveDocuments(documents)
    
if __name__ == "__main__":
    main()