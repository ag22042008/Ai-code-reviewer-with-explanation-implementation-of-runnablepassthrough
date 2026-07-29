# Order a Java — Streamlit edition

Same café-ticket concept as before, this time as a Streamlit app. The
pipeline in `app.py` (model, prompts, chains) is untouched from your
original script — it's cached with `@st.cache_resource` so it's built
once per session, and called with the same `pipeline.invoke({"topic": ...})`.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env   # then put your real key in .env
streamlit run app.py
```

It'll open at http://localhost:8501

## What you get

- A "menu card" on the left to describe the Java code you want
- A real-time "brewing" status (grinding → pulling the shot → steaming →
  plating) while the two Mistral calls run in the background
- The result on the right as an order ticket with two tabs:
  **Ticket** (the generated code, with Streamlit's built-in copy button)
  and **Barista's Notes** (the plain-words explanation)
- A dark espresso / warm paper theme set both via `.streamlit/config.toml`
  and custom CSS injected in `app.py`
