# ☕ Order a Java — AI Code Generator & Explainer (Streamlit Edition)

An interactive, café-themed Streamlit application that generates concise Java code for any problem statement and provides a step-by-step explanation. Built using **LangChain (`RunnablePassthrough`, `RunnableParallel`)** and **Google Gemini (`langchain-google-genai`)**.

---

## 🏗️ Architecture & Pipeline Flow

The underlying LCEL (LangChain Expression Language) pipeline processes the topic in sequential and parallel steps:

```mermaid
graph TD
    A[User Input: Topic] --> B[code_prompt]
    B --> C[ChatGoogleGenerativeAI: gemini-1.5-flash]
    C --> D[StrOutputParser]
    D --> E[Generated Java Code]

    E --> F[RunnableParallel Step]

    subgraph Parallel Execution
        F --> G[RunnablePassthrough: Preserves Raw Code]
        F --> H[explain_prompt]
        H --> I[ChatGoogleGenerativeAI: gemini-1.5-flash]
        I --> J[StrOutputParser: Code Explanation]
    end

    G --> K["Final Output Object: { code, explanation }"]
    J --> K
    K --> L[Streamlit UI Render]
