import streamlit as st
import sqlite3

st.set_page_config(page_title="My Watched Films", page_icon="🎥")

def get_connection():
    return sqlite3.connect("film_tracker.db")

USER_ID = 1

st.title("🎥 My Watched Films")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT r.id, f.title, r.rating_score, r.watched_date, r.review_text
    FROM ratings r
    JOIN films f ON r.film_id = f.id
    WHERE r.user_id = ?
    ORDER BY r.watched_date DESC;
""", (USER_ID,))
rows = cur.fetchall()

conn.close()

if rows:
    for r in rows:
        rating_id, title, score, watched_date, review = r

        st.write(f"🎬 **{title}**")
        st.write(f"⭐ Rating: {score} | 📅 Watched: {watched_date}")
        st.write(f"📝 Review: {review[:100] + '...' if review and len(review) > 100 else (review if review else '')}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Edit", key=f"edit_{rating_id}"):
                st.session_state["rate_film_id"] = None
                st.switch_page("pages/3_Log_Rate_Film.py")

        with col2:
            if st.button("🗑️ Delete", key=f"delete_{rating_id}"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM ratings WHERE id = ?;", (rating_id,))
                conn.commit()
                conn.close()
                st.success("Deleted rating. Refresh page to update.")
        st.markdown("---")
else:
    st.info("You haven't logged any films yet.")