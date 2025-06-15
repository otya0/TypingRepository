//定義
//targetからwordDisplayに変更
const wordDisplay = document.getElementById("word");
const input = document.getElementById("input");
const scoreDisplay = document.getElementById("score");
const timerDisplay = document.getElementById("timer");
const startBtn = document.getElementById("start-btn");
const correctSE = document.getElementById("correct-se");

let score;
let time;
let interval;
let current = "";
const kanjiChaos = "縺繧縲繝妛彁硲暃坩堝竈箪笥隋臧艱艷靡黌鼾齊龕龜龠堯槇".split(
  ""
);

const hiraganaSamples = [
  "こんにちは",
  "おはよう",
  "さようなら",
  "ありがとう",
  "すみません",
  "たのしいね",
  "ねこがすき",
  "あしたもがんばろう",
  "ゆうやけきれい",
  "まいにちれんしゅう",
];

//関数
function GameScreen() {
  document.getElementById("startScreen").style.display = "none";
  document.getElementById("gameScreen").style.display = "block";
}
function onStartClick() {
  GameScreen();
  startGame();
}

function BackScreen() {
  document.getElementById("startScreen").style.display = "block";
  document.getElementById("gameScreen").style.display = "none";
}

//出力の中心となる部分

function startGame() {
  score = 0;
  time = 120;
  scoreDisplay.textContent = "Score: 0";
  timerDisplay.textContent = "Time: 120";
  input.value = "";
  input.disabled = false;
  //input.focus();
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

function getRandomWord() {
  return hiraganaSamples[Math.floor(Math.random() * hiraganaSamples.length)];
}

function displayWord(word) {
  wordDisplay.classList.remove("pop");
  void wordDisplay.offsetWidth;
  wordDisplay.classList.add("pop");
  wordDisplay.textContent = word;

  // 文字が数秒後に変化
  setTimeout1(() => {
    let chars = word.split("");
    //chをcに変更
    let mutated = chars.map((c) =>
      Math.random() < 0.3 //0.3の確率つまり30%の確率で文字が乱れる マジックナンバーはちゃんと説明をかくこと！
        ? kanjiChaos[Math.floor(Math.random() * kanjiChaos.length)]
        : c
    );
    wordDisplay.textContent = mutated.join("");
  }, 2000); //2秒後に文字が乱れるマジックナンバーには説明を加えること

  // さらに5秒後に消える
  setTimeout2(() => {
    wordDisplay.textContent = "";
  }, 5000); //５秒後に文字が乱れるマジックナンバーには説明を加えること
}

//判定
input.addEventListener("input", () => {
  if (input.value === current) {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
    input.value = "";
    correctSE.currentTime = 0;
    correctSE.play();
    current = getRandomWord();
    displayWord(current);
  }
});

function endGame() {
  clearInterval(interval);
  input.disabled = true;
  wordDisplay.textContent = `終了！あなたのスコアは ${score} 点でした！`;
}
//実行
document.getElementById("hard").addEventListener("click", GameScreen);
document.getElementById("easy").addEventListener("click", GameScreen);
document.getElementById("back").addEventListener("click", BackScreen);
startBtn.addEventListener("click", onStartClick);

//問題点
//スタートが何回も押せる←スタートボタンを隠す
//音が鳴る時とならないときがある。←原因を探す
//予測変換ださないようにする
//タイプミスしたら入力できないようにする

const typingArea = document.getElementById("typing-area");
let answer = "konnichiwa"; // 例：現在の答え
let buffer = "";

// 最初はフォーカスを当てておく
typingArea.focus();

// キー入力を全部ここで受け取る
window.addEventListener("keydown", (e) => {
  let k = e.key;

  // バックスペースは「取り消し」扱い
  if (k === "Backspace") {
    buffer = buffer.slice(0, -1);
    typingArea.textContent = buffer;
    return;
  }

  // 文字キー以外は無視（Tab や Shift, Alt など）
  if (k.length !== 1) return;

  k = k.toLowerCase(); // 大文字対応

  // 期待文字を取得
  const expected = answer[buffer.length];

  if (k === expected) {
    // 正解ならバッファに追加して表示更新
    buffer += k;
    typingArea.textContent = buffer;

    // もし全問正解なら次の処理へ…
    if (buffer.length === answer.length) {
      // 例：次の単語をセットして buffer = "" etc.
    }
  } else {
    // ミスなら何も追加せず振動フィードバック
    typingArea.classList.add("shake");
    setTimeout(() => typingArea.classList.remove("shake"), 150);
  }
});
