let state = 'submit'; // 'submit' or 'next'
let selectedChoice = null;

const feedback = document.getElementById("feedback");
const streakCount = document.getElementById("streak-count");
const choicesContainer = document.getElementById("choices-container");
const wordDisplay = document.getElementById("quiz-word");

async function submitAnswer(button) {
  if (state === 'submit') {
    // Tıklanan butonun cevabını al
    selectedChoice = button.dataset.choice;
    const currentWord = wordDisplay.textContent.trim();

    const response = await fetch("/quiz/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        current_word: currentWord,
        user_answer: selectedChoice
      })
    });

    const result = await response.json();

    feedback.textContent = result.result === 'correct'
      ? "✅ Correct!"
      : `❌ Incorrect! Correct answer: ${result.correct_answer}`;

    feedback.className = result.result === 'correct'
      ? "text-green-400 text-center mt-4 font-semibold"
      : "text-red-400 text-center mt-4 font-semibold";

    streakCount.textContent = result.streak;

    // Tüm butonları disable et
    const buttons = document.querySelectorAll("#choices-container button");
    buttons.forEach(btn => {
      btn.disabled = true;
      btn.classList.add("opacity-50", "cursor-not-allowed");
    });

    // Next butonu ekle
    const nextBtn = document.createElement("button");
    nextBtn.id = "next-btn";
    nextBtn.textContent = "Next";
    nextBtn.className = "w-full bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded-lg transition mt-4";
    nextBtn.onclick = getNextQuiz;
    choicesContainer.appendChild(nextBtn);

    state = 'next';
  }
}

async function getNextQuiz() {
  const res = await fetch("/quiz/next", {
    method: "GET",
    credentials: "include"
  });

  const data = await res.json();

  // Ekranı sıfırla ve güncelle
  wordDisplay.textContent = data.word;
  streakCount.textContent = data.streak;
  feedback.textContent = "";
  feedback.className = "";

  // Şıkları temizle ve yeniden oluştur
  choicesContainer.innerHTML = "";
  data.choices.forEach(choice => {
    const btn = document.createElement("button");
    btn.textContent = choice;
    btn.dataset.choice = choice;
    btn.className = "w-full bg-lightcolor dark:bg-darkcolor hover:bg-midcolor text-darkcolor dark:text-lightcolor font-semibold py-2 px-4 rounded transition-all";
    btn.onclick = function () {
      submitAnswer(btn);
    };
    choicesContainer.appendChild(btn);
  });

  state = 'submit';
}
