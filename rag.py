from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

#without splitting be3amel kul file la7aloh 
def setup_rag():

    loader = DirectoryLoader(
        "knowledge_base",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 1}
    )

    return retriever