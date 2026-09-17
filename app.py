import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Research System", page_icon="🔎", layout="wide")

st.title("🔎 Multi-Agent Research System")
st.caption("Search Agent → Research Agent → Writer Agent → Critic Agent")

# --- Input ---
with st.form("topic_form"):
    topic = st.text_input(
        "Enter a topic to research",
        placeholder="e.g. impact of water pollution in Mumbai 2026",
    )
    submitted = st.form_submit_button("Run Research Pipeline", type="primary")

# --- Run pipeline ---
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
        st.stop()

    with st.spinner("Running the 4-agent pipeline... this can take a minute or two."):
        try:
            state = run_research_pipeline(topic)
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            st.stop()

    st.success("Done!")

    # --- Final report front and center ---
    st.header("📄 Final Research Report")
    st.markdown(state.get("report", "_No report generated._"))

    st.divider()

    # --- Critic feedback ---
    st.header("🧐 Critic Feedback")
    st.markdown(state.get("feedback", "_No feedback generated._"))

    st.divider()

    # --- Raw intermediate steps, collapsed by default ---
    st.subheader("Intermediate Steps")

    with st.expander("Step 1 · Search Agent — raw search results"):
        st.text(state.get("search_results", "No data."))

    with st.expander("Step 2 · Research Agent — scraped content"):
        st.text(state.get("scraped_content", "No data."))

    # --- Download the report ---
    st.download_button(
        label="⬇️ Download report as Markdown",
        data=state.get("report", ""),
        file_name=f"{topic.strip().replace(' ', '_')}_report.md",
        mime="text/markdown",
    )

else:
    st.info("Enter a topic above and click **Run Research Pipeline** to get started.")