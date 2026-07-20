import streamlit as st
import pandas as pd
import sqlite3
import datetime
from pathlib import Path
from classifier import classify

st.set_page_config(
    page_title="GDPR Request Classifier",
    page_icon="🔐",
    layout="wide"
)

DB_PATH = "requests.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_text TEXT,
            request_type TEXT,
            gdpr_article TEXT,
            action TEXT,
            priority TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_to_db(input_text, result):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO classifications
        (timestamp, input_text, request_type, gdpr_article, action, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.utcnow().isoformat(),
        input_text,
        result["request_type"],
        result["gdpr_article"],
        result["action"],
        result["priority"]
    ))
    conn.commit()
    conn.close()


def get_history(limit=20):
    if not Path(DB_PATH).exists():
        return pd.DataFrame(columns=[
            "timestamp", "input_text", "request_type",
            "gdpr_article", "action", "priority"
        ])

    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT timestamp, input_text, request_type, gdpr_article, action, priority
        FROM classifications
        ORDER BY id DESC
        LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df


init_db()

st.title("🔐 GDPR Request Classifier")
st.caption("Classify data subject requests and map them to the relevant GDPR article.")

tab1, tab2 = st.tabs(["Classifier", "Recent history"])

with tab1:
    example_prompts = [
        "I want a copy of all the personal data you hold about me.",
        "Please delete all my personal data from your systems.",
        "Your company leaked my information in a data breach.",
        "My address is wrong and needs to be updated.",
        "I want to transfer my data to another provider."
    ]

    selected_example = st.selectbox(
        "Try an example request",
        [""] + example_prompts
    )

    default_text = selected_example if selected_example else ""

    user_input = st.text_area(
        "Enter the request text",
        value=default_text,
        height=180,
        placeholder="Example: I want to know what personal data you hold about me."
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        run_button = st.button("Classify", type="primary", use_container_width=True)

    if run_button:
        cleaned = user_input.strip()

        if not cleaned:
            st.error("Request text cannot be empty.")
        elif len(cleaned) < 5:
            st.error("Request text is too short to classify.")
        elif len(cleaned) > 5000:
            st.error("Request text exceeds the 5000 character limit.")
        else:
            result = classify(cleaned)
            log_to_db(cleaned, result)

            st.success("Classification complete.")

            c1, c2 = st.columns(2)
            c1.metric("Request Type", result["request_type"])
            c2.metric("Priority", result["priority"])

            st.markdown("### GDPR Mapping")
            st.write(f"**Article:** {result['gdpr_article']}")
            st.write(f"**Recommended action:** {result['action']}")

            with st.expander("Structured output"):
                st.json(result)

with tab2:
    st.markdown("### Last 20 classifications")
    history_df = get_history(20)

    if history_df.empty:
        st.info("No classifications logged yet.")
    else:
        st.dataframe(history_df, use_container_width=True)

        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download history as CSV",
            data=csv,
            file_name="gdpr_classifier_history.csv",
            mime="text/csv"
        )

st.markdown("---")
st.caption("Note: SQLite storage on Streamlit Cloud is temporary and may reset after app restarts.")