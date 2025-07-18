let selectedWords = [];

function selectWord(button) {
  const word = button.textContent;
  selectedWords.push(word);
  button.disabled = true;
  button.classList.add("opacity-50", "cursor-not-allowed");
  updateResponseArea();
}

function updateResponseArea() {
  const responseText = document.getElementById("response-text");
  responseText.textContent = selectedWords.join(" ");
}

function resetSentence() {
  selectedWords = [];
  updateResponseArea();

  // Tüm butonları yeniden aktif et
  const buttons = document.querySelectorAll("#word-buttons button");
  buttons.forEach(btn => {
    btn.disabled = false;
    btn.classList.remove("opacity-50", "cursor-not-allowed");
  });

  // Geri bildirim temizle
  document.getElementById("feedback").textContent = "";

  // Submit butonunu tekrar göster
  showSubmitButton();
}

function disableAllButtons() {
  const buttons = document.querySelectorAll("#word-buttons button");
  buttons.forEach(btn => {
    btn.disabled = true;
    btn.classList.add("opacity-50", "cursor-not-allowed");
  });
}

function showNextButton() {
  document.getElementById("submit-btn").classList.add("hidden");
  document.getElementById("next-btn").classList.remove("hidden");
}

function showSubmitButton() {
  document.getElementById("submit-btn").classList.remove("hidden");
  document.getElementById("next-btn").classList.add("hidden");
}

async function submitSentence() {
  const userResponse = selectedWords.join(" ");
  const feedback = document.getElementById("feedback");

  if (!userResponse.trim()) {
    feedback.textContent = "Please construct a sentence first.";
    feedback.className = "text-red-500";
    return;
  }

  try {
    const originalSentence = document.getElementById("original-sentence").value;

    const res = await fetch("/ros/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        current_sentence: originalSentence,
        user_answer: userResponse
      })
    });

    const data = await res.json();

    if (res.ok) {
      if (data.result === "correct") {
        document.getElementById("streak-count").textContent = data.streak;
        feedback.textContent = "✅ Correct!";
        feedback.className = "text-green-500";
        disableAllButtons();
      } else {
        document.getElementById("streak-count").textContent = "0";
        feedback.textContent = `❌ Incorrect! Correct answer: ${data.correct_answer}`;
        feedback.className = "text-red-500";
      }

      // Submit -> Next dönüşümü
      showNextButton();
    }

  } catch (error) {
    console.error("Error submitting sentence:", error);
    feedback.textContent = "Something went wrong.";
    feedback.className = "text-red-500";
  }
}

async function getNextSentence() {
  try {
    const res = await fetch("/ros/next", {
      method: "GET",
      credentials: "include"
    });

    if (!res.ok) throw new Error("Failed to fetch new sentence.");

    const data = await res.json();

    // Yeni cümleyi yerleştir
    selectedWords = [];
    updateResponseArea();
    document.getElementById("original-sentence").value = data.original_sentence;

    const wordButtonsDiv = document.getElementById("word-buttons");
    wordButtonsDiv.innerHTML = "";

    data.splitted_sentence.forEach(word => {
      const button = document.createElement("button");
      button.textContent = word;
      button.className = "bg-lightgreen dark:bg-darkgreen hover:bg-midgreen dark:hover:bg-midgreen text-darkgreen dark:text-lightgreen font-semibold px-4 py-2 rounded-lg transition-all";
      button.onclick = function () {
        selectWord(button);
      };
      wordButtonsDiv.appendChild(button);
    });

    document.getElementById("feedback").textContent = "";

    // Next -> Submit dönüşümü
    showSubmitButton();

  } catch (error) {
    console.error("Error getting next sentence:", error);
    const feedback = document.getElementById("feedback");
    feedback.textContent = "Couldn't load next sentence.";
    feedback.className = "text-red-500";
  }
}
