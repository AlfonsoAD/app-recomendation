const table = document.getElementById("table");
const table2 = document.getElementById("table2");

const searchTitle = () => {
  $.ajax({
    type: "POST",
    url: "/searchTitle",
    data: {
      title: $("#titleMovie").val(),
    },
    success: (response) => {
      table.innerHTML = response[0];
      table2.innerHTML = response[1];
      alert("Resultados listos");
    },
    error: () => {
      alert("Error, algo ha salido mal");
    },
  });
};

$("#formulario").on("submit", (e) => {
  e.preventDefault();
  searchTitle();
});

// ---------------------------------------------------------------------------------------------
// Función para tabbar
function openCity(evt, cityName) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
