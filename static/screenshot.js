$(document).ready(function () {
  var currentIndex = 0;
  var screenshots = [];

  // Function to close the overlay modal
  function closeModal() {
    $("#overlayModal").modal("hide");
  }

  // Function to show the image at the specified index
  function showImage(index) {
    $("#overlayImage").attr("src", screenshots[index].src);
    updateDots(index);
  }

  // Function to update the navigation dots
  function updateDots(index) {
    $("#navDots .dot").removeClass("active");
    $("#navDots .dot").eq(index).addClass("active");
  }

  // Listen for click on Keystrokes button (if needed)
  $("#btnKeystrokes").click(function () {
    // Implement behavior for Keystrokes button click (if needed)
  });

  // Listen for click on Screenshots button (if needed)
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

  // Listen for click on Videos button (if needed)
  $("#btnVideos").click(function () {
    // Implement behavior for Videos button click (if needed)
  });

  // Initialize the screenshots array and dots
  $(".screenshot-thumbnail").each(function (index) {
    screenshots.push({
      src: $(this).attr("src"),
      caption: $(this).data("caption"),
    });

    $("#navDots").append('<div class="dot" data-index="' + index + '"></div>');
  });

  // Show the first image initially
  if (screenshots.length > 0) {
    showImage(0);
  }

  // Event listener for navigation dots
  $("#navDots").on("click", ".dot", function () {
    var index = $(this).data("index");
    currentIndex = index;
    showImage(index);
  });

  // Event listeners for navigation buttons
  $("#prevImage").click(function () {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : screenshots.length - 1;
    showImage(currentIndex);
  });

  $("#nextImage").click(function () {
    currentIndex = currentIndex < screenshots.length - 1 ? currentIndex + 1 : 0;
    showImage(currentIndex);
  });

  // Initialize modal with the first image
  if (screenshots.length > 0) {
    showImage(0);
  }
});
