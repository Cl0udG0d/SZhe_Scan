// $(function () {
//   var dqPage = Number("{{paginate.page}}"); //当前页
//   var pageCount = Number("{{paginate.pages}}"); //总页数
//   if ("{{ i }}" == 1) {
//     $("{{ i }}").text(currentPage);
//   } else if ("{{ i }}" == 2) {
//     $("{{ i }}").text(currentPage - 2);
//   } else if ("{{ i }}" == 3) {
//     $("{{ i }}").text(currentPage - 1);
//   } else if ("{{ i }}" == 4) {
//     $("{{ i }}").text(currentPage + 1);
//   } else if ("{{ i }}" == 5) {
//     $("{{ i }}").text(currentPage + 2);
//   }
//   $("#btn2").text(currentPage - 2);

//   $("#btn4").css("color", "#4f90fb");
//   $("#btn4").css("border-color", "#4f90fb");
//   if (currentPage == 1) {
//     $("#prePage").hide();
//   }
//   if (currentPage == pageNum) {
//     $("#sufPage").hide();
//   }
// });

// 分页
function createPage(dqPage, pageCount) {
  var dqPage = Number("{{paginate.page}}"); //当前页
  var pageCount = Number("{{paginate.pages}}"); //总页数
  var pageSize = $("#pageSize").val();
  var i = 1;
  i = parseInt(i);
  $("#pageBtn").html("");
  var item = "";
  item += "<ul class='pagination my-pagination'>";
  if (dqPage == 1) {
    item +=
      "<li><a href='#' style='display: none' aria-label='Previous'><span aria-hidden='true'> < </span></a></li>";
  } else {
    item +=
      "<li><a href='javascript:void(0);' onclick='pageRequest(" +
      (dqPage - 1) +
      "," +
      pageSize +
      ")'  aria-label='Previous'><span aria-hidden='true'> < </span></a></li>";
  }
  if (pageCount <= 5) {
    for (i; i <= pageCount; i++) {
      if (i == dqPage) {
        item += "<li><a class='disabled'>" + i + "</a></li>";
      } else {
        item +=
          "<li><a href='javascript:void(0);' onclick='pageRequest(" +
          i +
          "," +
          pageSize +
          ")'>" +
          i +
          "</a></li>";
      }
    }
  } else if (pageCount > 5) {
    if (dqPage < 5) {
      for (i; i <= 5; i++) {
        if (i == dqPage) {
          item += "<li><a class='disabled'>" + i + "</a></li>";
        } else {
          item +=
            "<li><a href='javascript:void(0);' onclick='pageRequest(" +
            i +
            "," +
            pageSize +
            ")' >" +
            i +
            "</a></li>";
        }
      }
      if (dqPage <= pageCount - 2) {
        item += "<li><span style='background: none'> . . . </span></li>";
      }
    } else if (dqPage >= 5) {
      for (i; i <= 2; i++) {
        item += "<a href='" + href + i + "' >" + i + "</a>";
      }
      item += "<li><span style='background: none'> . . . </span></li>";
      if (dqPage + 1 == pageCount) {
        for (i = dqPage - 1; i <= pageCount; i++) {
          if (i == dqPage) {
            item += "<li><a class='disabled'>" + i + "</a></li>";
          } else {
            item +=
              "<li><a href='javascript:void(0);' onclick='pageRequest(" +
              i +
              "," +
              pageSize +
              ")' >" +
              i +
              "</a></li>";
          }
        }
      } else if (dqPage == pageCount) {
        for (i = dqPage - 2; i <= pageCount; i++) {
          if (i == dqPage) {
            item += "<li><a class='disabled'>" + i + "</a></li>";
          } else {
            item +=
              "<li><a href='javascript:void(0);' onclick='pageRequest(" +
              i +
              "," +
              pageSize +
              ")' >" +
              i +
              "</a></li>";
          }
        }
      } else {
        for (i = dqPage - 1; i <= dqPage + 1; i++) {
          if (i == dqPage) {
            item += "<li><a class='disabled'>" + i + "</a></li>";
          } else {
            item +=
              "<li><a href='javascript:void(0);' onclick='pageRequest(" +
              i +
              "," +
              pageSize +
              ")' >" +
              i +
              "</a></li>";
          }
        }
        item += "<li><span style='background: none'> . . . </span></li>";
      }
    }
  }

  if (dqPage == pageCount) {
    item +=
      "<li><a href='#' style='display: none' aria-label='Previous'><span aria-hidden='true'> > </span></a></li>";
  } else {
    item +=
      "<li><a href='javascript:void(0);' onclick='pageRequest(" +
      (dqPage + 1) +
      "," +
      pageSize +
      ")' aria-label='Previous'><span aria-hidden='true'> > </span></a></li>";
  }
  item += "<li>";
  item += "<div class='btn-group' role='group'>";
  item +=
    "<button type='button' class='btn btn-default dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>10条/页</button>";
  item += "<ul class='dropdown-menu'>";
  item +=
    "<li><a href='javascript:void(0);' onclick='pageRequest(" +
    1 +
    "," +
    10 +
    ")'>10条</a></li>";
  item +=
    "<li><a href='javascript:void(0);' onclick='pageRequest(" +
    1 +
    "," +
    20 +
    ")'>20条</a></li>";
  item +=
    "<li><a href='javascript:void(0);' onclick='pageRequest(" +
    1 +
    "," +
    30 +
    ")'>30条</a></li>";
  item +=
    "<li><a href='javascript:void(0);' onclick='pageRequest(" +
    1 +
    "," +
    40 +
    ")'>40条</a></li>";
  item +=
    "<li><a href='javascript:void(0);' onclick='pageRequest(" +
    1 +
    "," +
    50 +
    ")'>50条</a></li>";
  item += "</ul>";
  item += "</div>";
  item += "</li>";
  item += "<li>跳至</li>";
  item +=
    "<li><input type='text' id='selectIndex' class='form-control page-number' placeholder='5'>页<input type='button' style='background: none' onclick='toInextPage(" +
    pageSize +
    "," +
    pageCount +
    ")' value='确定'></li>";
  item += "<li></li>";
  item += "</ul>";
  $("#pageBtn").append(item);
}
