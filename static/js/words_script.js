let allWords = [];

document.addEventListener("DOMContentLoaded", () => {
  getAllWords();
  document.getElementById("new-word-form").addEventListener("submit", handleAddWord);
});

async function getAllWords() {
  try {
    const res = await fetch("/words/api", { credentials: "include" });
    if (!res.ok) throw new Error("Failed to fetch words.");
    allWords = await res.json();
    displayWords(allWords);
  } catch (error) {
    console.error("Error fetching words:", error);
    document.getElementById("word-list").innerHTML =
      "<p class='text-center text-red-500'>Unable to load words. Try again later.</p>";
  }
}

function searchWord() {
  const query = document.getElementById("search-input").value.toLowerCase().trim();
  const filtered = allWords.filter(w => w.word.toLowerCase().includes(query));
  displayWords(filtered);
}

function displayWords(words) {
  const container = document.getElementById("word-list");
  container.innerHTML = "";

  if (words.length === 0) {
    container.innerHTML = "<p class='text-center text-red-500'>No words found.</p>";
    return;
  }

  words.forEach(word => {
    const card = document.createElement("div");
    card.className = "bg-lightgreen dark:bg-darkgreen text-darkgreen dark:text-lightgreen p-4 rounded-lg shadow cursor-pointer transition hover:scale-[1.02]";
    card.innerHTML = `
      <div class="flex justify-between items-center">
        <h3 class="text-xl font-bold">${word.word}</h3>
        <button onclick="toggleDetails(event, ${word.id})" class="text-sm text-midgreen underline">Details</button>
      </div>
      <div id="details-${word.id}" class="mt-4 hidden">
        <p><strong>Meaning:</strong> <span id="meaning-${word.id}">${word.meaning}</span></p>
        <p><strong>Example:</strong> <span id="sentence-${word.id}">Loading...</span></p>
        <div class="flex gap-3 mt-3">
          <button onclick="editWord(${word.id})" class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded">Edit</button>
          <button onclick="deleteWord(${word.id})" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded">Delete</button>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

async function toggleDetails(event, id) {
  event.stopPropagation();
  const details = document.getElementById(`details-${id}`);
  const sentenceSpan = document.getElementById(`sentence-${id}`);
  details.classList.toggle("hidden");

  if (!details.classList.contains("hidden")) {
    try {
      const res = await fetch(`/words/word/${id}`, { credentials: "include" });
      if (!res.ok) throw new Error("Fetch failed.");
      const wordData = await res.json();
      sentenceSpan.textContent = wordData.sentence || "No example available.";
    } catch {
      sentenceSpan.textContent = "Failed to load sentence.";
    }
  }
}

function editWord(id) {
  const currentMeaning = document.getElementById(`meaning-${id}`).textContent;
  const newMeaning = prompt("Edit meaning:", currentMeaning);
  if (newMeaning && newMeaning !== currentMeaning) {
    fetch(`/words/word/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ word: allWords.find(w => w.id === id).word, meaning: newMeaning })
    }).then(() => {
      document.getElementById(`meaning-${id}`).textContent = newMeaning;
    });
  }
}

function deleteWord(id) {
  if (confirm("Are you sure you want to delete this word?")) {
    fetch(`/words/word/${id}`, {
      method: "DELETE",
      credentials: "include"
    }).then(() => {
      allWords = allWords.filter(w => w.id !== id);
      displayWords(allWords);
    });
  }
}

// Show/Hide Add Word Form
function toggleAddWordForm() {
  const form = document.getElementById("add-word-form");
  form.classList.toggle("hidden");
}

// Handle Add Word
async function handleAddWord(event) {
  event.preventDefault();

  const word = document.getElementById("new-word").value.trim();
  const meaning = document.getElementById("new-meaning").value.trim();
  const sentence = document.getElementById("new-sentence").value.trim();

  if (!word || !meaning || !sentence) {
    alert("Please fill in all fields.");
    return;
  }

  const alreadyExists = allWords.some(w => w.word.toLowerCase() === word.toLowerCase());
  if (alreadyExists) {
    alert("This word already exists in your list.");
    return;
  }

  try {
    const res = await fetch("/words/word", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        word: { word, meaning },
        correct_incorrect: { is_last_time_correct: true },
        sentence: { sentence }
      })
    });

    if (!res.ok) throw new Error("Failed to add word.");

    // Clear form
    document.getElementById("new-word").value = "";
    document.getElementById("new-meaning").value = "";
    document.getElementById("new-sentence").value = "";

    toggleAddWordForm();
    await getAllWords();
  } catch (error) {
    console.error("Error adding word:", error);
    alert("Failed to add word. Try again.");
  }
}
