# Legal-Contract-Analyzer

# ⚖️ Legal Contract Analyzer
### AI-Powered Contract Intelligence Using Hybrid Retrieval-Augmented Generation (RAG)

## 📌 Project Overview

The **Legal Contract Analyzer** is an AI-powered application designed to simplify the process of understanding and analyzing legal contracts using **Hybrid Retrieval-Augmented Generation (RAG)**.

Legal contracts often contain lengthy clauses, complex terminology, and important conditions that can be difficult to understand. This application allows users to upload legal documents and interact with them through a conversational Question-Answering system.

It combines keyword-based retrieval (BM25) and semantic search (vector embeddings) to retrieve relevant information from uploaded contracts. The retrieved context is then passed to a Large Language Model (LLM) to generate relevant, context-aware responses.

The primary objective is to make legal document analysis faster, more accessible, and easier to understand.

## 🎯 Objectives

- Simplify the understanding of complex legal documents.
- Extract meaningful information from uploaded contracts.
- Implement Hybrid RAG for improved document retrieval.
- Generate context-aware answers using Large Language Models.
- Reduce the time required for manual contract review.
- Provide an interactive interface for contract-based question answering.

## ✨ Key Features

### 1. Document Upload
- Upload legal documents in PDF, DOCX, and TXT formats.
- Extract text from uploaded documents.
- Process documents for further analysis.

### 2. Intelligent Document Processing
- Extract text from legal documents.
- Split extracted text into smaller chunks.
- Generate vector embeddings for semantic representation.
- Store document embeddings in ChromaDB.

### 3. Hybrid Information Retrieval
Combines two retrieval approaches:

- **BM25 Retriever:** Retrieves relevant information based on keyword matching.
- **Dense Vector Retriever:** Retrieves semantically similar content using embeddings.

Both retrieval results are combined using an Ensemble Retriever to improve the relevance of retrieved information.

### 4. AI-Powered Question Answering
- Ask natural-language questions about uploaded contracts.
- Retrieve relevant contract sections.
- Generate answers using the LLM.
- Provide responses grounded in the uploaded contract context.

### 5. Interactive Streamlit Interface
- Simple and user-friendly interface.
- Upload and analyze contracts.
- Ask questions through a conversational interface.
- Receive AI-generated responses.

## 🏗️ System Architecture

The application follows a Hybrid RAG architecture.

**Document Processing Pipeline:**

1. Upload legal contract.
2. Extract text from the document.
3. Split text into smaller chunks.
4. Generate embeddings.
5. Store embeddings in ChromaDB.
6. Build the BM25 keyword retriever.

**Question Answering Pipeline:**

1. User enters a question.
2. BM25 retrieves keyword-relevant chunks.
3. Vector search retrieves semantically relevant chunks.
4. Ensemble Retriever combines retrieval results.
5. Retrieved context is passed to the LLM.
6. LLM generates a context-aware response.
7. Response is displayed in Streamlit.

## 🔄 Workflow

```text
       User Uploads Contract
                |
                v
        Document Extraction
                |
                v
         Text Processing
                |
                v
          Text Chunking
                |
          +-----+------+
          |            |
          v            v
     BM25 Index    Embeddings
          |            |
          |            v
          |         ChromaDB
          |            |
          +-----+------+
                |
                v
         User Asks Question
                |
                v
        Hybrid Retrieval
                |
                v
       Ensemble Retriever
                |
                v
         Relevant Context
                |
                v
           LLM Processing
                |
                v
        Generated Answer
                |
                v
        Streamlit Interface
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| LangChain | RAG pipeline orchestration |
| OpenAI GPT | Natural-language response generation |
| OpenAI Embeddings | Semantic vector representation |
| ChromaDB | Vector database |
| BM25 | Keyword-based retrieval |
| Ensemble Retriever | Hybrid retrieval |
| PyMuPDF (fitz) | PDF text extraction |
| python-docx | DOCX text extraction |

## 🧠 Hybrid RAG Approach

The project uses Hybrid Retrieval-Augmented Generation to improve the quality of information retrieval.

**Keyword-Based Retrieval (BM25)**

BM25 identifies relevant document chunks by matching query keywords with document content. It is useful when searching for exact legal terminology, clause names, and specific terms.

**Semantic Retrieval (Dense Retrieval)**

Dense retrieval converts text into numerical vector embeddings. It identifies relevant information based on semantic similarity, even when the wording of the question differs from the contract.

**Ensemble Retrieval**

The Ensemble Retriever combines the results from both retrieval methods to provide more comprehensive and relevant context to the LLM.

## 📂 Project Structure

```text
Legal-Contract-Analyzer/
│
├── app.py
│
├── requirements.txt
│
├── .env
│
├── README.md
│
└── sample_contracts/
    ├── contract1.pdf
    ├── contract2.pdf
    └── contract3.pdf
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd Legal-Contract-Analyzer
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file in the project directory.

```env
OPENAI_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💡 Example Use Cases

Users can ask questions such as:

- What is the purpose of this contract?
- Who are the parties involved?
- What are the termination conditions?
- What are the payment obligations?
- What happens if either party breaches the agreement?
- What is the duration of this agreement?
- Are there any confidentiality obligations?
- What are the responsibilities of each party?
- What are the potential risks mentioned in this contract?
- Can you explain this clause in simple language?

## ⚠️ Limitations

- The quality of responses depends on the quality and completeness of the uploaded document.
- Complex legal terminology may require additional interpretation.
- Retrieval may not always identify every relevant clause.
- LLM-generated responses may contain inaccuracies or omit important details.
- The application is not a substitute for professional legal advice.

## 🚀 Future Enhancements

- Automatic identification of high-risk contractual clauses.
- Contract summarization.
- Clause-wise risk classification.
- Highlighting important contractual obligations.
- Comparison of multiple legal contracts.
- Extraction of parties, dates, amounts, and obligations.
- Source citations with page numbers and clause references.
- Integration of legal-domain-specific language models.
- Improved evaluation using RAGAS metrics.

## 🔐 Disclaimer

This application is developed for educational and informational purposes. It provides AI-assisted contract analysis and should not be considered a substitute for professional legal advice. All generated responses should be independently verified before making legal or business decisions.

## 👩‍💻 Author

**Akankssha Adepu**

B.Tech – Computer Science and Engineering

Project: Legal Contract Analyzer

**Technologies:** Python | Generative AI | Hybrid RAG | LangChain | Streamlit | ChromaDB
