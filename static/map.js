function myFunction() {
  var x = document.getElementById("mappa-div");
  if (x.style.display === "none") {
    x.style.display = "block";
    document.querySelector('#mappa-btn').value = 'Nascondi mappa';
  } else {
    x.style.display = "none";
    document.querySelector('#mappa-btn').value = 'Mostra mappa';
  }
}