// Dark mode toggle with localStorage
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("darkToggle");
  const root = document.documentElement;

  // initial theme
  const saved = localStorage.getItem("theme") || "light";
  root.setAttribute("data-theme", saved);
  if (saved === "dark") toggle.textContent = "☀️";
  else toggle.textContent = "🌙";

  toggle.addEventListener("click", function () {
    const current = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", current);
    localStorage.setItem("theme", current);
    toggle.textContent = current === "dark" ? "☀️" : "🌙";
  });

  // small fade-up on scroll
  const faders = document.querySelectorAll(".fade-up");
  const onScroll = () => {
    const trigger = window.innerHeight - 50;
    faders.forEach(el => {
      const top = el.getBoundingClientRect().top;
      if (top < trigger) el.classList.add("visible");
    });
  };
  onScroll();
  window.addEventListener("scroll", onScroll);
});
