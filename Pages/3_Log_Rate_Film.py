import streamlit as st
import sqlite3

st.set_page_config(page_title="Log / Rate Film", page_icon="⭐")

def get_connection():
    return sqlite3.connect("film_tracker.db")

USER_ID = 1

st.title("⭐ Log / Rate a Film")

conn = get_connection()
cur = conn.cursor()

# Film dropdown
cur.execute("SELECT id, title FROM films ORDER BY title;")
films = cur.fetchall()

film_options = {f"{f[1]}": f[0] for f in films}

default_index = 0
if "rate_film_id" in st.session_state:
    selected_id = st.session_state["rate_film_id"]
    for i, (name, fid) in enumerate(film_options.items()):
        if fid == selected_id:
            default_index = i
            break

film_name = st.selectbox("Choose a Film", list(film_options.keys()), index=default_index)
film_id = film_options[film_name]

# Check if already rated
cur.execute("""
    SELECT id, rating_score, review_text, watched_date
    FROM ratings
    WHERE user_id = ? AND film_id = ?;
""", (USER_ID, film_id))
existing = cur.fetchone()

existing_rating_id = None
rating_default = 0.0
review_default = ""
watched_default = None

if existing:
    existing_rating_id = existing[0]
    rating_default = existing[1]
    review_default = existing[2] if existing[2] else ""
    watched_default = existing[3]

st.markdown("---")

with st.form("rate_form"):
    rating_score = st.number_input("Rating (0.0 - 5.0)", min_value=0.0, max_value=5.0, step=0.1, value=float(rating_default))
    review_text = st.text_area("Review", value=review_default)
    watched_date = st.date_input("Watched Date")

    submitted = st.form_submit_button("Save Rating")

    if submitted:
        try:
            if existing_rating_id:
                cur.execute("""
                    UPDATE ratings
                    SET rating_score = ?, review_text = ?, watched_date = ?
                    WHERE id = ?;
                """, (rating_score, review_text, watched_date, existing_rating_id))
                conn.commit()
                st.success("✅ Rating updated successfully!")
            else:
                cur.execute("""
                    INSERT INTO ratings (user_id, film_id, rating_score, review_text, watched_date)
                    VALUES (?, ?, ?, ?, ?);
                """, (USER_ID, film_id, rating_score, review_text, watched_date))
                conn.commit()
                st.success("✅ Rating saved successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

if existing_rating_id:
    if st.button("🗑️ Delete Rating"):
        cur.execute("DELETE FROM ratings WHERE id = ?;", (existing_rating_id,))
        conn.commit()
        st.success("Rating deleted.")

conn.close()