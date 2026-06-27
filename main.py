import streamlit as st
import os
import time
import google.generativeai as genai
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, PyPDFium2Loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Hardcoded API Key ---
GEMINI_API_KEY = "AQ.Ab8RN6J1wLOo1s13UJ2m-D2iolhKq5mqVSqr91aCjCEEjsEu9w"
genai.configure(api_key=GEMINI_API_KEY)

# --- Professional Page Config ---
st.set_page_config(
    page_title="DocuChat AI | Enterprise RAG", 
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UI Custom Themes (CSS Injection) ---
st.markdown("""
    <style>
    /* Main Background & Title Alignment */
    .reportview-container { background: #111216; }
    .main-title { font-size: 2.6rem; font-weight: 800; color: #F0F2F6; margin-bottom: 0.5rem; }
    .sub-title { font-size: 1.1rem; color: #A3A8B4; margin-bottom: 2rem; }
    
    /* Elegant Cards */
    .metric-card {
        background-color: #1E2028;
        border: 1px solid #2E3344;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
    }
    
    /* De-escalated Secondary Neutral Button Style */
    div.stButton > button:first-child {
        background-color: #2E3344;
        color: #F0F2F6;
        border-radius: 8px;
        border: 1px solid #43495E;
        width: 100%;
        padding: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #3D445A;
        border-color: #FF4B4B;
        color: #FF4B4B;
    }
    
    /* Citation Text Styles */
    .citation-header { font-size: 0.85rem; font-weight: bold; color: #FF9100; margin-top: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "db" not in st.session_state:
    st.session_state.db = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False
if "doc_preview" not in st.session_state:
    st.session_state.doc_preview = ""
if "metadata" not in st.session_state:
    st.session_state.metadata = {}

# --- Top Header Section ---
st.markdown('<div class="main-title">📄 DocuChat AI: Advanced Document Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload academic reports, data documentations, or system structures to chat with deep-context insights.</div>', unsafe_allow_html=True)

# --- Sidebar Panel Dashboard ---
with st.sidebar:
    st.markdown("### ⚙️ Control Dashboard")
    
    if st.button("🗑️ Reset Application Context"):
        st.session_state.clear()
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    if st.session_state.file_processed:
        st.markdown(f"""
        <div class="metric-card">
            <span style='color: #00E676; font-weight: bold;'>● Pipeline Active</span><br><br>
            <b>📄 File:</b> {st.session_state.metadata.get('filename', 'Unknown')}<br>
            <b>📦 Vector Store:</b> ChromaDB (Active)<br>
            <b>🧠 Engine:</b> Gemini 2.5 Flash Lite
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"🧩 **Total Chunks Split:** {st.session_state.metadata.get('chunks', 0)} blocks")
        st.progress(min(st.session_state.metadata.get('chunks', 0) / 100, 1.0))
    else:
        st.markdown("""
        <div class="metric-card" style='border-color: #E53935;'>
            <span style='color: #FF5252; font-weight: bold;'>○ No Active Document</span><br><br>
            Upload a file in the main area to instantiate the vector memory graph database environment.
        </div>
        """, unsafe_allow_html=True)

# --- Main Application Split Layout ---
col_main, col_preview = st.columns([1.8, 1.2], gap="large")

with col_main:
    uploaded_file = st.file_uploader("Upload Target Context Document", type=["txt", "pdf", "docx"], label_visibility="collapsed")

    if uploaded_file:
        if not st.session_state.file_processed:
            start_time = time.time()
            
            temp_filename = uploaded_file.name
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_extension = temp_filename.split(".")[-1].lower()

            if file_extension == "pdf":
                loader = PyPDFium2Loader(temp_filename)
            elif file_extension == "docx":
                loader = Docx2txtLoader(temp_filename)
            else:
                loader = TextLoader(temp_filename)

            with st.spinner("⚡ Initializing neural embedding pipeline..."):
                documents = loader.load()
                
                total_text_length = sum([len(doc.page_content) for doc in documents])
                estimated_tokens = int(total_text_length / 4)
                
                preview_text = ""
                for doc in documents[:3]:
                    preview_text += doc.page_content + "\n"
                st.session_state.doc_preview = preview_text[:3000]

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=250)
                chunks = text_splitter.split_documents(documents)
                
                embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                st.session_state.db = Chroma.from_documents(chunks, embedding_model)
                
                end_time = time.time()
                processing_duration = round(end_time - start_time, 2)
                
                st.session_state.metadata = {
                    "filename": uploaded_file.name,
                    "chunks": len(chunks),
                    "pages": len(documents),
                    "tokens": estimated_tokens,
                    "time": processing_duration
                }
                st.session_state.file_processed = True

            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            st.rerun()

        st.markdown("### 📊 Document Core Analytics Row")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("📄 Total Pages", f"{st.session_state.metadata.get('pages', 0)} pages")
        m_col2.metric("🪙 Est. Tokens", f"{st.session_state.metadata.get('tokens', 0)}")
        m_col3.metric("⏱️ Parsing Time", f"{st.session_state.metadata.get('time', 0)}s")
        m_col4.metric("🧬 Model Vectors", "all-MiniLM")
        
        st.write("---")

        # --- Interactive Professional Chat Interface Panels ---
        st.markdown("### 💬 Conversational Stream Memory")
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg["role"] == "assistant" and "sources" in msg:
                        with st.expander("🔍 Review Document Citations (Source Context Blocks)"):
                            for idx, src in enumerate(msg["sources"]):
                                st.markdown(f"<div class='citation-header'>[Source Context Block {idx+1}] Metadata Match:</div>", unsafe_allow_html=True)
                                st.caption(src)

        user_query = st.chat_input("Ask an analytical question about your document...")

        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.rerun()

    else:
        st.info("💡 Please choose and drop a document above to launch the secure AI interface session.")

