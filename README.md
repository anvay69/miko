# Miko

#### Video Demo: https://www.youtube.com/watch?v=CEWQ30UQedU

#### Description:
My project is a mental math game site. I've used Flask and SQLite3 to implement the backend of the web app, while the front end is built with HTML, CSS, JavaScript, and Bootstrap. 

Users can create an account or play without registering. If you choose to create an account, your score will be stored, and you'll appear on the leaderboards! The database consists of three tables: users, scores, and leaderboard. The users table stores user information, while the scores table records individual scores for each user based on their performance in the game. The leaderboard table maintains the highest scores for each difficulty level for every user, allowing players to compete against one another and strive for the top spots.

To enhance security, I use CSRF token verification to ensure that requests sent to the submit route are valid and originate from the application. When a GET request is made to index.html, a new CSRF token is generated. This token is then used for submitting scores, ensuring that each request is authenticated and protected against cross-site request forgery attacks.

Additionally, I hash passwords before storing them in the database, providing an extra layer of security for user accounts. This way, even if the database were compromised, user passwords would remain secure.

Test history for each user is stored, allowing them to track their progress over time. There is a profile page that displays stats based on past tests, providing users with insights into their performance.

Of course, you can play without logging in and access the leaderboards, but you won't find your score there as it is not saved. The gameplay experience is designed to be engaging and competitive, encouraging users to improve their mental math skills while enjoying the challenges presented by the problem sets.


Here is a brief description of the routes:
- **Register:** Supports GET and POST requests. Registers users using a simple registration form.
- **Login:** Supports GET and POST requests. Logs the user in.
- **Index:** The game screen appears here.
- **History:** Logged-in users can see their test history.
- **Profile:** Logged-in users can see their stats.
- **Leaderboard:** Shows the top performers across the site.
- **Submit:** A route that only supports POST requests, which is utilized by the web app internally to store scores after each test finishes. It uses a CSRF token to ensure that the request is valid.

