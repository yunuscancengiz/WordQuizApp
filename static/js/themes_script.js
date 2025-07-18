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

          // 🎨 Yeni renkleri anında uygula
          if (data.theme) {
            applyThemeColors(data.theme);
          }
        } else {
          alert("Failed to update theme.");
        }
      } catch (err) {
        console.error(err);
        alert("An error occurred.");
      }
    });
  });

  function applyThemeColors(theme) {
    if (!theme) return;

    // Eski geçici stil varsa kaldır
    const oldStyle = document.getElementById("dynamic-theme-style");
    if (oldStyle) oldStyle.remove();

    // Yeni stil etiketi oluştur ve güncel renkleri yaz
    const style = document.createElement("style");
    style.id = "dynamic-theme-style";
    style.innerHTML = `
      :root {
        --darkcolor: ${theme.darkcolor};
        --midcolor: ${theme.midcolor};
        --lightcolor: ${theme.lightcolor};
      }
    `;
    document.head.appendChild(style);

    // Gerekirse Tailwind dark class'ını da koru
    document.documentElement.classList.add("dark");
  }
});
