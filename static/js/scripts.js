// Animate Navbar - Comes from the top and stays visible
gsap.from(".navbar", {
  duration: 1, 
  y: -50,  // Moves navbar down smoothly
  opacity: 0,  
  ease: "power2.out"
});

// Animate Menu Links - Staggered appearance
gsap.from(".menu a", {
  duration: 1,
  opacity: 0,
  y: 10,  // Moves up slightly instead of disappearing
  stagger: 0.2,
  ease: "power2.out"
});

// Fix disappearing issue by ensuring elements remain visible after animation
gsap.set(".navbar, .menu a", { opacity: 1, y: 0 });

// Button Hover Effect
document.querySelectorAll(".btns button").forEach((button) => {
  button.addEventListener("mouseenter", () => {
      gsap.to(button, { scale: 1.1, duration: 0.2 });
  });
  button.addEventListener("mouseleave", () => {
      gsap.to(button, { scale: 1, duration: 0.2 });
  });
});

// Fix Search Box Animation
const searchBox = document.querySelector(".search-box");
searchBox.addEventListener("mouseenter", () => {
  gsap.to(".search-box input", { width: "200px", duration: 0.3, ease: "power2.out" });
});
searchBox.addEventListener("mouseleave", () => {
  gsap.to(".search-box input", { width: "120px", duration: 0.3, ease: "power2.in" });
});


document.addEventListener("DOMContentLoaded", function() {
    const articles = document.querySelectorAll(".article");
    articles.forEach(article => {
        article.addEventListener("mouseenter", () => {
            article.style.transform = "scale(1.05)";
            article.style.transition = "0.3s ease-in-out";
        });
        article.addEventListener("mouseleave", () => {
            article.style.transform = "scale(1)";
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
  gsap.from(".title", {opacity: 0, y: -50, duration: 1});
  gsap.from(".card", {opacity: 0, y: 50, duration: 1, stagger: 0.3});
});

document.addEventListener("DOMContentLoaded", function() {
  const articles = document.querySelectorAll(".editor-article");
  articles.forEach(article => {
      article.addEventListener("mouseenter", () => {
          article.style.transform = "scale(1.05)";
          article.style.transition = "0.3s ease-in-out";
      });
      article.addEventListener("mouseleave", () => {
          article.style.transform = "scale(1)";
      });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const articles = document.querySelectorAll(".card");
  articles.forEach(article => {
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

document.getElementById("searchBox").addEventListener("input", function() {
  let filter = this.value.toLowerCase();
  let rows = document.querySelectorAll("#tableBody tr");
  rows.forEach(row => {
      let text = row.textContent.toLowerCase();
      if (text.includes(filter)) {
          row.style.display = "table-row";
      } else {
          row.style.display = "none";
      }
  });
});




