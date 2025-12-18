let settings = document.querySelector("#settings");
let startMsg = document.querySelector("#startMessage");
let gameArea = document.querySelector("#gameArea");
let resultArea = document.querySelector("#resultSection");


// event listener which starts the game
const keyDownHandler = (event) => {
    settings.classList.add("hidden");
    startMsg.classList.add("hidden");

    gameArea.classList.remove("hidden");

    document.removeEventListener("keydown", keyDownHandler);
};

function setUp() {
    document.addEventListener("keydown", keyDownHandler);
}


setUp();