//页码部分
$(function () {
  var currentPage = Number("{{paginate.page}}"); //当前页
  var pageNum = Number("{{paginate.pages}}"); //总页数
  if ("{{ i }}" == 1) {
    $("{{ i }}").text(currentPage);
  }
  // else if ("{{ i }}" == 2) {
  //   $("{{ i }}").text(currentPage - 2);
  // } else if ("{{ i }}" == 3) {
  //   $("{{ i }}").text(currentPage - 1);
  // } else if ("{{ i }}" == 4) {
  //   $("{{ i }}").text(currentPage + 1);
  // } else if ("{{ i }}" == 5) {
  //   $("{{ i }}").text(currentPage + 2);
  // }
  // $("#btn2").text(currentPage - 2);

  $("#btn4").css("color", "#4f90fb");
  $("#btn4").css("border-color", "#4f90fb");
  if (currentPage == 1) {
    $("#prePage").hide();
  }
  if (currentPage == pageNum) {
    $("#sufPage").hide();
  }
});
