$(function () {
  var currentPage = Number("{{paginate.page}}"); //当前页
  var pageNum = Number("{{paginate.pages}}"); //总页数

  $("#btn2").text(currentPage - 2);
  $("#btn3").text(currentPage - 1);
  $("#btn4").text(currentPage);
  $("#btn5").text(currentPage + 1);
  $("#btn6").text(currentPage + 2);
  $("#btn7").text(pageNum);

  $("#btn4").css("color", "#4f90fb");
  $("#btn4").css("border-color", "#4f90fb");

  if (currentPage == 1) {
    $("#prePage").hide();
  }

  if (currentPage == pageNum) {
    $("#sufPage").hide();
  }

  if (currentPage <= 3) {
    $("#prePoint").hide();
    $("#btn1").hide();
  } else if (currentPage == 4) {
    $("#prePoint").hide();
  }
  if (currentPage == 1) {
    $("#btn2").hide();
    $("#btn3").hide();
  } else if (currentPage == 2) {
    $("#btn2").hide();
  }

  if (currentPage >= pageNum - 2) {
    $("#sufPoint").hide();
    $("#btn7").hide();
  } else if (currentPage == pageNum - 3) {
    $("#sufPoint").hide();
  }

  if (currentPage == pageNum) {
    $("#btn5").hide();
    $("#btn6").hide();
  }

  if (currentPage == pageNum - 1) {
    $("#btn6").hide();
  }
});
