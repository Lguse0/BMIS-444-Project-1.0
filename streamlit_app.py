import streamlit as st
import sqlite3
from datetime import datetime

import sqlite3

def get_connection():
    return sqlite3.connect("film_tracker.db")

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS directors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date DATE,
        nationality TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_date DATE,
        genre TEXT,
        runtime_minutes INTEGER,
        description TEXT,
        director_id INTEGER,
        FOREIGN KEY (director_id) REFERENCES directors(id)
            ON DELETE SET NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        film_id INTEGER NOT NULL,
        rating_score REAL NOT NULL,
        review_text TEXT,
        watched_date DATE DEFAULT (DATE('now')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, film_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE,
        FOREIGN KEY (film_id) REFERENCES films(id)
            ON DELETE CASCADE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        film_id INTEGER NOT NULL,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        priority_level INTEGER DEFAULT 3,
        UNIQUE(user_id, film_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE,
        FOREIGN KEY (film_id) REFERENCES films(id)
            ON DELETE CASCADE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS coming_soon (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        film_id INTEGER NOT NULL,
        release_date DATE NOT NULL,
        trailer_url TEXT,
        platform TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(film_id),
        FOREIGN KEY (film_id) REFERENCES films(id)
            ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

# Run once when app starts
create_tables()

st.set_page_config(page_title="Film Tracker Home", page_icon="🎬")

# -------------------------------
# Database Connection (SQLite)
# -------------------------------
def get_connection():
    return sqlite3.connect("film_tracker.db")

st.title("🎬 Film Tracker Dashboard")
st.write("Welcome! Track your watched films, ratings, watchlist, and upcoming releases.")

st.markdown("---")
st.subheader("📊 Your Stats")

try:
    conn = get_connection()
    cur = conn.cursor()

    # -------------------------------
    # Dashboard Stats
    # -------------------------------

    # Total films watched (ratings table = watched films)
    cur.execute("SELECT COUNT(*) FROM ratings;")
    total_watched = cur.fetchone()[0]

    # Average rating
    cur.execute("SELECT ROUND(AVG(rating_score), 2) FROM ratings;")
    avg_rating = cur.fetchone()[0]
    if avg_rating is None:
        avg_rating = 0

    # Total watchlist films
    cur.execute("SELECT COUNT(*) FROM watchlist;")
    total_watchlist = cur.fetchone()[0]

    # Upcoming films count
    cur.execute("SELECT COUNT(*) FROM coming_soon;")
    upcoming_count = cur.fetchone()[0]

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎥 Films Watched", total_watched)
    col2.metric("⭐ Average Rating", avg_rating)
    col3.metric("📌 Watchlist Films", total_watchlist)
    col4.metric("📅 Upcoming Films", upcoming_count)

    st.markdown("---")
    st.subheader("📝 Recently Rated Films")

    # -------------------------------
    # Recently Rated Films Table
    # -------------------------------
    cur.execute("""
        SELECT f.title, r.rating_score, r.review_text, r.watched_date
        FROM ratings r
        JOIN films f ON r.film_id = f.id
        ORDER BY r.created_at DESC
        LIMIT 10;
    """)
    rows = cur.fetchall()

    if rows:
        st.table([
            {
                "Film": r[0],
                "Rating": r[1],
                "Review": r[2] if r[2] else "",
                "Watched Date": r[3]
            }
            for r in rows
        ])
    else:
        st.info("No films have been rated yet. Start rating movies to see them here!")

    cur.close()
    conn.close()

except Exception as e:
    st.error(f"Database connection error: {e}")
