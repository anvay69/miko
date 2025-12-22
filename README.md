# Miko

#### Video Demo: https://www.youtube.com/watch?v=CEWQ30UQedU

#### Description:
My project is a mental math game site. I've used Flask and SQLite3 to implement the backend of the web app. The front end requires HTML, CSS, JavaScript, along with Bootstrap.

Users can create an account or play without making one. If you do create an account, your score will be stored, and you'll appear on the leaderboards!

Test history for each user is stored, so you can look at your progress anytime. 

There is a profile page that shows your stats based on your past tests.

Of course, you can play without logging in and access the leaderboards, but you won't find your score there as it is not saved.

#### Here is a brief description of the routes:
- **Register:** Supports GET and POST requests. Registers users using a simple registration form.
- **Login:** Supports GET and POST requests. Logs the user in.
- **Index:** The game screen appears here.
- **History:** Logged-in users can see their test history.
- **Profile:** Logged-in users can see their stats.
- **Leaderboard:** Shows the top performers across the site.
- **Submit:** A route that only supports POST requests, which is utilized by the web app internally to store scores after each test finishes. It uses a CSRF token to ensure that the request is valid.

