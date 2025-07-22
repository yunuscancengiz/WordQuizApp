document.addEventListener("DOMContentLoaded", () => {
  // Scroll animasyonları, badge hover veya dark mode desteği gibi gelişmiş etkileşimler ileride eklenebilir.

  // Badge hover efektleri (istersen kullanabilirsin)
  const badges = document.querySelectorAll(".badge-img");
  badges.forEach((badge) => {
    badge.addEventListener("mouseenter", () => {
      badge.classList.add("scale-105", "brightness-110");
    });
    badge.addEventListener("mouseleave", () => {
      badge.classList.remove("scale-105", "brightness-110");
    });
  });

  // About metni uzunluğu kontrolü (max 500 karakter gibi sınırlamalar ileride eklenebilir)
});
