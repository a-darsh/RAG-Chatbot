from langchain.llms import LlamaCpp
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from document_processor import get_url_content, get_page_urls
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def initialize_chatbot(urls):
    documents = [Document(page_content=get_url_content(url)[1], metadata={'url': url}) for url in urls]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10})

    llm = LlamaCpp(
        model_path="path/to/your/mistral/model",  # Adjust this path
        n_gpu_layers=40,
        n_batch=2048,
        n_ctx=2048,
        temperature=0,
        verbose=False,
        streaming=True,
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, verbose=False)

    return qa_chain

class Chatbot:
    def __init__(self, urls):
        self.qa_chain = initialize_chatbot(urls)

    def get_response(self, user_input):
        try:
            response = self.qa_chain.run(user_input)
            return response
        except Exception as e:
            print(f"Error during chatbot response generation: {e}")
            return "I'm sorry, I couldn't process that."
