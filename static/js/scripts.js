const menuBtn = document.getElementById("menu-toggle");
const mobilemenu = document.getElementById("mobile-menu");

menuBtn.addEventListener("click", () => {
  mobilemenu.classList.toggle("hidden");
});

document.addEventListener("DOMContentLoaded", function () {
  const articles = document.querySelectorAll(".article");
  articles.forEach((article) => {
    article.addEventListener("mouseenter", () => {
      article.style.transform = "scale(1.05)";
      article.style.transition = "0.3s ease-in-out";
    });
    article.addEventListener("mouseleave", () => {
      article.style.transform = "scale(1)";
    });
  });
});

// document.addEventListener("DOMContentLoaded", () => {
//   gsap.from(".title", {opacity: 0, y: -50, duration: 1});
//   gsap.from(".card", {opacity: 0, y: 50, duration: 1, stagger: 0.3});
// });

document.addEventListener("DOMContentLoaded", function () {
  const articles = document.querySelectorAll(".editor-article");
  articles.forEach((article) => {
    article.addEventListener("mouseenter", () => {
      article.style.transform = "scale(1.05)";
      article.style.transition = "0.3s ease-in-out";
    });
    article.addEventListener("mouseleave", () => {
      article.style.transform = "scale(1)";
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const articles = document.querySelectorAll(".card");
  articles.forEach((article) => {
    article.addEventListener("mouseenter", () => {
      article.style.transform = "scale(1.05)";
      article.style.transition = "0.3s ease-in-out";
    });
    article.addEventListener("mouseleave", () => {
      article.style.transform = "scale(1)";
    });
  });
});

// stock code

// document.getElementById("searchBox").addEventListener("input", function() {
//   let filter = this.value.toLowerCase();
//   let rows = document.querySelectorAll("#tableBody tr");
//   rows.forEach(row => {
//       let text = row.textContent.toLowerCase();
//       if (text.includes(filter)) {
//           row.style.display = "table-row";
//       } else {
//           row.style.display = "none";
//       }
//   });
// });
