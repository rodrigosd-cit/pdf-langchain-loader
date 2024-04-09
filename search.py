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

def getEmbeddings():
    # Create embeddings for the chunks
    return AzureOpenAIEmbeddings(
                deployment= "text-embedding-ada-002-a",
                azure_endpoint= "https://flow-core-llm-eaus2-ca.openai.azure.com/",
            )

def connectDb():
    # Connect to the existing vector store in the database
    db = PGVecto_rs.from_collection_name(
        embedding=getEmbeddings(),
        db_url=getDbConnection(),
        collection_name="health_artcles")
    
    return db

def find(text, numer_of_chuncks=4):
    return connectDb().similarity_search(text, k=numer_of_chuncks)



def main():
    # Print the search results
    documents = find("covid")
    for doc in documents:
        print(doc.page_content)
        print("======================")
    
if __name__ == "__main__":
    main()