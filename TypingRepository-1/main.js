const words = ["ありがとう", "こんにちは", "さようなら", "やきにく", "おはよう", "さくら", "たんじょうび", "きょうりゅう"];
let current = "";
let score = 0;
let timeLeft = 30;
let interval, timer;
let startTime;
const input = document.getElementById("input");
const target = document.getElementById("target");
const scoreDisplay = document.getElementById("score");
const timeDisplay = document.getElementById("time");
const wpmDisplay = document.getElementById("wpm");
const startBtn = document.getElementById("startBtn");



function StartScreenGame() {
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';


    function getRandomWord() {
        return words[Math.floor(Math.random() * words.length)];
    }

    function displayWord(word) {
        target.textContent = word;
    }

    function changeWordRandomly() {
        // 20%の確率でランダムなひらがなに1文字すり替える
        if (Math.random() < 0.5) {
            const hira = "あいうえおかきくけこさしすせそたちつてとなにぬねの";
            const chars = current.split("");
            const index = Math.floor(Math.random() * chars.length);
            chars[index] = hira[Math.floor(Math.random() * hira.length)];
            displayWord(chars.join(""));
        } else {
            displayWord(current); // 変化しない（フェイント）
        }
    }

    function startGame() {
        score = 0;
        timeLeft = 30;
        current = getRandomWord();
        displayWord(current);
        input.value = "";
        input.disabled = false;
        input.focus();
        scoreDisplay.textContent = "0";
        timeDisplay.textContent = "30";
        wpmDisplay.textContent = "0";
        startTime = Date.now();

        interval = setInterval(() => {
            changeWordRandomly();
        }, 3000); // 3秒ごとに文字が変化

        timer = setInterval(() => {
            timeLeft--;
            timeDisplay.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(interval);
                clearInterval(timer);
                input.disabled = true;
                const minutes = (Date.now() - startTime) / 60000;
                const wpm = Math.round(score / minutes);
                wpmDisplay.textContent = wpm;
                target.textContent = "終了！また挑戦してね！";
            }
        }, 1000);
    }

    input.addEventListener("input", () => {
        if (input.value === current) {
            score++;
            scoreDisplay.textContent = score;
            input.value = "";
            current = getRandomWord();
            displayWord(current);
        }
    });

    startBtn.addEventListener("click", startGame);
};
function BackScreenGame() {
    document.getElementById('startScreen').style.display = 'block';
    document.getElementById('gameScreen').style.display = 'none';
};
document.getElementById('hard').addEventListener('click', StartScreenGame);
document.getElementById('easy').addEventListener('click', StartScreenGame);
document.getElementById('back').addEventListener('click', BackScreenGame);
