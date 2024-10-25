function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      alert("success: copied!");
    })
    .catch((err) => {
      console.error("Could not copy: ", err);
    });
}
