// $("inp").attr("placeholder", "white");
// changePasswordDisplayState = function () {
//   if ($inputpw.attr("type") == "password") {
//     $inputpw.get(0).setAttribute("type", "text");
//     $eye.get(0).setAttribute("class", "fa fa-eye-slash");
//   } else {
//     $inputpw.get(0).setAttribute("type", "password");
//     $eye.get(0).setAttribute("class", "fa fa-sye");
//   }
// };
var eye = document.getElementById("eye");
var pwd = document.getElementById("pwd");

function showhide() {
  if (pwd.type == "password") {
    pwd.type = "text";
    eye.className = "fa fa-eye-slash";
  } else {
    pwd.type = "password";
    eye.className = "fa fa-eye";
  }
}
