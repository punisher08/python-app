function showSpinner() {
  document.getElementById("loadingSpinner").style.display = "block";
  document.querySelector(".btn-label").innerHTML = "loading";
}

function hideSpinner() {
  document.getElementById("loadingSpinner").style.display = "none";
  document.querySelector(".btn-label").innerHTML = "Completed";
}
