# HackChallengeBackend
Repo for the backend of our hack challenge

This backend supports a simple set of APIs for an app where users could post reviews to restaurants in the Ithaca area. 

Routes:
GET /locations/: In our App Ithaca is divided into 6 locations or regions. This route returns the id and name of all locations.\
POST /restaurants/: This route creates a review for a restaurant in the database. \
GET /restaurants/i/ : This route fetches all reviews of restaurants under a certain region with id i.\
GET /restaurant/i/: Fetches a specific restaurant review with id i.\
DELETE /restaurant/i/: Deletes a specific review. This is initially intended to be used with authentication or a "downvote" mechanism, but the those features can't be implemented due to time constraints of frontend teammates. 

Database Models:
Two tables, one representing the locations and one representing the reviews, is implemented as sqlite3 tables. 

Relationships:
A FOREIGN KEY relationship in the reviews table referencing the id of a location in the locations table. 
