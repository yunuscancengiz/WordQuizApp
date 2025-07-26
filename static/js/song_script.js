document.addEventListener("DOMContentLoaded", () => {
  renderPagination();
});

function renderPagination() {
  const paginationDiv = document.getElementById("pagination");
  paginationDiv.innerHTML = "";

  const createPageButton = (page) => {
    const btn = document.createElement("button");
    btn.textContent = page;
    btn.className =
      "px-3 py-1 rounded-lg border " +
      (page === currentPage
        ? "bg-midcolor text-darkcolor font-bold"
        : "bg-lightcolor dark:bg-darkcolor text-midcolor");

    btn.addEventListener("click", () => {
      if (page !== currentPage) {
        window.location.href = `/songs?page=${page}`;
      }
    });

    return btn;
  };

  let pagesToShow = [];

  if (totalPages <= 10) {
    pagesToShow = Array.from({ length: totalPages }, (_, i) => i + 1);
  } else {
    pagesToShow = [1, 2, 3, 4, 5, 6, 7, 8, 9, totalPages];
  }

  pagesToShow.forEach((page, index) => {
    if (index > 0 && page - pagesToShow[index - 1] > 1) {
      const dots = document.createElement("span");
      dots.textContent = "...";
      dots.className = "px-2";
      paginationDiv.appendChild(dots);
    }
    paginationDiv.appendChild(createPageButton(page));
  });
}
