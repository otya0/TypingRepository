// ===================== 定数・要素取得 =====================
const wordDisplay = document.getElementById("word");
const input = document.getElementById("input");
const scoreDisplay = document.getElementById("score");
const timerDisplay = document.getElementById("timer");
const startBtn = document.getElementById("start-btn");
const correctSE = document.getElementById("correct-se");
const incorrectSE = document.getElementById("incorrect-se");
const attackSE = document.getElementById("attack-se");

let score = 0;
let time = 30;
let interval;
let current = "";
let difficulty = "easy";
let attackInterval;

// 文字化け用のカオス漢字
const kanjiChaos =
  "縺繧縲繝妛彁硲暃坩堝竈箪笥隋臧艱艷靡黌鼾齊龕龜龠堯槇 ".split("");

// 単語一覧（表示：ひらがな、判定：ローマ字）
import { hiraganaSamples as easyWords } from "./hiraganaSamples_with_count.js";
import { hiraganaSamples as hardWords } from "./word_hard.js";
// ===================== 画面切り替え =====================
function GameScreen() {
  document.getElementById("startScreen").style.display = "none";
  document.getElementById("gameScreen").style.display = "block";
}

function BackScreen() {
  clearInterval(interval);
  clearInterval(attackInterval);
  startBtn.disabled = false;
  input.value = "";
  score = 0;
  time = difficulty === "easy" ? 30 : 60;
  scoreDisplay.textContent = "0";
  timerDisplay.textContent = `${time}`;

  wordDisplay.textContent = "スタートを押してね";
  document.getElementById("startScreen").style.display = "block";
  document.getElementById("gameScreen").style.display = "none";
}

function onStartClick() {
  startBtn.disabled = true;
  GameScreen();
  startGame();
  input.focus();
}

// ===================== ゲーム処理 =====================
function startGame() {
  if (difficulty === "easy") {
    startEasyMode();
  } else if (difficulty === "hard") {
    startHardMode();
  }
}

function startEasyMode() {
  score = 0;
  time = 30;
  scoreDisplay.textContent = "0";
  timerDisplay.textContent = "30";
  input.value = "";
  input.disabled = false;

  current = getRandomWord();
  displayWord(current);

  interval = setInterval(() => {
    time--;
    timerDisplay.textContent = `${time}`;
    if (time <= 0) {
      timerDisplay.textContent = "0";
      endGame();
    }
  }, 1000);
}

function startHardMode() {
  score = 0;
  time = 60;
  scoreDisplay.textContent = "0";
  timerDisplay.textContent = "60";
  input.value = "";
  input.disabled = false;

  current = getRandomWord();
  displayWord(current);

  interval = setInterval(() => {
    time--;
    timerDisplay.textContent = `${time}`;
    if (time <= 0) {
      timerDisplay.textContent = "0";
      endGame();
    }
  }, 1000);
}

function endGame() {
  clearInterval(interval);
  clearInterval(attackInterval);
  input.disabled = true;
  startBtn.disabled = false;

  time = difficulty === "easy" ? 30 : 60;

  wordDisplay.textContent = `終了！あなたのスコアは ${score} 点でした！`;
  startBtn.disabled = false;
  setTimeout(() => {
    startAttackSequence(score);
  }, 2000);
}

// ===================== 単語処理 =====================
function getRandomWord() {
  const wordList = difficulty === "hard" ? hardWords : easyWords;
  return wordList[Math.floor(Math.random() * wordList.length)];
}

function displayWord(word) {
  // アニメーション用のclass再適用
  wordDisplay.classList.remove("pop");
  void wordDisplay.offsetWidth;
  wordDisplay.classList.add("pop");

  // 表示（ひらがな）
  wordDisplay.textContent = word.display;

  // 2秒後にカオス文字化け
  setTimeout(() => {
    wordDisplay.textContent = mutateWithChaos(word.display);
  }, 2000); // 2秒後

  // さらに3秒後（計5秒後）に消える
  if (difficulty === "hard") {
    const eraseDelay = 5000;
    setTimeout(() => {
      wordDisplay.textContent = "";
    }, eraseDelay);
  }
}

// ===================== 文字化けロジック =====================
function mutateWithChaos(text) {
  const chars = text.split("");
  let mutated = chars.map((c) =>
    Math.random() < 0.3
      ? kanjiChaos[Math.floor(Math.random() * kanjiChaos.length)]
      : c
  );

  return mutated.join("");
}

// ===================== 入力判定 =====================
input.addEventListener("input", () => {
  const inputText = input.value;
  const answer = current.answer;

  // 1文字ずつ厳密にチェック
  for (let i = 0; i < inputText.length; i++) {
    if (inputText[i] !== answer[i]) {
      // 間違った文字を削除（最後に入力した文字を除去）
      input.value = inputText.slice(0, -1);
      incorrectSE.currentTime = 0;
      incorrectSE.play();
      return;
    }
  }
  if (input.value === current.answer) {
    score++;
    scoreDisplay.textContent = `${score}`;
    input.value = "";

    correctSE.currentTime = 0;
    correctSE.play();

    current = getRandomWord();
    displayWord(current);
  }
});
//攻撃フェーズへ
function startAttackSequence(hitCount) {
  const bear = document.getElementById("target-bear");
  const log = document.getElementById("damage-log");
  
  //開始前にログをなくす
  log.innerHTML = "";
  bear.style.display = "block";
  log.style.display = "block";

  let totalDamage = 0;
  let count = 0;

  const attackInterval = setInterval(() => {
    if (count >= hitCount) {
      clearInterval(attackInterval);
      log.innerHTML += `<p style="color: yellow; font-size: 50px;">合計 ${totalDamage} ダメージ！</p>`;
      setTimeout(() => {
        bear.style.display = "none";
        log.style.display ="none";
        log.innerHTML = "";
      }, 4000);
      return;
    }

    const damage = count * 20 + 1;
    totalDamage += damage;

    // ダメージログ追加
    log.innerHTML += `<p>${count + 1} 回目の攻撃：${damage} ダメージ！</p>`;
    setTimeout(() => {
      log.innerHTML = "";
    }, 500);
    // アニメーション付加

    bear.classList.remove("hit"); // 再発動のためリセット
    void bear.offsetWidth; // DOM再読み込み
    bear.classList.add("hit");
    attackSE.currentTime = 0;
    attackSE.play();

    count++;
  }, 600); // 攻撃間隔
}

// ===================== ボタン実行 =====================
document.getElementById("hard").addEventListener("click", () => {
  difficulty = "hard";
  startBtn.disabled = false;
  input.value = "";
  score = 0;
  scoreDisplay.textContent = "0";
  timerDisplay.textContent = "60";
  GameScreen();
});
document.getElementById("easy").addEventListener("click", () => {
  difficulty = "easy";
  startBtn.disabled = false;
  input.value = "";
  score = 0;
  scoreDisplay.textContent = "0";
  timerDisplay.textContent = "30";
  GameScreen();
});
document.getElementById("back").addEventListener("click", BackScreen);
startBtn.addEventListener("click", onStartClick);
