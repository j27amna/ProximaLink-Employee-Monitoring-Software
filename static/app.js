function filterLogs(category) {
  var logs = document.querySelectorAll(".log-entry");

  logs.forEach(function (log) {
    if (category === "all") {
      log.style.display = "block"; // Show all logs if 'All' is selected
    } else {
      // Check if log entry has the specified category class
      var hasCategory = log.classList.contains(category);

      // Toggle display based on category match
      log.style.display = hasCategory ? "block" : "none";
    }
  });
}

$(document).ready(function () {
  $("#sidebarCollapse").on("click", function () {
    $(".sidebar").toggleClass("active");
  });
});
