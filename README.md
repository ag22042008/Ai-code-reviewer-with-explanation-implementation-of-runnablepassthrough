# Ai-code-reviewer-with-explanation-implementation-of-runnablepassthrough
Same café-ticket concept as before, this time as a Streamlit app. The pipeline in app.py (model, prompts, chains) is untouched from your original script — it's cached with @st.cache_resource so it's built once per session, and called with the same pipeline.invoke({"topic": ...}).
