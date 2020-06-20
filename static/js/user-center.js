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
function dele() {
  var follow;
  follow = document.getElementsByClassName("myFollow");
  follow.style.display = "none";
}
