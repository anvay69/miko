(() => {let settings = document.querySelector("#settings");
let startMsg = document.querySelector("#startMessage");
let gameArea = document.querySelector("#gameArea");
let resultArea = document.querySelector("#resultSection");

let totalProblems = 5;
let timePerProblem = 15000;
let solvedProblems;
let startTime;
let tInterval;
let pTimeout;
let pSetTime;
let timeTaken;
let difficulty;
let problems;
let currAnswer;
let score;


document.getElementById("nextTestButton").addEventListener("click", (event) => {
    setUp();
});


document.getElementById("answerInput").addEventListener("input", (event) => {
    let value = event.target.value.trim();
    
    if (value && Number(value) != NaN) {
        if (Number(value) == currAnswer) {
            solvedProblems += 1;
            clearTimeout(pTimeout);
            let diff = new Date().getTime() - pSetTime;
            score += (15000 - diff);
            setProblem();
        }
    }
});

// event listener which starts the game
const keyDownHandler = (event) => {
    settings.classList.add("hidden");
    startMsg.classList.add("hidden");

    gameArea.classList.remove("hidden");

    document.removeEventListener("keydown", keyDownHandler);

    startGame();
};


// function to get an object of problems
function getProblems(numProblems, difficulty) {
    const problemsList = [];
    const operators = ['+', '-', '*', '/'];

    // Define number ranges based on difficulty
    let min, max;
    switch (difficulty) {
        case 'easy':
            min = 1;
            max = 10; // One to two-digit numbers
            break;
        case 'medium':
            min = 1;  // Allow two-digit and above
            max = 10; // Two to three-digit numbers
            break;
        case 'hard':
            min = 1; // Allow three-digit and above
            max = 10; // Three to four-digit numbers
            break;
        default:
            throw new Error('Invalid difficulty level. Please use "easy", "medium", or "hard".');
    }

    for (let i = 0; i < numProblems; i++) {
        // Generate two random numbers within the specified range
        const num1 = Math.floor(Math.random() * (max - min + 1)) + min;
        const num2 = Math.floor(Math.random() * (max - min + 1)) + min;
        const operator = operators[Math.floor(Math.random() * operators.length)];

        // Create a math problem string
        let problem;
        let answer;

        // Handle division to avoid division by zero
        if (operator === '/') {
            // Ensure the divisor is not zero
            const divisor = num2 === 0 ? 1 : num2; // Set divisor to 1 if it's zero
            problem = `${num1} ${operator} ${divisor}`;
            answer = (num1 / divisor).toFixed(1); // Round to 1 decimal place
        } else {
            problem = `${num1} ${operator} ${num2}`;
            answer = eval(problem); // Calculate the answer
        }

        // Create an object for the problem and solution
        const problemObject = {
            problem: problem,
            solution: answer
        };

        // Add the problem object to the list
        problemsList.push(problemObject);
    }

    return problemsList;
}

function setUp() {
    score = 0;
    solvedProblems = 0;
    document.addEventListener("keydown", keyDownHandler);
    document.getElementById("timeDisplay").textContent = "0s";

    settings.classList.remove("hidden");
    startMsg.classList.remove("hidden");
    gameArea.classList.add("hidden");
    resultArea.classList.add("hidden");
}


function startGame() {
    document.getElementById("answerInput").focus();

    difficulty = getDifficulty();
    problems = getProblems(totalProblems, difficulty);
    
    document.getElementById("counterText").textContent = `Solved: ${solvedProblems} / ${totalProblems}`;
    startTime = new Date().getTime();
    tInterval = setInterval(updateTime, 1000);
    setProblem();

}


function getDifficulty() {
    let difficultyOption = document.querySelector(".difficulty-option.selected");
    if (!difficultyOption) throw new Error("No difficulty selected");

    let difficulty = difficultyOption.getAttribute("data-value");
    if (!["easy", "medium", "hard"].includes(difficulty)) {
        throw new Error("Difficulty not recognised");
    }

    return difficulty;
}

function updateTime() {
    let diff = new Date().getTime() - startTime;
    let timer = document.getElementById("timeDisplay");
    timer.textContent = `${Math.floor(diff / 1000)}s`;
}


function setProblem() {
    if (problems && problems.length != 0) {
        let problem = problems.shift();

        document.getElementById("counterText").textContent = `${totalProblems - problems.length}/${totalProblems}`
        document.getElementById("problemDisplay").textContent = problem["problem"];
        document.getElementById("answerInput").value = "";

        currAnswer = problem["solution"];
        
        pSetTime = new Date().getTime();
        pTimeout = setTimeout(setProblem, timePerProblem);

    } else {
        gameOver();
    }
}


function gameOver() {
    clearInterval(tInterval);

    timeTaken = (new Date().getTime() - startTime) / 1000;
    score /= 1000;

    let csrf = document.getElementById("mikoCsrf").value;

    gameArea.classList.add("hidden");
    resultArea.classList.remove("hidden");

    submitScore(csrf, score, solvedProblems, totalProblems, difficulty, timeTaken, new Date().getTime());

    document.getElementById("score").textContent = `Score: ${score}`;
    document.getElementById("timeTaken").textContent = `Time Taken: ${timeTaken}s`;
    document.getElementById("solvedCount").textContent = `${solvedProblems}/${totalProblems}`;
}


function submitScore(csrf, score, solved, total, difficulty, time_taken, timestamp) {
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            csrf: csrf, // CSRF token
            score: score, // Score value
            solved: solved, // Number of problems solved
            total: total, // Total number of problems
            difficulty: difficulty, // Difficulty level
            time: time_taken, // Time taken
            timestamp: timestamp // Timestamp
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Handle success response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error); // Handle error
    });
}

setUp();})()