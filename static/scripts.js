document.addEventListener("DOMContentLoaded", function () {
  const toggleKeylogsButton = document.getElementById("toggleKeylogs");
  const toggleScreenshotsButton = document.getElementById("toggleScreenshots");
  const keylogsSection = document.getElementById("keylogsSection");
  const screenshotsSection = document.getElementById("screenshotsSection");
  const overlayModal = document.getElementById("overlayModal");
  const overlayImage = document.getElementById("overlayImage");

  toggleKeylogsButton.addEventListener("click", function () {
    keylogsSection.style.display = "block";
    screenshotsSection.style.display = "none";
  });

  toggleScreenshotsButton.addEventListener("click", function () {
    keylogsSection.style.display = "none";
    screenshotsSection.style.display = "block";
  });

  $("#overlayModal").on("show.bs.modal", function (event) {
    const button = $(event.relatedTarget);
    const imageSrc = button.data("image");
    overlayImage.src = imageSrc;
  });
});
