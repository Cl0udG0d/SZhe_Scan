/*饼状图部分*/
function drawCircle(canvasId, data_arr, color_arr, text_arr) {
  var c = document.getElementById(canvasId);
  var ctx = c.getContext("2d");

  var radius = c.height / 2 + 0;
  var ox = radius + 40,
    oy = radius + 0;

  var width = 10,
    height = 10;
  var posX = ox * 2 - 8,
    posY = 78; //
  var textX = posX + width + 5,
    textY = posY + 10;

  var startAngle = 0;
  var endAngle = 0;
  for (var i = 0; i < data_arr.length; i++) {
    endAngle = endAngle + data_arr[i] * Math.PI * 2;
    ctx.fillStyle = color_arr[i];
    ctx.beginPath();
    ctx.moveTo(ox, oy);
    ctx.arc(ox, oy, radius, startAngle, endAngle, false);
    ctx.closePath();
    ctx.fill();
    startAngle = endAngle;

    ctx.fillStyle = color_arr[i];
    ctx.fillRect(posX, posY + 20 * i, width, height);
    ctx.moveTo(posX, posY + 20 * i);
    ctx.font = "bold 12px 微软雅黑";
    ctx.fillStyle = color_arr[i];
    var percent = text_arr[i] + "：" + 100 * data_arr[i] + "%";
    ctx.fillText(percent, textX, textY + 20 * i);
  }
}
function init() {
  //绘制饼图
  //比例数据和颜色
  var data_arr = [0.25, 0.25, 0.25, 0.25];
  var color_arr = ["#6495ed", "#6a5acd", "#c63300", "#8b0000"];
  var text_arr = ["低危", "中危", "高危", "严重"];

  drawCircle("canvas_circle", data_arr, color_arr, text_arr);
}

window.onload = init;

/*漏洞类型部分*/
$(".skill-per").each(function () {
  var $this = $(this);
  var per = $this.attr("per");
  $this.css("width", per);
  $({ animatedValue: 0 }).animate(
    { animatedValue: per },
    {
      duartion: 1000,
      step: function () {
        $this.attr("per", Math.floor(this.animatedValue));
      },
      complete: function () {
        $this.attr("per", Math.floor(this.animatedValue));
      },
    }
  );
});
