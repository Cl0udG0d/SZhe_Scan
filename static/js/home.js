// /*饼状图部分*/
// function drawCircle(canvasId, data_arr, color_arr, text_arr) {
//   var c = document.getElementById(canvasId);
//   var ctx = c.getContext("2d");

//   var radius = c.height / 2 + 0;
//   var ox = radius + 40,
//     oy = radius + 0;

//   var width = 10,
//     height = 10;
//   var posX = ox * 2 - 8,
//     posY = 78; //
//   var textX = posX + width + 5,
//     textY = posY + 10;

//   var startAngle = 0;
//   var endAngle = 0;
//   for (var i = 0; i < data_arr.length; i++) {
//     endAngle = endAngle + data_arr[i] * Math.PI * 2;
//     ctx.fillStyle = color_arr[i];
//     ctx.beginPath();
//     ctx.moveTo(ox, oy);
//     ctx.arc(ox, oy, radius, startAngle, endAngle, false);
//     ctx.closePath();
//     ctx.fill();
//     startAngle = endAngle;

//     ctx.fillStyle = color_arr[i];
//     ctx.fillRect(posX, posY + 20 * i, width, height);
//     ctx.moveTo(posX, posY + 20 * i);
//     ctx.font = "bold 12px 微软雅黑";
//     ctx.fillStyle = color_arr[i];
//     var percent = text_arr[i] + "：" + 100 * data_arr[i] + "%";
//     ctx.fillText(percent, textX, textY + 20 * i);
//   }
// }
// function init() {
//   //绘制饼图
//   //比例数据和颜色
//   var data_arr = [0.25, 0.25, 0.25, 0.25];
//   var color_arr = ["#1e90ff", "#3cb371", "#fd7e14", "#cc0000"];
//   var text_arr = ["低危", "中危", "高危", "严重"];

//   drawCircle("canvas_circle", data_arr, color_arr, text_arr);
// }

// window.onload = init;

// 饼状图部分
var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};

app.title = "百分比";

var option = {
  tooltip: {
    trigger: "item",
    formatter: "{a} <br/>{b}: {c} ({d}%)",
  },
  color: ["#90ee90", "#7342fa", "#fdb903", "#e9003a"],
  legend: {
    orient: "horizontal",
    x: "top",
    data: ["低危", "中危", "高危", "严重"],
  },
  series: [
    {
      name: "漏洞属性",
      type: "pie",
      radius: ["30%", "70%"],
      avoidLabelOverlap: false,
      label: {
        normal: {
          show: false,
          position: "center",
        },
        emphasis: {
          show: true,
          textStyle: {
            fontSize: "15",
            fontWeight: "bold",
          },
        },
      },
      labelLine: {
        normal: {
          show: false,
        },
      },
      data: [
        {
          value: 135,
          name: "低危",
        },
        {
          value: 170,
          name: "中危",
        },
        {
          value: 234,
          name: "高危",
        },
        {
          value: 265,
          name: "严重",
        },
      ],
    },
  ],
};
if (option && typeof option === "object") {
  myChart.setOption(option, true);
}

/*漏洞类型部分*/
$(".skill-per").each(function () {
  var $this = $(this);
  var per = $this.attr("per");
  $this.css("width", per);
  $({ animatedValue: 0 }).animate(
    { animatedValue: per },
    {
      duartion: 300,
      step: function () {
        $this.attr("per", Math.floor(this.animatedValue));
      },
      complete: function () {
        $this.attr("per", Math.floor(this.animatedValue));
      },
    }
  );
});
