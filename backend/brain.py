import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()

class ChatBrain:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "google").lower()
        self.vector_db = None
        self.qa_chain = None
        self._setup_llm()

    def _setup_llm(self):
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found")
            self.embeddings = OpenAIEmbeddings()
            # GPT-4o is a good default, can be changed to gpt-5 once available
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
        else:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found")
            genai.configure(api_key=api_key)
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

    def index_documents(self, data_dir: str):
        """Indexes all PDFs in the given directory."""
        documents = []
        for file in os.listdir(data_dir):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(data_dir, file))
                documents.extend(loader.load())
        
        if not documents:
            print("No PDF documents found to index.")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        
        self.vector_db = Chroma.from_documents(
            documents=texts, 
            embedding=self.embeddings,
            persist_directory=os.path.join(data_dir, "chroma_db")
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            return_source_documents=True
        )

    def ask(self, question: str):
        """Answers a question based on indexed documents."""
        if not self.qa_chain:
            # Fallback to direct LLM if no docs indexed
            response = self.llm.invoke(question)
            return response.content, []
        
        result = self.qa_chain.invoke({"query": question})
        answer = result["result"]
        sources = [doc.metadata.get("source") for doc in result["source_documents"]]
        return answer, list(set(sources))

# Singleton instance
brain = ChatBrain()
