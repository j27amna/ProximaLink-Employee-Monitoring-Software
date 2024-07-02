// app.js
function filterLogs(user, category) {
  var logEntries = document.querySelectorAll(".log-entry");

  logEntries.forEach(function (entry) {
    var isKeystroke = entry.classList.contains("key-stroke");
    var isClipboard = entry.classList.contains("clipboard");

    if (
      (category === "KeyStroke" && isKeystroke) ||
      (category === "Clipboard" && isClipboard && user === "Clipboard")
    ) {
      entry.style.display = "block";
    } else {
      entry.style.display = "none";
    }
  });
}
