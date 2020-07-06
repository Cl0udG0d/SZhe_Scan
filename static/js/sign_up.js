var eye1 = document.getElementById("eye1");
var pwd1 = document.getElementById("user_password1");

function showhide() {
  if (user_password1.type == "password") {
    user_password1.type = "text";
    eye1.className = "fa fa-eye-slash";
  } else {
    user_password1.type = "password";
    eye1.className = "fa fa-eye";
  }
}

var eye2 = document.getElementById("eye2");
var pwd2 = document.getElementById("user_password2");

function showhide1() {
  if (user_password2.type == "password") {
    user_password2.type = "text";
    eye2.className = "fa fa-eye-slash";
  } else {
    user_password2.type = "password";
    eye2.className = "fa fa-eye";
  }
}
