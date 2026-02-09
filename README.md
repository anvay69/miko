# Miko - Mental Math Game

![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=flat&logo=bootstrap&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja-000000?style=flat&logo=jinja&logoColor=white)


Welcome to **Miko**, a cozy web application where you can enjoy a fun and relaxing experience while sharpening your mental math skills. Whether you choose to create an account or play as a guest, you can track your scores and compete on leaderboards, making every session both enjoyable and rewarding.


## Tools Used

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript, Bootstrap


## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:anvay69/miko.git
   cd miko
   ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**:
    ```bash
    python setup_database.py
    ```

5. **Run the Application**:
    ```bash
    flask run
    ```

6. **Access the Application**:
Open http://127.0.0.1:5000 in your browser.


## Features
- **User Registration and Login**:
Users can create an account to track their progress and scores.

- **Gameplay**:
The game offers mental math challenges with three difficulty modes: Easy, Medium, and Hard. Each mode varies the number of digits in numbers. Players have 15 seconds to solve 5 problems in each round.

- **Scoring System**:
Scores are based on the time taken to solve problems. Faster responses yield higher scores, promoting quick thinking. Both the time limit and number of problems can be easily adjusted in the code.

- **Leaderboards**:
Users compete for top spots on the leaderboard, which displays the highest scores in each difficulty.

- **Profile Page & History**:
Each user has a profile page that shows their statistics in each difficulty setting. Users can also see their game history.

- **Security**:
The application includes CSRF protection and password hashing to secure user data, ensuring that personal information is kept safe.

- **Real-time Score Updates**:
After completing a round, JavaScript makes a POST request to update the user’s score in the database, enabling real-time tracking of achievements.


## Routes Overview

- **Register**: User registration (GET/POST)
- **Login**: User login (GET/POST)
- **Index**: Main game screen
- **History**: Test history for logged-in users
- **Profile**: User stats and performance
- **Leaderboard**: Top performers
- **Submit**: Store scores (POST only, CSRF protected)


## Security Measures

- **CSRF Token** Verification: Validates requests to prevent unauthorized actions.
- **Password Hashing**: Ensures user passwords are secure.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

