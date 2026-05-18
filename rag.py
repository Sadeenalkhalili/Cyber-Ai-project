from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter#LLMs retrieve better from smaller sections.
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def setup_rag():

    loader = TextLoader("knowledge_base/owasp_guidelines.txt")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(#Searches the vector DB for relevant chunks
        documents=split_docs,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    return retriever