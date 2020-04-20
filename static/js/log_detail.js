function ApplyStyle(s) {
  document.getElementById("myTab").className = s.innerText;
}

$(function () {
  addHover("myTab");
});

/**
 * 在鼠标悬停时突出显示行--jQuery处理表格
 *
 * @tab table id
 */
function addHover(tab) {
  $("#" + tab + " tr").hover(
    function () {
      $(this).find("td").addClass("hover");
    },
    function () {
      $(this).find("td").removeClass("hover");
    }
  );
}
