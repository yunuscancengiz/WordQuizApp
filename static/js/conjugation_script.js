let data = null;
let selectedSuggestionIndex = -1;

async function loadJSON() {
  const response = await fetch("/static/verbs.json");
  data = await response.json();
  console.log("Veri yüklendi:", data);
}

function showSuggestions() {
  const inputValue = document.getElementById("searchInput").value.trim().toLowerCase();
  const suggestionBox = document.getElementById("suggestions");

  if (!inputValue || !data) {
    suggestionBox.innerHTML = "";
    suggestionBox.classList.add("hidden");
    return;
  }

  const verbList = data.verbs || data;

  const matches = Object.keys(verbList)
    .filter(verb => verb.startsWith(inputValue))
    .slice(0, 10);

  if (matches.length === 0) {
    suggestionBox.innerHTML = "";
    suggestionBox.classList.add("hidden");
    return;
  }

  // 1. Doldur
  suggestionBox.innerHTML = matches
    .map(verb =>
      `<div data-value="${verb}" class="px-3 py-2 hover:bg-midcolor hover:text-white cursor-pointer">${verb}</div>`
    )
    .join("");

  // 2. Tıklanabilir hale getir
  suggestionBox.querySelectorAll("div").forEach(div => {
    div.addEventListener("click", () => {
      selectSuggestion(div.dataset.value);
    });
  });

  // 3. En son görünür yap
  suggestionBox.classList.remove("hidden");
  selectedSuggestionIndex = -1;
}

function updateSuggestionHighlight(suggestions) {
  const isDarkMode = document.documentElement.classList.contains("dark");

  suggestions.forEach((el, idx) => {
    el.classList.remove("bg-lightcolor", "text-darkcolor", "bg-darkcolor", "text-lightcolor");
    if (idx === selectedSuggestionIndex) {
      if (isDarkMode) {
        el.classList.add("bg-lightcolor", "text-darkcolor");
      } else {
        el.classList.add("bg-darkcolor", "text-lightcolor");
      }
    }
  });

  const activeElement = suggestions[selectedSuggestionIndex];
  if (activeElement) {
    activeElement.scrollIntoView({ block: "nearest" });
  }
}

function selectSuggestion(verb) {
  document.getElementById("searchInput").value = verb;
  document.getElementById("suggestions").innerHTML = "";
  document.getElementById("suggestions").classList.add("hidden");
  searchVerb();
}

function searchVerb() {
  const query = document.getElementById("searchInput").value.trim().toLowerCase();
  if (query) {
    window.location.href = `/conjugations/${query}`;
  }
}

// function toggleDarkMode() {
//   const html = document.documentElement;
//   html.classList.toggle("dark");
//   localStorage.setItem("theme", html.classList.contains("dark") ? "dark" : "light");
// }

(function applyInitialTheme() {
  const html = document.documentElement;
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    html.classList.add("dark");
  } else {
    html.classList.remove("dark");
  }
})();

window.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");

  input.addEventListener("input", showSuggestions);

  input.addEventListener("keydown", function (e) {
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
      suggestionBox.classList.add("hidden");
      selectedSuggestionIndex = -1;
    }
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("#searchInput") && !e.target.closest("#suggestions")) {
      document.getElementById("suggestions").innerHTML = "";
      document.getElementById("suggestions").classList.add("hidden");
    }
  });
});

loadJSON();
