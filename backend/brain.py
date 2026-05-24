import os
import json
from dotenv import load_dotenv

# --- AI DEPENDENCIES (COMMENTED OUT FOR FUTURE USE) ---
# import google.generativeai as genai
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# -------------------------------------------------------

load_dotenv()

class ChatBrain:
    def __init__(self):
        # --- AI CONFIGURATION (COMMENTED OUT) ---
        # Description: Handles provider selection and initialization for Gemini/GPT.
        # self.provider = os.getenv("LLM_PROVIDER", "google").lower()
        # self.vector_db = None
        # self.qa_chain = None
        # self._setup_llm()
        # ------------------------------------------
        
        # FAQ Configuration (Active)
        self.faq_data = self._load_faq()

    def _load_faq(self):
        """Loads predefined questions and answers from faq.json."""
        faq_path = os.path.join(os.path.dirname(__file__), "faq.json")
        if os.path.exists(faq_path):
            with open(faq_path, "r") as f:
                return json.load(f).get("predefined_questions", [])
        return []

    # --- AI SETUP METHOD (COMMENTED OUT) ---
    # def _setup_llm(self):
    #     """Initializes the LLM (OpenAI or Gemini) based on environment variables."""
    #     if self.provider == "openai":
    #         api_key = os.getenv("OPENAI_API_KEY")
    #         if not api_key:
    #             raise ValueError("OPENAI_API_KEY not found")
    #         self.embeddings = OpenAIEmbeddings()
    #         self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    #     else:
    #         api_key = os.getenv("GOOGLE_API_KEY")
    #         if not api_key:
    #             raise ValueError("GOOGLE_API_KEY not found")
    #         genai.configure(api_key=api_key)
    #         self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    #         self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    # ------------------------------------------

    # --- AI DOCUMENT INDEXING (COMMENTED OUT) ---
    def index_documents(self, data_dir: str):
        """AI Implementation: Indexes all PDFs in the given directory using RAG."""
        # documents = []
        # for file in os.listdir(data_dir):
        #     if file.endswith(".pdf"):
        #         loader = PyPDFLoader(os.path.join(data_dir, file))
        #         documents.extend(loader.load())
        # if not documents: return
        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        # texts = text_splitter.split_documents(documents)
        # self.vector_db = Chroma.from_documents(documents=texts, embedding=self.embeddings, 
        #                                         persist_directory=os.path.join(data_dir, "chroma_db"))
        # self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", 
        #                                             retriever=self.vector_db.as_retriever(), return_source_documents=True)
        pass
    # ------------------------------------------

    def ask(self, question: str):
        """Answers a question based on predefined FAQ (Rule-based)."""
        # --- AI ASK LOGIC (COMMENTED OUT) ---
        # if self.qa_chain:
        #     result = self.qa_chain.invoke({"query": question})
        #     return result["result"], [doc.metadata.get("source") for doc in result["source_documents"]]
        # --------------------------------------

        # FAQ Logic (Active)
        question_lower = question.lower()
        for item in self.faq_data:
            if item["question"].lower() in question_lower or question_lower in item["question"].lower():
                return item["answer"], ["Predefined FAQ"]
        
        return "I'm sorry, I don't have a predefined answer for that. How else can I help you?", []

# Singleton instance
brain = ChatBrain()
