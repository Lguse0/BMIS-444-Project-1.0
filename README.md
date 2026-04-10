# BMIS-444-Project-1.0

🎬 Film Tracker App (Letterboxd-Inspired)
📌 Project Title & Description
Project Title: Film Tracker (Letterboxd-Inspired)
Description:
The Film Tracker is a web application that allows users to log, rate, and track movies they have watched or want to watch. Users can search for films, add ratings and written reviews, and maintain a personal watchlist. The system also includes upcoming films through a “Coming Soon” section so users can explore and plan future viewing.
The purpose of this system is to create a centralized, user-friendly platform for organizing film viewing history and preferences. It simulates a real-world movie tracking application similar to Letterboxd by supporting user accounts, film metadata, ratings, and personalized watchlists.

Your ERD — embedded as an image (![ERD](erd.png) or similar).

<img width="316" height="346" alt="erd" src="https://github.com/user-attachments/assets/9d44d00b-39d1-4f78-933d-8d01312c8dd9" />

Table descriptions

🗃️ Table Descriptions
👤 users
Stores user account information.
id: Unique identifier for each user (Primary Key)
username: Unique username used for login
email: User’s email address (unique)
password_hash: Encrypted password for authentication
created_at: Timestamp when the user account was created

🎬 directors
Stores film director information.
id: Primary key
first_name: Director’s first name
last_name: Director’s last name
birth_date: Director’s date of birth
nationality: Country of origin

🎞️ films
Stores movie details.
id: Primary key
title: Film title
release_date: Official release date
genre: Film genre
runtime_minutes: Duration of the film in minutes
description: Short summary of the film
director_id: Foreign key linking to directors

⭐ ratings
Stores user ratings and reviews for films.
id: Primary key
user_id: Links rating to a user
film_id: Links rating to a film
rating_score: Numeric rating from 0.0 to 5.0
review_text: Optional written review
watched_date: Date the user watched the film
created_at: Timestamp of rating creation
UNIQUE(user_id, film_id): Prevents duplicate ratings per film per user

📋 watchlist
Stores films users want to watch.
id: Primary key
user_id: Links entry to a user
film_id: Links entry to a film
added_date: Timestamp when added to watchlist
priority_level: Importance level (1–5)
UNIQUE(user_id, film_id): Prevents duplicates in watchlist

🎥 coming_soon
Stores upcoming film releases.
film_id: Primary key and foreign key to films
release_date: Future release date
trailer_url: Link to trailer
platform: Where the film will be released (Netflix, theaters, etc.)
notes: Additional information about the release
created_at: Timestamp when entry was added

How to run locally — what someone would need to do to run your app on their own machine (install dependencies, set up secrets, etc.).
To run this project on your own machine:

1. Install dependencies
Make sure you have Python installed, then run:
pip install streamlit psycopg2-binary pandas

2. Set up PostgreSQL database
Create a PostgreSQL database
Run your SQL schema to create tables
Make sure all relationships and constraints are included

3. Add Streamlit secrets
Create a file:
.streamlit/secrets.toml
Add your database credentials:
[connections.postgresql]
host = "your-host"
dbname = "your-db-name"
user = "your-username"
password = "your-password"
port = 5432

4. Run the app
streamlit run app.py


Live app URL - https://bmis-444-project-1-pzmyxf3n46qwrrpxff7u7k.streamlit.app 
