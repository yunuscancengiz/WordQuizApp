let data = null;
let selectedSuggestionIndex = -1;

async function loadJSON() {
  const response = await fetch("/static/verbs.json");
  data = await response.json();
}

function showSuggestions() {
  const input = document.getElementById("searchInput").value.trim().toLowerCase();
  const suggestionBox = document.getElementById("suggestions");

  if (!input || !data || !data.verbs) {
    suggestionBox.innerHTML = "";
    return;
  }

  const matches = Object.keys(data.verbs).filter(verb => verb.startsWith(input)).slice(0, 10);

  if (matches.length === 0) {
    suggestionBox.innerHTML = "";
    return;
  }

  suggestionBox.innerHTML = matches.map(verb =>
    `<div data-value="${verb}">${verb}</div>`
  ).join("");

  selectedSuggestionIndex = -1;
}

function updateSuggestionHighlight(suggestions) {
  suggestions.forEach((el, idx) => {
    el.classList.toggle("active", idx === selectedSuggestionIndex);
  });

  const activeElement = suggestions[selectedSuggestionIndex];
  if (activeElement) {
    activeElement.scrollIntoView({ block: "nearest" });
  }
}

function selectSuggestion(verb) {
  document.getElementById("searchInput").value = verb;
  document.getElementById("suggestions").innerHTML = "";
  searchVerb();
}

function searchVerb() {
  const query = document.getElementById("searchInput").value.trim().toLowerCase();
  if (query) {
    window.location.href = `/conjugations/${query}`;
  }
}

function toggleDarkMode() {
  document.body.classList.toggle("dark");
  localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
}

(function applyInitialTheme() {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
  }
})();

document.addEventListener("click", function (e) {
  if (!e.target.closest("#searchInput") && !e.target.closest("#suggestions")) {
    document.getElementById("suggestions").innerHTML = "";
  }
});

document.getElementById("searchInput").addEventListener("input", showSuggestions);

document.getElementById("searchInput").addEventListener("keydown", function (e) {
  const suggestionBox = document.getElementById("suggestions");
  const suggestions = suggestionBox.querySelectorAll("div");

  if (e.key === "Enter") {
    e.preventDefault();
    if (suggestions.length > 0 && selectedSuggestionIndex >= 0) {
      const selectedVerb = suggestions[selectedSuggestionIndex].dataset.value;
      selectSuggestion(selectedVerb);
    } else {
      searchVerb();
    }
  }

  if (e.key === "ArrowDown") {
    e.preventDefault();
    if (suggestions.length === 0) return;
    selectedSuggestionIndex = (selectedSuggestionIndex + 1) % suggestions.length;
    updateSuggestionHighlight(suggestions);
  }

  if (e.key === "ArrowUp") {
    e.preventDefault();
    if (suggestions.length === 0) return;
    selectedSuggestionIndex = (selectedSuggestionIndex - 1 + suggestions.length) % suggestions.length;
    updateSuggestionHighlight(suggestions);
  }

  if (e.key === "Escape") {
    suggestionBox.innerHTML = "";
    selectedSuggestionIndex = -1;
  }
});

loadJSON();
