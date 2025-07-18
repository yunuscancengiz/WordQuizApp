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
            document.getElementById("message").classList.remove("hidden");
            document.getElementById("message").textContent = "✅ Theme updated.";
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