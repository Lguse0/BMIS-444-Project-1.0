import streamlit as st
import sqlite3

st.set_page_config(page_title="Browse Films", page_icon="🔍")

def get_connection():
    return sqlite3.connect("film_tracker.db")

st.title("🔍 Browse / Search Films")

search_title = st.text_input("Search Film Title")

conn = get_connection()
cur = conn.cursor()

# Get genres for filter dropdown
cur.execute("SELECT DISTINCT genre FROM films WHERE genre IS NOT NULL ORDER BY genre;")
genres = [g[0] for g in cur.fetchall()]
genre_filter = st.selectbox("Filter by Genre", ["All"] + genres)

# Get directors for filter dropdown
cur.execute("SELECT id, first_name || ' ' || last_name FROM directors ORDER BY last_name;")
directors = cur.fetchall()
director_dict = {d[1]: d[0] for d in directors}
director_filter = st.selectbox("Filter by Director", ["All"] + list(director_dict.keys()))

release_year = st.text_input("Filter by Release Year (ex: 2022)")

query = """
    SELECT f.id, f.title, f.genre, f.release_date,
           d.first_name || ' ' || d.last_name AS director
    FROM films f
    LEFT JOIN directors d ON f.director_id = d.id
    WHERE 1=1
"""
params = []

if search_title:
    query += " AND f.title LIKE ?"
    params.append(f"%{search_title}%")

if genre_filter != "All":
    query += " AND f.genre = ?"
    params.append(genre_filter)

if director_filter != "All":
    query += " AND f.director_id = ?"
    params.append(director_dict[director_filter])

if release_year:
    query += " AND strftime('%Y', f.release_date) = ?"
    params.append(release_year)

query += " ORDER BY f.title;"

cur.execute(query, params)
films = cur.fetchall()

conn.close()

st.markdown("---")
st.subheader("🎬 Film Results")

if films:
    for film in films:
        film_id, title, genre, release_date, director = film

        st.write(f"**{title}** ({release_date if release_date else 'Unknown'})")
        st.write(f"Genre: {genre if genre else 'N/A'} | Director: {director if director else 'N/A'}")

        if st.button(f"View Details: {title}", key=f"details_{film_id}"):
            st.session_state["selected_film_id"] = film_id
            st.switch_page("pages/2_Film_Details.py")

        st.markdown("---")
else:
    st.info("No films found matching your search.")