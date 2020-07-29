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

//页码部分
$(function () {
  var currentPage = Number("{{paginate.page}}"); //当前页
  var pageNum = Number("{{paginate.pages}}"); //总页数
  if ("{{ i }}" == 1) {
    $("{{ i }}").text(currentPage);
  }
  //  else if ("{{ i }}" == 2) {
  //   $("{{ i }}").text(currentPage - 2);
  // } else if ("{{ i }}" == 3) {
  //   $("{{ i }}").text(currentPage - 1);
  // } else if ("{{ i }}" == 4) {
  //   $("{{ i }}").text(currentPage + 1);
  // } else if ("{{ i }}" == 5) {
  //   $("{{ i }}").text(currentPage + 2);
  // }
  // $("#btn2").text(currentPage - 2);

  // $("#btn4").css("color", "#4f90fb");
  // $("#btn4").css("border-color", "#4f90fb");
  if (currentPage == 1) {
    $("#prePage").hide();
  }
  if (currentPage == pageNum) {
    $("#sufPage").hide();
  }
});
