document.addEventListener("DOMContentLoaded", function () {
  const radios = document.querySelectorAll('input[name="theme"]');

  radios.forEach(radio => {
    radio.addEventListener("change", async function () {
      const themeId = this.getAttribute("data-theme-id");

      try {
        const response = await fetch(`/themes/use/${themeId}`, {
          method: "PATCH",
          credentials: "include"
        });

        if (response.ok) {
          const data = await response.json();

          document.getElementById("message").classList.remove("hidden");
          document.getElementById("message").textContent = "✅ Theme updated.";

          // Temayı uygula ve localStorage'a kaydet
          applyThemeColors(data.theme);
          localStorage.setItem("activeTheme", JSON.stringify(data.theme));
        } else {
          alert("Failed to update theme.");
        }
      } catch (err) {
        console.error(err);
        alert("An error occurred.");
      }
    });
  });
});

function applyThemeColors(theme) {
  if (!theme) return;
  document.documentElement.style.setProperty('--darkcolor', theme.darkcolor);
  document.documentElement.style.setProperty('--midcolor', theme.midcolor);
  document.documentElement.style.setProperty('--lightcolor', theme.lightcolor);
}