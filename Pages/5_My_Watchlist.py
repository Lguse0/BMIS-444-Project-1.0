import streamlit as st
import sqlite3

st.set_page_config(page_title="My Watchlist", page_icon="📌")

def get_connection():
    return sqlite3.connect("film_tracker.db")

USER_ID = 1

st.title("📌 My Watchlist")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT w.id, f.id, f.title, f.release_date, w.priority_level,
           d.first_name || ' ' || d.last_name
    FROM watchlist w
    JOIN films f ON w.film_id = f.id
    LEFT JOIN directors d ON f.director_id = d.id
    WHERE w.user_id = ?
    ORDER BY w.priority_level ASC, w.added_date DESC;
""", (USER_ID,))
watchlist = cur.fetchall()

conn.close()

if watchlist:
    for w in watchlist:
        watchlist_id, film_id, title, release_date, priority, director = w

        st.write(f"🎬 **{title}** ({release_date if release_date else 'Unknown'})")
        st.write(f"Director: {director if director else 'N/A'} | Priority: {priority}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("❌ Remove", key=f"remove_{watchlist_id}"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM watchlist WHERE id = ?;", (watchlist_id,))
                conn.commit()
                conn.close()
                st.success("Removed from watchlist. Refresh page to update.")

        with col2:
            if st.button("✅ Mark as Watched", key=f"watched_{watchlist_id}"):
                st.session_state["rate_film_id"] = film_id
                st.switch_page("pages/3_Log_Rate_Film.py")

        st.markdown("---")
else:
    st.info("Your watchlist is empty.")