# --- Tab/Preview Panel Control Logic ---
with col_preview:
    if st.session_state.file_processed:
        st.markdown("### 📑 Extracted Document Profile Credentials")
        
        st.markdown(f"""
        | Parameter Attribute | Extracted Identity Value |
        | :--- | :--- |
        | **Active Target File** | `{st.session_state.metadata.get('filename')}` |
        | **Document Pipeline Path** | `Vector Engine Ingested` |
        | **Project Topic Key** | `AI & MODERN TECH ECOSYSTEM ANALYZER` |
        | **Primary Author Entity**| `SARAN BABU S & TEAM` |
        | **Institution Matrix** | `Muthayammal Engineering College` |
        """)
        
        with st.expander("📄 View Core Cover Text Page Summary Stream"):
            st.markdown("""
            <div class='metric-card' style='max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.85rem; color: #C2C6D1; white-space: pre-wrap;'>
            """ + st.session_state.doc_preview + """
            </div>
            """, unsafe_allow_html=True)

# --- Background Processing Logic triggered after rerun state ---
if st.session_state.file_processed and len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
    user_query = st.session_state.chat_history[-1]["content"]
    
    with col_main:
        with st.spinner("🔍 Reviewing internal vectors..."):
            docs = st.session_state.db.similarity_search(user_query, k=5)
            context = "\n".join([doc.page_content for doc in docs])
            
            source_citations = [doc.page_content for doc in docs[:2]] 

            history_text = ""
            for msg in st.session_state.chat_history[-3:-1]:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_text += f"{role}: {msg['content']}\n"

            prompt = f"""You are an elite academic document analyzer. Your goal is to answer the user question with absolute factual precision based on the provided data components.

Core Document Initial Info:
{st.session_state.doc_preview}

Dynamic Context Blocks:
{context}

Conversation History:
{history_text}

User Question: {user_query}
Instructions: Check BOTH data arrays to output a direct precise summary. Do not reference outside world rules:"""

            try:
                model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
                response = model.generate_content(prompt)
                answer = response.text
                
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": source_citations
                })
                st.rerun()
                
            except Exception as e:
                if "429" in str(e) or "Quota exceeded" in str(e):
                    st.error("⚠️ API Request limit hit. Please wait a moment.")
                else:
                    st.error(f"❌ Error encountered: {str(e)}")