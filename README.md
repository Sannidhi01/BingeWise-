# BingeWise - Intelligent movie search and recommendation platform
BingeWise is a Flask-based web application that allows users to search for any movie/series/show, view its complete details using the OMDB API, and receive ML-powered movie recommendations using a DBSCAN clustering model.

It combines Web Development + Machine Learning + API Integration into one practical project.

🚀 Features

🔍 Movie Search

Search any movie/series by title

Fetches real-time details from OMDB API, including:
Title, Year
Genre
Actors
Plot
IMDb Rating
Poster
Trailer link (YouTube search)

🤖 ML-Based Recommendations

A DBSCAN clustering model groups movies based on similarity

When a user searches a movie, similar movies from the same cluster are recommended

Recommendations are displayed with:
Poster
Genre
Plot
Rating
Actors

🖥️ Frontend

Built using HTML, CSS, JavaScript

Uses async API calls to interact with Flask backend

Clean, responsive UI with movie cards

🧩 Backend (Flask)

Exposes endpoints for:

"/" → renders UI

"/recommend?movie=<title>" → returns recommended movies as JSON

Handles CORS

Integrates with ML model for cluster-based recommendations

🧠 Machine Learning

Resultant dataset from ML model stored as clustered_movies.csv

Movies are clustered using DBSCAN for natural similarity grouping

Backend picks movies with the same cluster ID as the searched title.

🏗️ Tech Stack

Frontend : 
HTML
CSS
JavaScript
Fetch API (async/await)

Backend :
Python
Flask
Flask-CORS
Pandas
Scikit-learn
NumPy

APIs :
OMDB API (for fetching real-time movie data)
