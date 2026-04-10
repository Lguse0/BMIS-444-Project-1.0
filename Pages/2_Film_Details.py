import streamlit as st
import sqlite3

st.set_page_config(page_title="Film Details", page_icon="🎞️")

def get_connection():
    return sqlite3.connect("film_tracker.db")

USER_ID = 1

st.title("🎞️ Film Details")

if "selected_film_id" not in st.session_state:
    st.warning("No film selected. Go back to Browse Films.")
    st.stop()

film_id = st.session_state["selected_film_id"]

conn = get_connection()
cur = conn.cursor()

# Film details
cur.execute("""
    SELECT f.title, f.genre, f.runtime_minutes, f.description, f.release_date,
           d.first_name || ' ' || d.last_name
    FROM films f
    LEFT JOIN directors d ON f.director_id = d.id
    WHERE f.id = ?;
""", (film_id,))
film = cur.fetchone()

if not film:
    st.error("Film not found.")
    conn.close()
    st.stop()

title, genre, runtime, description, release_date, director = film

st.subheader(title)
st.write(f"**Genre:** {genre if genre else 'N/A'}")
st.write(f"**Runtime:** {runtime if runtime else 'N/A'} minutes")
st.write(f"**Director:** {director if director else 'N/A'}")
st.write(f"**Release Date:** {release_date if release_date else 'N/A'}")
st.write(f"**Description:** {description if description else 'N/A'}")

# Average rating
cur.execute("SELECT ROUND(AVG(rating_score), 2) FROM ratings WHERE film_id = ?;", (film_id,))
avg_rating = cur.fetchone()[0]

st.markdown("---")
st.write(f"⭐ **Average Rating:** {avg_rating if avg_rating else 'No ratings yet'}")

# User rating
cur.execute("""
    SELECT rating_score, review_text, watched_date
    FROM ratings
    WHERE user_id = ? AND film_id = ?;
""", (USER_ID, film_id))
user_rating = cur.fetchone()

if user_rating:
    st.markdown("---")
    st.subheader("👤 Your Rating")
    st.write(f"⭐ Rating: {user_rating[0]}")
    st.write(f"📅 Watched Date: {user_rating[2]}")
    st.write(f"📝 Review: {user_rating[1] if user_rating[1] else ''}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("📌 Add to Watchlist"):
        try:
            cur.execute("""
                INSERT INTO watchlist (user_id, film_id)
                VALUES (?, ?);
            """, (USER_ID, film_id))
            conn.commit()
            st.success("Added to watchlist!")
        except sqlite3.IntegrityError:
            st.warning("This film is already in your watchlist.")

with col2:
    if st.button("⭐ Rate / Log This Film"):
        st.session_state["rate_film_id"] = film_id
        st.switch_page("pages/3_Log_Rate_Film.py")

conn.close()