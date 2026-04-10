import streamlit as st
import sqlite3

st.set_page_config(page_title="Coming Soon", page_icon="📅")

def get_connection():
    return sqlite3.connect("film_tracker.db")

USER_ID = 1

st.title("📅 Coming Soon")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT cs.id, f.id, f.title, cs.release_date, cs.trailer_url, cs.platform
    FROM coming_soon cs
    JOIN films f ON cs.film_id = f.id
    ORDER BY cs.release_date ASC;
""")
upcoming = cur.fetchall()

conn.close()

if upcoming:
    for u in upcoming:
        coming_id, film_id, title, release_date, trailer_url, platform = u

        st.write(f"🎬 **{title}**")
        st.write(f"📅 Release Date: {release_date}")
        st.write(f"📺 Platform: {platform if platform else 'N/A'}")

        if trailer_url:
            st.markdown(f"[▶ Watch Trailer]({trailer_url})")

        if st.button("📌 Add to Watchlist", key=f"watchlist_{coming_id}"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO watchlist (user_id, film_id)
                    VALUES (?, ?);
                """, (USER_ID, film_id))
                conn.commit()
                conn.close()
                st.success("Added to watchlist!")
            except sqlite3.IntegrityError:
                st.warning("Already in watchlist.")

        st.markdown("---")
else:
    st.info("No upcoming films listed.")