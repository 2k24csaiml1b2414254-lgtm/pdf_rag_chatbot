import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()


class RAGEngine:
    def __init__(self):
        # HuggingFace hosted embeddings — no local download, works on Vercel
        self.embeddings = HuggingFaceEndpointEmbeddings(
            model="BAAI/bge-small-en-v1.5",
            huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        )
        # Groq LLM — llama3 is fast and free on Groq
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
        )
        self.vectorstore = None
        self.chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    def load_documents(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        loader = PyPDFLoader(file_path) if ext == ".pdf" else TextLoader(file_path, encoding="utf-8")

        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vectorstore.add_documents(chunks)

        self._build_chain()
        return len(chunks)

    def _build_chain(self):
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
            memory=self.memory,
            verbose=False,
        )

    def ask(self, question: str) -> str:
        if self.chain is None:
            return "Please upload a document first."
        result = self.chain.invoke({"question": question})
        return result["answer"]

    def reset(self):
        self.vectorstore = None
        self.chain = None
        self.memory.clear()
