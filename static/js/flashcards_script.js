let state = 'submit';  // 'submit' or 'next'

const form = document.getElementById("flashcard-form");
const input = document.getElementById("meaning-input");
const btn = document.getElementById("submit-btn");
const feedback = document.getElementById("feedback");
const streakCount = document.getElementById("streak-count");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  if (state === 'submit') {
    const userAnswer = input.value.trim();

    const response = await fetch("/flashcards/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_word: document.getElementById("word-display").innerText,
        user_answer: userAnswer
      }),
      credentials: "include"
    });

    const result = await response.json();

    feedback.textContent = result.result === 'correct'
      ? "✅ Correct!"
      : `❌ Incorrect! Correct answer: ${result.correct_answer}`;

    feedback.className = result.result === 'correct'
      ? "text-green-400 text-center mt-4 font-semibold"
      : "text-red-400 text-center mt-4 font-semibold";

    streakCount.textContent = result.streak;

    btn.textContent = "Next";
    state = 'next';
  } else {
    // 🎯 Yeni kelimeyi AJAX ile çek
    const response = await fetch("/flashcards/next", {
      method: "GET",
      credentials: "include"
    });

    const data = await response.json();

    // ✅ Ekranı güncelle
    document.getElementById("word-display").textContent = data.word;

    const sentenceList = document.getElementById("sentence-list");
    sentenceList.innerHTML = "";  // Önceki cümleleri temizle
    data.sentences.forEach(sentence => {
      const li = document.createElement("li");
      li.textContent = sentence;
      sentenceList.appendChild(li);
    });

    feedback.textContent = "";
    feedback.className = "";

    input.value = "";
    input.focus();

    btn.textContent = "Submit";
    state = "submit";

    streakCount.textContent = data.streak;
  }
});
