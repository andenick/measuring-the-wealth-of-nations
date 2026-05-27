// RMWND Shiny — Theme Toggle
// Toggles body.dark-mode class and sends the theme state to the Shiny server.

function toggleTheme() {
  var body = document.body;
  var isDark = body.classList.toggle("dark-mode");
  var mode = isDark ? "dark" : "light";

  // Update toggle icon
  var toggle = document.getElementById("theme_toggle");
  if (toggle) {
    var icon = toggle.querySelector("i");
    if (icon) {
      icon.className = isDark ? "fa fa-sun" : "fa fa-moon";
    }
  }

  // Persist preference
  localStorage.setItem("rmwnd-theme", mode);

  // Notify Shiny server
  if (window.Shiny && Shiny.setInputValue) {
    Shiny.setInputValue("app_theme", mode, { priority: "event" });
  }
}

// Restore theme on page load
document.addEventListener("DOMContentLoaded", function () {
  var saved = localStorage.getItem("rmwnd-theme");
  if (saved === "dark") {
    document.body.classList.add("dark-mode");
    var toggle = document.getElementById("theme_toggle");
    if (toggle) {
      var icon = toggle.querySelector("i");
      if (icon) icon.className = "fa fa-sun";
    }
    // Notify Shiny after connection
    $(document).on("shiny:connected", function () {
      Shiny.setInputValue("app_theme", "dark", { priority: "event" });
    });
  }
});
