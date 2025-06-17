// ===================== 定数・要素取得 =====================
const wordDisplay = document.getElementById("word");
const input = document.getElementById("input");
const scoreDisplay = document.getElementById("score");
const timerDisplay = document.getElementById("timer");
const startBtn = document.getElementById("start-btn");
const correctSE = document.getElementById("correct-se");

let score = 0;
let time = 30;
let interval;
let current = "";

// 文字化け用のカオス漢字
const kanjiChaos = "縺繧縲繝妛彁硲暃坩堝竈箪笥隋臧艱艷靡黌鼾齊龕龜龠堯槇".split("");

// 単語一覧（表示：ひらがな、判定：ローマ字）
import {hiraganaSamples} from "./word_easy.js";

// ===================== 画面切り替え =====================
function GameScreen() {
  document.getElementById("startScreen").style.display = "none";
  document.getElementById("gameScreen").style.display = "block";
}

function BackScreen() {
  document.getElementById("startScreen").style.display = "block";
  document.getElementById("gameScreen").style.display = "none";
}

function onStartClick() {
  GameScreen();
  startGame();
}

// ===================== ゲーム処理 =====================
function startGame() {
  score = 0;
  time = 30;
  scoreDisplay.textContent = "Score: 0";
  timerDisplay.textContent = "Time: 30";
  input.value = "";
  input.disabled = false;

  current = getRandomWord();
  displayWord(current);

  interval = setInterval(() => {
    time--;
    timerDisplay.textContent = `Time: ${time}`;
    if (time <= 0) {
      timerDisplay.textContent = "Time: 0";
      endGame();
    }
  }, 1000);
}

function endGame() {
  clearInterval(interval);
  input.disabled = true;
  wordDisplay.textContent = `終了！あなたのスコアは ${score} 点でした！`;
}

// ===================== 単語処理 =====================
function getRandomWord() {
  return hiraganaSamples[Math.floor(Math.random() * hiraganaSamples.length)];
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
  setTimeout(() => {
    wordDisplay.textContent = "";
  }, 5000); // 5秒後
}

// ===================== 文字化けロジック =====================
function mutateWithChaos(text) {
  const chars = text.split("");
  let mutated = chars.map(c =>
    Math.random() < 0.3
      ? kanjiChaos[Math.floor(Math.random() * kanjiChaos.length)]
      : c
  );

  // 1文字も変化してなかったら、1文字だけ強制変化
  if (mutated.join("") === text && chars.length > 0) {
    const i = Math.floor(Math.random() * chars.length);
    mutated[i] = kanjiChaos[Math.floor(Math.random() * kanjiChaos.length)];
  }

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
      return;
    }
  }
  if (input.value === current.answer) {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
    input.value = "";

    correctSE.currentTime = 0;
    correctSE.play();

    current = getRandomWord();
    displayWord(current);
  }
});

// ===================== ボタン実行 =====================
document.getElementById("hard").addEventListener("click", GameScreen);
document.getElementById("easy").addEventListener("click", GameScreen);
document.getElementById("back").addEventListener("click", BackScreen);
startBtn.addEventListener("click", onStartClick);

