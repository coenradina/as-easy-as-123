(function () {
  "use strict";

  /* ============== config ============== */
  var PASSWORD = "gutierritos";
  var SESSION_KEY = "jar_unlocked";

  var GREETINGS = ["hola", "hihihihi", "haaaii", "halooo"];
  var NICKNAMES = [
    "mi vida",
    "cariño",
    "sayang",
    "mi hogar",
    "mi guapo",
    "alejandrito",
    "cintaku",
  ];
  var MOODS = ["happy", "sad", "tired", "bored", "idk", "missingMe"];

  /* ============== password screen ============== */
  var passwordScreen = document.getElementById("password-screen");
  var appScreen = document.getElementById("app-screen");
  var passwordForm = document.getElementById("password-form");
  var passwordInput = document.getElementById("password-input");
  var passwordError = document.getElementById("password-error");
  var passwordCard = document.querySelector(".password-card");

  function unlock() {
    passwordScreen.classList.add("hidden");
    appScreen.classList.remove("hidden");
    try {
      sessionStorage.setItem(SESSION_KEY, "1");
    } catch (e) {
      /* ignore storage errors */
    }
  }

  passwordForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var value = (passwordInput.value || "").trim().toLowerCase();
    if (value === PASSWORD) {
      unlock();
    } else {
      passwordError.textContent = "hmm, that's not it. try again?";
      passwordCard.classList.remove("shake");
      // force reflow so the animation can replay
      void passwordCard.offsetWidth;
      passwordCard.classList.add("shake");
      passwordInput.value = "";
      passwordInput.focus();
    }
  });

  try {
    if (sessionStorage.getItem(SESSION_KEY) === "1") {
      unlock();
    }
  } catch (e) {
    /* ignore storage errors */
  }

  /* ============== main app ============== */
  var jar = document.getElementById("jar");
  var bubble = document.getElementById("bubble");
  var bubbleText = document.getElementById("bubble-text");
  var hint = document.getElementById("hint");
  var moods = document.getElementById("moods");
  var letterOverlay = document.getElementById("letter-overlay");
  var letterCard = document.getElementById("letter-card");
  var letterText = document.getElementById("letter-text");
  var letterClose = document.getElementById("letter-close");

  var currentNickname = "";
  var greetTimeout = null;

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function showBubble(text, isSwap) {
    bubbleText.textContent = text;
    bubble.hidden = false;
    if (isSwap) {
      bubble.classList.remove("swap");
      void bubble.offsetWidth;
      bubble.classList.add("swap");
    }
  }

  function startGreeting() {
    if (greetTimeout) {
      clearTimeout(greetTimeout);
    }
    hint.classList.add("hidden");
    var greeting = pick(GREETINGS);
    showBubble(greeting, false);

    greetTimeout = setTimeout(function () {
      currentNickname = pick(NICKNAMES);
      showBubble("how are you feeling today, " + currentNickname + "?", true);
      moods.hidden = false;
    }, 1400);
  }

  jar.addEventListener("click", function () {
    startGreeting();
  });

  /* ---------- mood letter draw (shuffle-bag per mood, no repeats until exhausted) ---------- */
  var bags = {};

  function shuffledIndices(length) {
    var arr = [];
    for (var i = 0; i < length; i++) arr.push(i);
    for (var j = arr.length - 1; j > 0; j--) {
      var k = Math.floor(Math.random() * (j + 1));
      var tmp = arr[j];
      arr[j] = arr[k];
      arr[k] = tmp;
    }
    return arr;
  }

  function drawLetter(mood) {
    var pool = window.LETTERS[mood] || [];
    if (!pool.length) return "";

    if (!bags[mood] || bags[mood].length === 0) {
      bags[mood] = shuffledIndices(pool.length);
    }
    var idx = bags[mood].pop();
    return pool[idx];
  }

  var moodButtons = moods.querySelectorAll(".mood-btn");
  for (var m = 0; m < moodButtons.length; m++) {
    moodButtons[m].addEventListener("click", function (e) {
      var mood = e.currentTarget.getAttribute("data-mood");
      var text = drawLetter(mood);
      letterText.textContent = text;
      letterOverlay.hidden = false;
    });
  }

  function closeLetter() {
    letterOverlay.hidden = true;
  }

  letterClose.addEventListener("click", closeLetter);
  letterOverlay.addEventListener("click", function (e) {
    if (e.target === letterOverlay) {
      closeLetter();
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !letterOverlay.hidden) {
      closeLetter();
    }
  });
})();
