
import os
from pathlib import Path
from io import BytesIO
from dotenv import load_dotenv

import fitz
import streamlit as st
from docx import Document as DocxDocument
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

# load API key from .env file
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)
api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Legal Contract Analyzer", page_icon="⚖️", layout="wide")
st.title("⚖️ Legal Contract Analyzer")
st.caption("Hybrid RAG for contract Q&A and preliminary risk review. Not a substitute for legal advice.")

SYSTEM_PROMPT = """You are a careful legal contract review assistant.
Use only the supplied excerpts. Never invent clauses, dates, amounts, or obligations.
If evidence is insufficient, say so. Cite filename and page where available.
Separate explicit contract wording from possible issues to review.
Risk flags are preliminary review prompts, not definitive legal conclusions.
Do not claim to be a lawyer or replace qualified legal advice."""

# extract text from uploaded contract files
def extract_file(upload):
    name = upload.name
    ext = name.rsplit(".", 1)[-1].lower()
    data = upload.getvalue()
    docs = []

    if not data:
        raise ValueError(f"{name} is empty.")

    if ext == "pdf":
        with fitz.open(stream=data, filetype="pdf") as pdf:
            for page_no, page in enumerate(pdf, 1):
                text = page.get_text("text").strip()
                if text:
                    docs.append(Document(
                        page_content=text,
                        metadata={"source": name, "page": page_no, "file_type": ext}
                    ))

    elif ext == "docx":
        docx = DocxDocument(BytesIO(data))
        text = "\n".join(p.text for p in docx.paragraphs if p.text.strip())
        if text.strip():
            docs.append(Document(
                page_content=text,
                metadata={"source": name, "page": None, "file_type": ext}
            ))

    elif ext == "txt":
        text = data.decode("utf-8", errors="replace").strip()
        if text:
            docs.append(Document(
                page_content=text,
                metadata={"source": name, "page": None, "file_type": ext}
            ))

    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")

    if not docs:
        raise ValueError(f"No text extracted from {name}. If this is a scanned PDF, OCR is required.")

    return docs


# split documents and create hybrid retriever
def build_retriever(files, embedding_model):
    docs = []
    for file in files:
        docs.extend(extract_file(file))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", "; ", " ", ""]
    )

    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    if not chunks:
        raise ValueError("No text chunks created.")

    embeddings = OpenAIEmbeddings(
        model=embedding_model,
        api_key=api_key
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="legal_contracts"
    )

    dense = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 12, "lambda_mult": 0.65}
    )

    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = 5

    hybrid = EnsembleRetriever(
        retrievers=[dense, bm25],
        weights=[0.6, 0.4]
    )

    return hybrid, len(docs), len(chunks)


# prepare retrieved context with source details
def format_context(docs):
    pieces = []

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        page_label = f", page {page}" if page is not None else ""
        pieces.append(f"[Source: {source}{page_label}]\n{doc.page_content}")

    return "\n\n---\n\n".join(pieces)


# generate answers using retrieved contract information
def ask_rag(question, retriever, model_name, task="question"):
    docs = retriever.invoke(question)
    context = format_context(docs)

    if task == "risk":
        instructions = """Review the excerpts for clauses that may deserve human review.
Focus on termination, payment, renewal, indemnity, liability limits, confidentiality,
data protection, dispute resolution, penalties, and unclear obligations.
For each finding provide topic, evidence, why it may deserve review, preliminary
priority (High/Medium/Low/Not assessed), and source/page. Do not make definitive
legal judgments or assume a clause is missing from excerpts alone."""
    else:
        instructions = """Answer the user's question. Use headings: Answer based on the
contract; Evidence and citations; Potential issues to review; Limitations."""

    prompt = f"""{SYSTEM_PROMPT}

{instructions}

Contract excerpts:
{context}

Question: {question}"""

    llm = ChatOpenAI(
        model=model_name,
        temperature=0,
        api_key=api_key
    )

    answer = llm.invoke(prompt).content

    return {"answer": answer, "documents": docs}
# model settings
embedding_model = "text-embedding-3-large"
baseline_model = "gpt-4o-mini"
tuned_model = os.getenv("LEGAL_FINE_TUNED_MODEL_ID", "")
model_name = tuned_model if tuned_model else baseline_model

# upload contracts
uploads = st.file_uploader(
    "Upload contract(s)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploads:
    st.write("Selected files: " + ", ".join(f.name for f in uploads))

    if st.button("Process and index contracts", type="primary"):
        if not api_key:
            st.error("OpenAI API key not found. Check your .env file.")
        else:
            try:
                with st.spinner("Extracting text and building Hybrid RAG index..."):
                    retriever, sections, chunks = build_retriever(uploads, embedding_model)

                st.session_state["retriever"] = retriever
                st.session_state["files"] = [f.name for f in uploads]
                st.session_state["sections"] = sections
                st.session_state["chunks"] = chunks

                st.session_state.pop("last_result", None)
                st.session_state.pop("risk_result", None)

                st.success("Contracts indexed successfully!")

            except Exception as e:
                st.error(f"Indexing failed: {e}")


# display results after indexing
if st.session_state.get("retriever") is not None:
    st.metric("Pages / text sections", st.session_state["sections"])

    st.caption("Indexed: " + ", ".join(st.session_state["files"]))

    tab1, tab2, tab3 = st.tabs([
        "Ask the contract",
        "Risk review",
        "Evidence"
    ])

    # contract question answering
    with tab1:
        with st.form("question_form"):
            question = st.text_input(
                "Ask a question",
                placeholder="What notice period is required for termination?"
            )
            submitted = st.form_submit_button("Get answer")

        if submitted:
            if not question.strip():
                st.warning("Enter a question first.")
            elif not api_key:
                st.error("OpenAI API key not found.")
            else:
                try:
                    with st.spinner("Searching evidence and generating answer..."):
                        st.session_state["last_result"] = ask_rag(
                            question,
                            st.session_state["retriever"],
                            model_name
                        )
                except Exception as e:
                    st.error(f"Could not answer question: {e}")

        if st.session_state.get("last_result"):
            st.markdown(st.session_state["last_result"]["answer"])


    # preliminary contract risk review
    with tab2:
        st.write("Risk labels are review prompts, not legal conclusions.")

        if st.button("Analyze potential risks"):
            if not api_key:
                st.error("OpenAI API key not found.")
            else:
                try:
                    with st.spinner("Reviewing retrieved clauses..."):
                        st.session_state["risk_result"] = ask_rag(
                            "Review potential risks in this contract.",
                            st.session_state["retriever"],
                            model_name,
                            task="risk"
                        )
                except Exception as e:
                    st.error(f"Risk review failed: {e}")

        if st.session_state.get("risk_result"):
            st.markdown(st.session_state["risk_result"]["answer"])


    # display retrieved evidence
    with tab3:
        result = st.session_state.get("last_result")

        if result:
            for i, doc in enumerate(result["documents"], 1):
                source = doc.metadata.get("source", "Unknown source")
                page = doc.metadata.get("page")
                label = f"{i}. {source}" + (f" · Page {page}" if page else "")

                with st.expander(label):
                    st.write(doc.page_content)
        else:
            st.info("Ask a question first to view the retrieved evidence.")

    st.divider()
    st.caption(
        "Privacy: extracted contract text is sent to your configured embedding and LLM providers. "
        "Only upload documents you are authorized to process."
    )

else:
    st.info("Upload one or more contracts, then click Process and index contracts.")
