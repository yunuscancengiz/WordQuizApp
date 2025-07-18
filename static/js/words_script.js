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
    card.className = "bg-lightcolor dark:bg-darkcolor text-darkcolor dark:text-lightcolor p-4 rounded-lg shadow";

    card.innerHTML = `
      <p class="font-bold text-lg cursor-pointer hover:underline" id="word-text-${word.id}">${word.word}</p>

      <div id="details-${word.id}" class="mt-4 hidden">
        <p>Meaning: <span class="meaning-text" id="meaning-${word.id}">${word.meaning}</span></p>
        <p>Sentence: <span class="sentence-text" id="sentence-${word.id}">Loading...</span></p>
        <div class="flex gap-2 mt-2">
          <button onclick="toggleEditForm(${word.id})" class="bg-yellow-400 text-darkcolor px-3 py-1 rounded hover:bg-yellow-300 transition">Edit</button>
          <button onclick="deleteWord(${word.id})" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition">Delete</button>
        </div>

        <form id="edit-form-${word.id}" class="mt-4 hidden grid grid-cols-1 sm:grid-cols-2 gap-4" onsubmit="submitEditForm(event, ${word.id})">
          <input type="text" id="edit-word-${word.id}" placeholder="Word" value="${word.word}" class="w-full px-3 py-2 border rounded text-darkcolor col-span-1 sm:col-span-2">
          <input type="text" id="edit-meaning-${word.id}" placeholder="Meaning" value="${word.meaning}" class="w-full px-3 py-2 border rounded text-darkcolor col-span-1 sm:col-span-2">
          <input type="text" id="edit-sentence-${word.id}" placeholder="Sentence" class="w-full px-3 py-2 border rounded text-darkcolor col-span-1 sm:col-span-2">
          <button type="submit" class="w-full col-span-1 sm:col-span-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-800 transition">Save Changes</button>
        </form>
      </div>
    `;

    container.appendChild(card);

    // Sadece başlığa tıklanınca detay aç/kapat
    const title = card.querySelector(`#word-text-${word.id}`);
    title.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleDetails(null, word.id);
    });
  });
}

async function toggleDetails(_, id) {
  const details = document.getElementById(`details-${id}`);
  const sentenceSpan = document.getElementById(`sentence-${id}`);
  const editInput = document.getElementById(`edit-sentence-${id}`);

  details.classList.toggle("hidden");

  if (!details.classList.contains("hidden")) {
    try {
      const res = await fetch(`/words/word/${id}`, { credentials: "include" });
      if (!res.ok) throw new Error("Fetch failed.");
      const wordData = await res.json();
      sentenceSpan.textContent = wordData.sentence || "No example available.";
      if (editInput) editInput.value = wordData.sentence || "";
    } catch {
      sentenceSpan.textContent = "Failed to load sentence.";
      if (editInput) editInput.value = "";
    }
  }
}

function toggleEditForm(id) {
  const form = document.getElementById(`edit-form-${id}`);
  form.classList.toggle("hidden");
}

async function submitEditForm(event, id) {
  event.preventDefault();

  const wordInput = document.getElementById(`edit-word-${id}`);
  const meaningInput = document.getElementById(`edit-meaning-${id}`);
  const sentenceInput = document.getElementById(`edit-sentence-${id}`);

  const updatedWord = wordInput.value.trim();
  const updatedMeaning = meaningInput.value.trim();
  const updatedSentence = sentenceInput.value.trim();

  if (!updatedWord || !updatedMeaning || !updatedSentence) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const res = await fetch(`/words/word/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        word: updatedWord,
        meaning: updatedMeaning,
        sentence: updatedSentence
      })
    });

    if (!res.ok) throw new Error("Update failed.");

    // UI'ı güncelle
    document.getElementById(`word-text-${id}`).textContent = updatedWord;
    document.getElementById(`meaning-${id}`).textContent = updatedMeaning;
    document.getElementById(`sentence-${id}`).textContent = updatedSentence;

    toggleEditForm(id);
  } catch (error) {
    console.error("Failed to update word:", error);
    alert("Failed to update word.");
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

function toggleAddWordForm() {
  const form = document.getElementById("add-word-form");
  form.classList.toggle("hidden");
}

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
