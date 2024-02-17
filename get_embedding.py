from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
from langchain_pinecone import Pinecone


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["PINECONE_API_KEY"] = os.getenv('PINECONE_API_KEY')

index_name = "loi"
loader = PyPDFLoader("book_ted.pdf")
def get_embd():
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    return Pinecone.from_documents(docs, embeddings, index_name=index_name)