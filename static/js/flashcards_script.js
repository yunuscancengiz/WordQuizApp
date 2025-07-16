let streak = 0;
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

    const response = await fetch("/flashcard/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ word: document.getElementById("word-display").innerText, meaning: userAnswer })
    });

    const result = await response.json();
    if (result.correct) {
    feedback.textContent = "✅ Correct!";
    feedback.className = "text-green-400 text-center mt-4 font-semibold";
    streak += 1;
    } else {
    feedback.textContent = "❌ Incorrect. Try again!";
    feedback.className = "text-red-400 text-center mt-4 font-semibold";
    streak = 0;
    }

    streakCount.textContent = streak;
    btn.textContent = "Next";
    state = 'next';
} else {
    // Yeni kelime için sayfayı yenile veya AJAX ile çek
    window.location.reload();  // Basit çözüm
}
});