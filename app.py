"""
Order a Java — Streamlit edition.

The pipeline below (model, prompts, chains) is the exact same LangChain
logic from the original script. Everything else on this page is UI.
"""

import time
import concurrent.futures

import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
for _key in ("MISTRAL_API_KEY"):
    if not os.getenv(_key):
        try:
            if _key in st.secrets:
                os.environ[_key] = st.secrets[_key]
        except Exception:
            pass
# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Order a Java",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Original pipeline — unchanged
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def build_pipeline():
    model = ChatMistralAI(model="mistral-small-2506")
    parser = StrOutputParser()

    code_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a ai code generator in java language and short code "),
        ("user", "{topic}"),
    ])
    explain_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a ai code generator in java language and short code "),
        ("user", "Explain the code generated in simple words step by step:\n{code}"),
    ])

    seq1 = code_prompt | model | parser
    seq2 = RunnableParallel({
        "code": RunnablePassthrough(),
        "explanation": explain_prompt | model | parser,
    })
    return seq1 | seq2


pipeline = build_pipeline()

# ---------------------------------------------------------------------------
# Theme (café / order-ticket aesthetic)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
      :root {
        --espresso: #2b1b12;
        --espresso-deep: #1c110a;
        --paper: #f5ead8;
        --caramel: #c77d34;
        --rust: #a13d2b;
        --muted: #a4917d;
        --muted-dark: #6f5a47;
      }

      .stApp {
        background: var(--espresso);
        color: #f5ead8;
      }

      html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

      /* header */
      .java-header { display:flex; align-items:flex-end; gap:0.8rem; margin-bottom: 0.25rem; }
      .java-header .cup { font-size: 2.1rem; }
      .java-header h1 {
        font-family: 'Fraunces', serif; font-weight: 700;
        font-size: 2rem; margin: 0; color: #f5ead8;
      }
      .java-tagline { color: var(--muted); font-size: 0.9rem; margin: 0.15rem 0 1.5rem 0; }

      /* menu card */
      .menu-card {
        background: var(--paper); color: var(--espresso);
        border-radius: 8px; padding: 1.4rem 1.5rem; border: 1px dashed rgba(43,27,18,0.2);
      }
      .menu-card .eyebrow {
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
        letter-spacing: 0.14em; text-transform: uppercase; color: var(--rust);
      }
      .menu-card h3 { font-family: 'Fraunces', serif; margin: 0.2rem 0 1rem 0; font-size: 1.25rem; }

      /* textarea */
      .stTextArea textarea {
        background: #fffaf0 !important; color: var(--espresso) !important;
        border: 1.5px solid rgba(43,27,18,0.2) !important; border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
      }

      /* button */
      .stButton>button {
        background: var(--caramel); color: #fffaf0; border: none; border-radius: 4px;
        font-weight: 600; padding: 0.55rem 1.4rem; width: 100%;
        transition: background 0.15s ease;
      }
      .stButton>button:hover { background: var(--rust); color: #fffaf0; }

      /* tabs -> look like ticket tabs */
      .stTabs [data-baseweb="tab-list"] { gap: 0.35rem; }
      .stTabs [data-baseweb="tab"] {
        background: rgba(245,234,216,0.06); color: var(--muted);
        border-radius: 6px 6px 0 0; font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem; letter-spacing: 0.04em; text-transform: uppercase;
      }
      .stTabs [aria-selected="true"] { background: var(--paper) !important; color: var(--espresso) !important; }

      /* ticket body */
      .ticket-panel {
        background: var(--paper); color: var(--espresso); border-radius: 0 6px 6px 6px;
        padding: 1.4rem 1.5rem 1.6rem; position: relative; min-height: 380px;
      }
      .ticket-panel::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 10px;
        background-image: radial-gradient(circle at 10px 0, var(--espresso) 5px, transparent 5.5px);
        background-size: 20px 10px; background-repeat: repeat-x; border-radius: 0 6px 0 0;
      }
      .ticket-head {
        display:flex; justify-content:space-between; font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem; letter-spacing: 0.08em; color: var(--muted-dark);
        border-bottom: 1px dashed rgba(43,27,18,0.25); padding-bottom: 0.55rem; margin-bottom: 0.9rem;
      }
      .stamp {
        display:inline-block; font-family:'Fraunces', serif; font-weight:700; font-size:0.95rem;
        letter-spacing:0.1em; color: var(--rust); border: 3px solid var(--rust); border-radius: 6px;
        padding: 0.15rem 0.55rem; transform: rotate(-9deg); opacity: 0.8; margin-left: 0.6rem;
      }

      .empty-state { text-align:center; color: var(--muted); padding: 3rem 1rem; }
      .empty-state .icon { font-size: 2rem; opacity: 0.5; }

      code, pre { font-family: 'JetBrains Mono', monospace !important; }

      .java-footer { text-align:center; color: var(--muted-dark); font-size: 0.78rem; margin-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="java-header"><span class="cup">☕</span><h1>Order a Java</h1></div>
    <p class="java-tagline">Describe it. We brew it. Java, on the house. &nbsp;·&nbsp;
    house pipeline: LangChain × Mistral</p>
    """,
    unsafe_allow_html=True,
)

if "order" not in st.session_state:
    st.session_state.order = None  # holds {"code": ..., "explanation": ...}

col1, col2 = st.columns([1, 1.6], gap="large")

# ---------------------------------------------------------------------------
# Left column — the order form
# ---------------------------------------------------------------------------
with col1:
    st.markdown(
        '<div class="menu-card"><span class="eyebrow">the order</span>'
        '<h3>What are we brewing today?</h3>',
        unsafe_allow_html=True,
    )
    topic = st.text_area(
        "Describe the Java code you want",
        placeholder="e.g. Write code for generating all distinct palindrome strings in a string",
        height=140,
        label_visibility="collapsed",
    )
    brew_clicked = st.button("Brew it ☕", use_container_width=True)
    st.caption("Every order runs the same house recipe: generate the code, then explain it in plain words.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Handle the order
# ---------------------------------------------------------------------------
BREWING_MESSAGES = [
    "Grinding the syntax…",
    "Pulling the shot…",
    "Steaming the semantics…",
    "Plating the ticket…",
]

if brew_clicked:
    if not topic or not topic.strip():
        st.warning("Tell the barista what you'd like brewed.")
    else:
        status_ph = st.empty()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(pipeline.invoke, {"topic": topic})
            i = 0
            while not future.done():
                status_ph.info(f"☕ {BREWING_MESSAGES[i % len(BREWING_MESSAGES)]}")
                i += 1
                time.sleep(1.1)
            try:
                result = future.result()
                st.session_state.order = {
                    "code": result["code"],
                    "explanation": result["explanation"],
                    "time": time.strftime("%H:%M"),
                }
            except Exception as exc:
                st.session_state.order = None
                status_ph.error(f"The machine jammed: {exc}")
            else:
                status_ph.empty()

# ---------------------------------------------------------------------------
# Right column — the ticket
# ---------------------------------------------------------------------------
with col2:
    order = st.session_state.order

    if not order:
        st.markdown(
            '<div class="ticket-panel"><div class="empty-state">'
            '<div class="icon">☕</div><p><strong>No order yet.</strong></p>'
            '<p>Place an order on the left to print your first ticket.</p>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    else:
        tab_code, tab_explain = st.tabs(["Ticket", "Barista's Notes"])

        with tab_code:
            st.markdown(
                f'<div class="ticket-panel"><div class="ticket-head">'
                f'<span>ORDER TICKET</span><span>{order["time"]} '
                f'<span class="stamp">COMPILED</span></span></div>',
                unsafe_allow_html=True,
            )
            st.code(order["code"], language="java")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_explain:
            st.markdown(
                '<div class="ticket-panel"><div class="ticket-head">'
                '<span>BARISTA\'S NOTES</span><span>step by step</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(order["explanation"])
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<p class="java-footer">Powered by a LangChain pipeline calling Mistral '
    '(<code>mistral-small-2506</code>) — the recipe never changes, only what you order.</p>',
    unsafe_allow_html=True,
)
