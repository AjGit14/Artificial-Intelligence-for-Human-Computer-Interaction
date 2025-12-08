let detailClicks = 0;
let simpleClicks = 0;

document.addEventListener("DOMContentLoaded", () => {
  const toggleButtons = document.querySelectorAll(".toggle-details");
  toggleButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".card");
      const details = card.querySelector(".details");
      const isHidden = details.classList.contains("hidden");

      if (isHidden) {
        // User chose more detail
        details.classList.remove("hidden");
        btn.textContent = "Hide details";
        detailClicks++;
      } else {
        // User collapsed details
        details.classList.add("hidden");
        btn.textContent = "Show more details";
        simpleClicks++;
      }
    });
  });

  const adaptBtn = document.getElementById("adapt-btn");
  adaptBtn.addEventListener("click", adaptInterface);
});

function adaptInterface() {
  const total = detailClicks + simpleClicks;
  const profileLabel = document.getElementById("profile-label");

  if (total === 0) {
    alert("Interact with the modules first so I can learn your preferences!");
    return;
  }

  const detailRatio = detailClicks / total;

  // Simple “AI-like” inference:
  // If user mostly expands details, treat them as expert.
  if (detailRatio > 0.6) {
    document.body.classList.remove("mode-beginner");
    document.body.classList.add("mode-expert");
    profileLabel.textContent =
      "Current profile: Expert (dense layout, more info visible)";
  } else {
    document.body.classList.remove("mode-expert");
    document.body.classList.add("mode-beginner");
    profileLabel.textContent =
      "Current profile: Beginner-friendly (larger fonts, less info per card)";
  }
}
