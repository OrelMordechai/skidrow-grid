let allGames = [];

const grid = document.getElementById("game-grid");
const toggleTheme = document.getElementById("theme-toggle");
const searchBox = document.getElementById("search-box");
const resultCount = document.getElementById("result-count");
const backToTopBtn = document.getElementById("back-to-top");

function renderGames(games) {
  const grid = document.getElementById("game-grid");
  grid.innerHTML = "";
  games.forEach(game => {
    const div = document.createElement("div");
    div.className = "game";
    div.innerHTML = `
      <a href="${game.link}" target="_blank">
        <img src="${game.image}" alt="Game Image">
      </a>
      <div class="game-title" title="${game.title}">
        <a href="${game.link}" target="_blank">${game.title}</a>
      </div>
    `;
    grid.appendChild(div);
  });
}

function updateCount(count) {
  resultCount.textContent =
    count === 1 ? "1 game found" : `${count} games found`;
}


fetch("https://skidrow-backend.onrender.com/api/games")
  .then(res => res.json())
  .then(games => {
    allGames = games;
    renderGames(allGames);
    updateCount(allGames.length); // 👈 הוסף שורה זו
  });


// Start in dark mode
document.body.classList.add("light");
document.getElementById("theme-icon").textContent = "☀️"; // ירח

document.getElementById("theme-toggle").onclick = () => {
  const icon = document.getElementById("theme-icon");

  if (document.body.classList.contains("dark")) {
    document.body.classList.remove("dark");
    document.body.classList.add("light");
    icon.textContent = "☀️"; // שמש
  } else {
    document.body.classList.remove("light");
    document.body.classList.add("dark");
    icon.textContent = "🌙"; // ירח
  }
};


// Filter on search
document.getElementById("search-box").addEventListener("input", (e) => {
  const keyword = e.target.value.toLowerCase();
  const filtered = allGames.filter(g =>
    g.title.toLowerCase().includes(keyword)
  );
  renderGames(filtered);
  updateCount(filtered.length); // 👈 עדכון לאחר סינון
});

window.addEventListener("scroll", () => {
  backToTopBtn.style.display = window.scrollY > 300 ? "block" : "none";
});

backToTopBtn.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});


function updateCount(count) {
  document.getElementById("result-count").textContent =
    count === 1
      ? "1 game found"
      : `${count} games found`;
}
