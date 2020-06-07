function openList(evt, cityName) {
  var i, tabPane, tablinks;
  tabPane = document.getElementsByClassName("tabPane");
  for (i = 0; i < tabPane.length; i++) {
    tabPane[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
function show1() {
  var True = document.getElementsByClassName(true);
  var False = document.getElementsByClassName(false);
  var x = 1;
  if (True[0].style.display != "none") {
    True[0].style.display = "none";
    False[0].style.display = "inline";
  } else {
    True[0].style.display = "inline";
    False[0].style.display = "none";
  }
}
