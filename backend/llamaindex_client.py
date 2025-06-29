from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever

def setup_retriever():
    documents = SimpleDirectoryReader("rag_docs").load_data()
    node_parser = SentenceSplitter(chunk_size=256, chunk_overlap=32)
    nodes = node_parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return VectorIndexRetriever(index=index, similarity_top_k=2)

retriever = setup_retriever()

def get_context(user_id, prompt=None):
    if prompt:
        results = retriever.retrieve(prompt)
        return "\n".join([n.get_content() for n in results])
    return "No context found."
