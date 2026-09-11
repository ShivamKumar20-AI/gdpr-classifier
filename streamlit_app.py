import streamlit as st
import pandas as pd
import sqlite3
import datetime
from pathlib import Path
from classifier import classify
from security import MIN_INPUT_LEN, MAX_INPUT_LEN
from security import hash_input, mask_sensitive_text

import time

MAX_REQUESTS_PER_MINUTE = 5

if "request_timestamps" not in st.session_state:
    st.session_state.request_timestamps = []


def check_rate_limit() -> bool:
    now = time.time()
    # Keep only timestamps from the last 60 seconds
    st.session_state.request_timestamps = [
        ts for ts in st.session_state.request_timestamps if now - ts < 60
    ]
    if len(st.session_state.request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        return False
    st.session_state.request_timestamps.append(now)
    return True


st.set_page_config(
    page_title="GDPR Request Classifier",
    page_icon="🔐",
    layout="wide"
)


DB_PATH = Path("requests.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_hash TEXT,
            input_preview TEXT,
            request_type TEXT,
            gdpr_article TEXT,
            action TEXT,
            priority TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_to_db(input_text, result):
    input_hash = hash_input(input_text)
    input_preview = mask_sensitive_text(input_text)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO classifications
        (timestamp, input_hash, input_preview, request_type, gdpr_article, action, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.utcnow().isoformat(),
        input_hash,
        input_preview,
        result.get("request_type", "Unknown"),
        result.get("gdpr_article", "Unknown"),
        result.get("action", "No action available"),
        result.get("priority", "Medium")
    ))
    conn.commit()
    conn.close()


def get_history(limit=20):
    if not DB_PATH.exists():
        return pd.DataFrame(columns=[
            "timestamp",
            "input_preview",
            "input_hash",
            "request_type",
            "gdpr_article",
            "action",
            "priority"
        ])

    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT timestamp, input_preview, input_hash, request_type, gdpr_article, action, priority
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
        elif not check_rate_limit():
            st.error("Too many requests. Please wait a minute before trying again.")
        elif len(cleaned) < MIN_INPUT_LEN:
            st.error(f"Request text is too short to classify (minimum {MIN_INPUT_LEN} characters).")
        elif len(cleaned) > MAX_INPUT_LEN:
            st.error(f"Request text exceeds the {MAX_INPUT_LEN} character limit.")
        else:
            try:
                result = classify(cleaned)
                log_to_db(cleaned, result)

                request_type = result.get("request_type", "Unknown")

                if request_type == "Invalid Input":
                    st.error(result.get("action", "The request text could not be classified."))
                else:
                    st.success("Classification complete.")

                # st.metric truncates long values with an ellipsis, so the request
                # type is rendered as text instead.
                c1, c2 = st.columns(2)
                c1.markdown("**Request Type**")
                c1.markdown(f"### {request_type}")
                c2.markdown("**Priority**")
                c2.markdown(f"### {result.get('priority', 'Unknown')}")

                if result.get("also_detected"):
                    st.warning(
                        f"This request also mentions: {result['also_detected']}. "
                        "It has been classified under the most urgent category — "
                        "handle the other points as well."
                    )

                st.markdown("### GDPR Mapping")
                st.write(f"**Article:** {result.get('gdpr_article', 'Unknown')}")
                st.write(f"**Recommended action:** {result.get('action', 'No action available')}")

                with st.expander("Structured output"):
                    st.json(result)

            except Exception as e:
                st.error(f"An error occurred during classification: {e}")


with tab2:
    st.subheader("Recent classifications")

    history_df = get_history()

    if history_df.empty:
        st.info("No classifications logged yet.")
    else:
        st.dataframe(history_df, use_container_width=True)

        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download history as CSV",
            data=csv,
            file_name="gdpr_classification_history.csv",
            mime="text/csv"
        )