from rag import setup_rag

retriever = setup_rag()

query = "SSH password authentication vulnerability"

docs = retriever.invoke(query)

for doc in docs:
    print("\n====================")
    print(doc.page_content)