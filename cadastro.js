document.getElementById("marca").addEventListener("change", function() {
  var campoOutro = document.getElementById("campo-outro");
  var outraMarcaInput = document.getElementById("outra-marca");

  if (this.value === "outro") {
    campoOutro.style.display = "block";
    outraMarcaInput.setAttribute("required", "true");
  } else {
    campoOutro.style.display = "none";
    outraMarcaInput.removeAttribute("required");
  }
});