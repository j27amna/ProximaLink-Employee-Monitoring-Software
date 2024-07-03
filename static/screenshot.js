// static/screenshot.js

$(document).ready(function () {
  let currentImageIndex = 0;
  let images = [];

  // Collect image elements and initialize modal
  $(".img-thumbnail").each(function (index) {
    images.push($(this).attr("data-image"));

    $(this).click(function () {
      currentImageIndex = index;
      updateModal();
      $("#overlayModal").modal("show");
    });
  });

  function updateModal() {
    $("#overlayImage").attr("src", images[currentImageIndex]);
  }

  // Navigation buttons
  $("#prevImage").click(function () {
    if (currentImageIndex > 0) {
      currentImageIndex--;
      updateModal();
    }
  });

  $("#nextImage").click(function () {
    if (currentImageIndex < images.length - 1) {
      currentImageIndex++;
      updateModal();
    }
  });
});
